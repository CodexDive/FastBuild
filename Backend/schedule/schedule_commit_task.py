#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/8/23 14:57
@desc: 定时启动镜像构建任务
"""
import threading
from threading import Thread
from multiprocessing import Process
from typing import Dict

from data.image_state import ImageState
from data.task import log
from db.db_task_service import DBTaskService

task_map: Dict[int, Process] = {}
#task_map: Dict[int, Thread] = {}

# 创建锁对象
lock = threading.Lock()


def commit_image_build_task():
    if not task_map:
        # 表示无待处理的镜像构建任务
        return

    available_task_count = get_available_image_build_task_count()
    start_image_build_task(available_task_count)


def start_image_build_task(available_task_count):
    queue_tasks = DBTaskService.query_queued_tasks()
    print("---------------------------------------------")
    print("当前等待构建任务：", queue_tasks)
    if len(queue_tasks) > 0:
        log.info(f"FastBuild数据库中有{len(queue_tasks)}待处理, 此刻可再提供{available_task_count}构建进程")
    print("当前可用构建数量：", available_task_count)
    for i in range(available_task_count):
        if i >= len(queue_tasks):
            break
        task = queue_tasks[i]
        if task.task_id not in task_map:
            log.info(f"数据库中存在未启动的任务{task.name}，但系统无相应的进程，更新构建任务崩溃"
                     f"强制将任务ID:{task.task_id}从状态:{task.state}更新至{ImageState.BUILD_ABORT.value}")
            DBTaskService.update_task_to_abort(task)
            continue
        process = task_map[task.task_id]
        if process.is_alive():
            log.info("something is impossible")
            raise Exception(
                f"something is impossible， in DB {task.task_id} is queue, but corresponding process has started")
            # 获取锁
        lock.acquire()

        process.start()
        task.pid = process.pid
        task.state = ImageState.STARTED.value
        log.info(f"启动任务，id: {task.task_id}，任务进程号:{task.pid}，将数据库中状态置为{ImageState.STARTED.value}")
        DBTaskService.save(task)

        lock.release()
        """
        thread = task_map[task.task_id]
        if thread.is_alive():
            log.info("something is impossible")
            raise Exception(
                f"something is impossible， in DB {task.task_id} is queue, but corresponding thread has started")
        # 获取锁
        lock.acquire()

        DBTaskService.update_task_state(task.task_id, ImageState.STARTED.value)
        thread.start()

        log.info(f"启动任务，id: {task.task_id}，将数据库中状态置为{ImageState.STARTED.value}")
        lock.release()
        """

def get_available_image_build_task_count():
    """FastBuild系统仅仅允许同时构建五个镜像"""
    return max(5 - len(DBTaskService.query_running_tasks()), 0)
