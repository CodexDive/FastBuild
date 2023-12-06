#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@file: __init__.py.py
@time: 2022/12/14 15:26
@desc: 用于接收页面的请求，得到镜像制作任务信息以及镜像的json详情
"""
import multiprocessing
import threading

import jsonpickle
from docker.errors import APIError
from fastapi import APIRouter

from data.fb_exception import FBException
from data.image_descriptor import ImageDescriptor
from data.image_request import ImageRequest
from data.image_utils import ImageUtils
from data.task import Task
from data.task_manager import delete_task
from db.db_image_check_result_service import DBImageCheckResultService
from db.db_image_life_service import DBImagesLifeService
from db.db_image_service import DBImageService
from db.db_task_service import DBTaskService
from schedule.schedule_commit_task import task_map
from utils.response import Response

router = APIRouter(
    prefix="/api/fast-build/task",
    tags=["task"],
    responses={404: {"description": "task module error"}}
)


@router.get("/welcome")
async def welcome():
    return {"message": "Welcome To Task Module"}


@router.post("/pull-image")
async def pull_image(image_name: str):
    image_utils = ImageUtils()
    if image_utils.image_exist(image_name):
        print(f"{image_name}已经在系统中存在")
        image_id, image_name = image_utils.get_image_identifier(image_name)
        return Response.success(msg="镜像已经存在在系统中", data={"image_id": image_id, "target_image_name": image_name})
    print(f"拉取镜像{image_name}")
    image_utils.pull_image(image_name, to_stdout=True)

    DBImagesLifeService.save(DBImagesLifeService.get_db_image(image_name))

    image_id, image_name = image_utils.get_image_identifier(image_name)
    return Response.success(msg="镜像拉取成功", data={"image_id": image_id, "target_image_name": image_name})

@router.get("/list-task")
async def list_task(page: int, page_size: int, image_name: str = None, task_status:str = None):
    status, total_count = DBTaskService.query_task_by_per_page(page, page_size, image_name, task_status)
    # 直接查询数据库里的
    image_data = {"page": {"current": page, "total": total_count, "page_size": page_size}, "task_list": status}
    return Response.success(data=image_data)


@router.post("/build-image")
async def build_image(image_request: ImageRequest):
    """
    镜像构建接口，用于根据用户选择的需求配置，生成dockerfile，构建镜像，推送到harbor仓库。
    :param image_request 任务构建请求
    :return:
    """
    #校验镜像的名称/版本是否重复
    name, tag = tuple(image_request.image_data.target_image_name.split(":"))
    if DBImageService.search_image_by_name_tag(name=name, tag=tag):
        return Response.error(f"镜像名 {name}:{tag} 已被使用，请更改名称或版本")

    base_image_name = image_request.dockerfile_json.base_image

    image_utils = ImageUtils()
    if not image_utils.image_exist(base_image_name):
        image_utils.pull_image(base_image_name)
        DBImagesLifeService.save(DBImagesLifeService.get_db_image(base_image_name))

    image = image_utils.get_image(base_image_name)
    record = DBImageCheckResultService.query_result_by_image_id(image.id)

    if record:
        image_descriptor = jsonpickle.loads(record.result)
    else:
        check_result = await check_image(base_image_name)
        if not check_result.is_successful():
            return Response.error(msg=check_result.msg)
        image_descriptor = check_result.data

    # 实例化Task对象，并保存到数据库

    task = Task(image_descriptor, image_request)
    if not task.check_package_source_match():
        file_name = task.dockerfile_json.image_installer_config.package_manager_installer_config.source.file_name
        os = task.image_descriptor.os
        return Response.error(f"镜像操作系统{os.name}:{os.version}版本与配置的包管理源文件名称不匹配: {file_name}")
    DBTaskService.save(task.record)

    task_map[task.task_id] = multiprocessing.Process(target=task.work, args=(), name=f"{task.task_id}")
    #task_map[task.task_id] = threading.Thread(target=task.work, args=(), name=f"{task.task_id}")
    return Response.success(msg=f"为{task.target_image_name}镜像构建任务开启进程，请等待", data=task)


def invalid_version(image_descriptor: ImageDescriptor):
    if image_descriptor.is_ubuntu():
        version = image_descriptor.os.version
        return "18.04" not in version and "20.04" not in version
    if image_descriptor.is_centos():
        version = image_descriptor.os.version
        return "release 7" not in version and "release 8" not in version
    return True


@router.post("/check-image")
async def check_image(image_name: str):
    image_utils = ImageUtils()

    if not image_utils.image_exist(image_name):
        try:
            image_utils.pull_image(image_name)
            DBImagesLifeService.save(DBImagesLifeService.get_db_image(image_name))
        except APIError as error:
            print(f"{image_name}镜像拉取失败，请检查相关的Harbor仓库,msg: {error}")
            return Response.error(msg=f"{image_name}镜像拉取失败，请检查相关的Harbor仓库")

    image = image_utils.get_image(image_name)
    record = DBImageCheckResultService.query_result_by_image_id(image.id)
    if record:
        return Response.success(msg="镜像检测成功", data=jsonpickle.loads(record.result))

    # 检测镜像操作系统内核架构
    if image_utils.invalid_os(image_name):
        return Response.error(msg="镜像系统架构不符，仅支持ubuntu:{18.04,20.04},centos:{7,8}")

    try:
        image_descriptor = image_utils.collect_image_info(image_name)
    except FBException as exception:
        return Response.error(msg=exception.message)

    DBImageCheckResultService.save(image_descriptor.get_db_image_check_result_service())
    return Response.success(msg="镜像检测结果成功", data=image_descriptor)


@router.get("/running-tasks")
async def get_running_tasks():
    print("获取系统正在运行的镜像构建任务")
    tasks = DBTaskService.query_running_tasks()
    return Response.success(msg=f"FastBuild系统中共有{len(tasks)}个镜像构建任务正在运行", data=tasks)


@router.get("/queued-tasks")
async def get_queued_tasks():
    print("获取FastBuild正在排队的镜像构建任务")
    tasks = DBTaskService.query_queued_tasks()
    return Response.success(msg=f"FastBuild系统中共有{len(tasks)}个镜像构建任务正在等待", data=tasks)


@router.get("/task-details_by_task_id")
async def check_task_details_by_task_id(task_id: int):
    task_record = DBTaskService.query_task_by_task_id(task_id)
    if not task_record:
        return Response.error(msg=f"根据任务id{task_id}查询镜像构建任务失败")
    return Response.success(data=task_record)


@router.get("/task-detail-by-image-name")
async def check_task_details_by_image_name(image_name: str):
    """根据镜像名称模糊查询任务构建数据"""
    task_records = DBTaskService.query_tasks_by_image_name(image_name)
    if not task_records:
        return Response.error(msg=f"根据镜像名称{image_name}查询镜像构建任务失败")
    return Response.success(data=task_records)


@router.get("/all-tasks")
async def get_all_tasks():
    """查询所有的镜像构建任务"""
    task_records = DBTaskService.query_all()
    if not task_records:
        return Response.error(msg=f"查询结果为空")
    return Response.success(data=task_records)


@router.delete("/delete-image-by-task-id")
async def delete_image_by_task_id(task_id: int):
    """根据任务id删除镜像"""
    task_record = DBTaskService.query_task_by_task_id(task_id)
    if not task_record:
        return Response.error(msg=f"任务id<{task_id}>任务不存在")
    status = ImageUtils().delete_by_image_name(task_record.target_image_name)
    if status:
        return Response.success(data=status)
    return Response.error(data=status)


@router.delete("/delete-task-by-task-id")
async def delete_task_by_task_id(task_id: int):
    """根据任务id删除镜像和作业目录"""
    task_record = DBTaskService.query_task_by_task_id(task_id)
    if not task_record:
        return Response.error(msg=f"任务id<{task_id}>任务不存在")
    # 校验任务终态
    if task_record.state not in "BUILD_FAILED , PUSH_SUCCESS , PUSH_FAILED , BUILD_ABORT":
        return Response.error(msg=f"任务id<{task_id}>任务仍在进行，无法删除")

    DBTaskService.del_task(task_record)
    if delete_task(task_record):
        return Response.success(data="Folder deleted successfully")
    return Response.error(data="Failed to delete folder or folder does not exist")
