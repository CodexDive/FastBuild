#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@file: schedule_service.py
@time: 2022/11/3 15:42
@desc:
"""
from schedule.schedule_clean_image import auto_clean_all
from schedule.schedule_commit_task import commit_image_build_task
from schedule.schedule_update_task import update_image_task_state
from utils.scheduler import Scheduler

scheduler = Scheduler.AsyncScheduler()


def add_schedule_service():
    """
    为FastBuild添加定时调度服务，为时间配置做准备
    """
    add_schedule_update_task(60)
    add_schedule_commit_task(5)
    add_schedule_free_space(100)


def add_schedule_update_task(interval: int):
    """添加定时单条数据扫描程序"""
    print("Enter add_schedule_update_task")
    scheduler.add_job(update_image_task_state, args=[], id=f"schedule_update_task_thread",
                      trigger="interval", seconds=interval, replace_existing=True)


def add_schedule_commit_task(interval: int):
    """添加定时单条数据扫描程序"""
    print("Enter add_schedule_commit_task")
    scheduler.add_job(commit_image_build_task, args=[], id=f"commit_image_build_task",
                      trigger="interval", seconds=interval, replace_existing=True)


def add_schedule_free_space(interval: int):
    """添加自动清理扫描程序"""
    print("Enter add_schedule_free_space")
    scheduler.add_job(auto_clean_all, args=[], id=f"add_schedule_free_space",
                      trigger="interval", seconds=interval, replace_existing=True)
