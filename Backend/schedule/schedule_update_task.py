#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/8/22 15:37
@desc: 定时维护任务状态
"""

from data.image_state import ImageState
from data.task import log
from db.db_task_service import DBTaskService
from schedule.schedule_commit_task import task_map


def update_image_task_state():
    release_end_task_resource()
    release_problem_task_resource()


def release_problem_task_resource():
    # 查找系统中数据库中正在运行的镜像构建任务,进程已start
    running_tasks = DBTaskService.query_running_tasks()

    for task in running_tasks:
        if task.task_id not in task_map:
            # 数据库中的任务找不到对应的进程，表明系统崩溃
            log.info(f"此刻FastBuild数据库中正在运行的构建任务id: {task.task_id}, 但FastBuild系统中找不到对应的进程，"
                     f"强制将任务ID:{task.task_id}从状态:{task.state}更新至{ImageState.BUILD_ABORT.value}")
            DBTaskService.update_task_to_abort(task)
            continue

        build_process = task_map[task.task_id]
        if build_process.is_alive():
            continue

        current_task = None
        if not build_process.is_alive():
            # 任务对应的线程已经不再运行了，此时状态应该处于终止状态
            current_task = DBTaskService.query_task_by_task_id(task.task_id)
            if current_task.state in ImageState.normal_end_states():
                continue
        """
        build_thread = task_map[task.task_id]
        if build_thread.is_alive():
            continue

        current_task = None
        if not build_thread.is_alive():
            # 任务对应的线程已经不再运行了，此时状态应该处于终止状态
            current_task = DBTaskService.query_task_by_task_id(task.task_id)
            if current_task.state in ImageState.normal_end_states():
                continue
        """
        log.info(f"数据库处于运行状态的任务: {task.name}, 镜像构建任务构建进程{build_process.name}已经不处于运行状态,"
                 f"强制将任务ID:{task.task_id}从状态:{current_task.state}更新至{ImageState.BUILD_ABORT.value}")
        DBTaskService.update_task_to_abort(task)

def release_end_task_resource():
    task_ids = list(task_map.keys())
    if not task_ids: return
    tasks = DBTaskService.query_tasks_by_task_ids(task_ids)
    task_id_to_release = [task.task_id for task in tasks if task_end_and_process_not_alive(task)]
    #task_id_to_release = [task.task_id for task in tasks if task_end_and_thread_not_alive(task)]
    if len(task_id_to_release) > 0:
        log.info(f"从内存中从task_map中移除出{len(task_id_to_release)}个构建进程对象")
    for task_id in task_id_to_release:
        process = task_map.pop(task_id)
        log.info(f"从内存中删除{task_id}对应的进程对象:{process.name}")
        """
        thread = task_map.pop(task_id)
        log.info(f"从内存中删除{task_id}对应的线程对象:{thread.name}")
        """

def task_end_and_process_not_alive(task):
    return task.state in ImageState.end_states() and not task_map[task.task_id].is_alive()

"""
def task_end_and_thread_not_alive(task):
    return task.state in ImageState.end_states() and not task_map[task.task_id].is_alive()
"""

