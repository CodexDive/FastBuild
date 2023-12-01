#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Filename :scheduler.py
@Description :
@Datetime :2022/10/08 16:05:52
@Author :yangqinglin
@email :yangqinglin@zhejianglab.com
"""
import threading
from functools import partial
from pathlib import Path

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler

from utils.log import Log

__all__ = ["Scheduler"]


class _AsyncScheduler:
    __instance_lock = threading.Lock()
    sqlite = "sqlite:///" + str(Path(__file__).parent.parent / "data/jobs.db")
    __interval_task = {
            # 配置存储器
            "jobstores": {
                'default': SQLAlchemyJobStore(url=sqlite)
            },
            # 配置执行器
            "executors": {
                'default': ThreadPoolExecutor(20),
                'processpool': ProcessPoolExecutor(5)
            },
            # 创建job时的默认参数
            "job_defaults": {
                'coalesce': True,  # 是否合并执行
                'max_instances': 5,  # 最大实例数
            }

        }

    asyncscheduler = None

    @staticmethod
    def job_listener(Event, logger, scheduler):
        job = scheduler.get_job(Event.job_id)
        if not Event.exception:
            logger.info(
                f"jobname={job.name};jobid={Event.job_id}|jobtrigger={job.trigger}|jobtime={Event.scheduled_run_time}|retval={Event.retval}")

        else:
            print(f"{Event.job_id}:任务出错了！！！！！")
            logger.error(
                "jobname={job.name}|jobtrigger={job.trigger}|errcode={Event.code}|exception=[{Event.exception}]|traceback=[{Event.traceback}]|scheduled_time={Event.scheduled_run_time}")

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls.__instance_lock:
                logger = Log.ulog()
                cls.asyncscheduler = AsyncIOScheduler(**cls.__interval_task)
                job_listener = partial(cls.job_listener,
                            logger=logger, scheduler=cls.asyncscheduler)
                cls.asyncscheduler.add_listener(job_listener, EVENT_JOB_ERROR |
                                        EVENT_JOB_MISSED | EVENT_JOB_EXECUTED)
                cls.asyncscheduler._logger = logger
                cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class Scheduler:
    @classmethod
    def AsyncScheduler(cls):
        return _AsyncScheduler().asyncscheduler

    @classmethod
    def BackgroundScheduler(cls):
        scheduler = BackgroundScheduler(**cls.__interval_task)
        return scheduler

