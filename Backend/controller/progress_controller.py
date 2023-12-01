#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/8/18 13:48
@desc: 用于查询任务进度
"""

from fastapi import APIRouter

from data.progress_status import ProgressStatus
from db.db_progress_service import DBProgressService
from db.db_task_service import DBTaskService
from utils.config_utils import host_config
from utils.response import Response

router = APIRouter(
    prefix="/api/fast-build/progress",
    tags=["progress"],
    responses={404: {"description": "progress module error"}}
)


@router.get("/welcome")
async def welcome():
    return {"message": "Welcome To Progress Module"}


@router.get("/details")
async def task_progresses_by_task_id(task_id: int):
    task = DBTaskService.query_task_by_task_id(task_id)
    if not task:
        return Response.success(data={})
    progresses = DBProgressService.query_progresses_by_task_id(task_id)
    add_dockerfile(progresses, task)
    result = {"task_id": task_id, "task_name": task.name, "progress": progresses}
    return Response.success(data=result)


def add_dockerfile(progresses, task):
    for progress in progresses:
        if progress.action not in [ProgressStatus.BUILD.value, ProgressStatus.PREPARE.value]:
            continue
        progress.dockerfile_path = task.dockerfile_path
        progress.dockerfile_url = get_dockerfile_url(task)


def get_dockerfile_url(task):
    return host_config.get_static_resource_prefix() + task.work_dir_name + "/Dockerfile"


@router.get("/running-tasks-progress")
async def running_tasks_progress():
    tasks = DBTaskService.query_running_tasks()
    result = {}
    for task in tasks:
        progresses = DBProgressService.query_progresses_by_task_id(task.task_id)
        result[task.task_id] = progresses
    return Response.success(msg=f"共有{len(tasks)}个正在运行的镜像构建任务", data=result)


@router.get("/status")
async def progress_status():
    return Response.success(data=[status for status in ProgressStatus])
