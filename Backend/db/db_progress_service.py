#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/8/18 11:20
@desc: 
"""
import datetime
from typing import List

from db.db_element import Session
from db.db_progress import DBProgress


class DBProgressService:
    """镜像构建任务进度服务"""

    @staticmethod
    def query_all() -> list:
        with Session() as session:
            return session.query(DBProgress).all()

    @staticmethod
    def query_progresses_by_task_id(task_id: int) -> List[DBProgress]:
        with Session() as session:
            return session.query(DBProgress) \
                .filter(DBProgress.task_id == task_id) \
                .order_by(DBProgress.start_time) \
                .all()

    @staticmethod
    def save(progress: DBProgress) -> DBProgress:
        """新增或者更新一组集群信息"""
        with Session() as session:
            session.add(progress)
            session.commit()
        return progress


if __name__ == '__main__':
    progress = DBProgress()
    progress.action = "pull"
    progress.task_id = 1233
    progress.duration = 234
    progress.start_time = datetime.datetime.now()
    progress.end_time = datetime.datetime.now()
    progress.log_path = "pull.log"
    progress.log_url = "http://pull.log"
    progress.status = "success"
    DBProgressService.save(progress)

    print(DBProgressService.query_progresses_by_task_id(1233))

    progress1 = DBProgress()
    progress1.action = "check"
    progress1.task_id = 1233
    progress1.duration = 234
    progress1.start_time = datetime.datetime.now()
    progress1.end_time = datetime.datetime.now()
    progress1.log_path = "pull.log"
    progress1.log_url = "http://pull.log"
    progress1.status = "success"
    DBProgressService.save(progress1)
    DBProgressService.query_progresses_by_task_id(1233)
    print(DBProgressService.query_progresses_by_task_id(1233))
