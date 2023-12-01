#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/24 11:10
@desc: 该类用于实现镜像构建任务记录的管理
"""
from typing import List

from data.image_state import ImageState
from db.db_element import Session
from db.db_task import DBTask


class DBTaskService:
    """镜像构建任务存储服务"""

    @staticmethod
    def query_all() -> list:
        with Session() as session:
            return session.query(DBTask).all()

    @staticmethod
    def query_task_by_per_page(page: int, page_size: int, image_name: str, task_status: str):
        # 计算起始索引和结束索引
        start_index = (page - 1) * page_size
        # end_index = start_index + per_page
        with Session() as session:
            db_image = session.query(DBTask).order_by(DBTask.create_time.desc())
            total_count = db_image.count()
            if image_name:
                db_image = db_image.filter(DBTask.target_image_name.ilike(f'%{image_name}%'))
                total_count = db_image.count()
            if task_status:
                db_image = db_image.filter(DBTask.state.ilike(f'%{task_status}%'))
                total_count = db_image.count()
            return db_image.offset(start_index).limit(page_size).all(), total_count


    @staticmethod
    def query_task_by_task_id(task_id: int) -> DBTask:
        with Session() as session:
            return session.query(DBTask) \
                .filter(DBTask.task_id == task_id) \
                .first()

    @staticmethod
    def query_tasks_by_task_ids(task_ids: List[int]) -> List[DBTask]:
        with Session() as session:
            return session.query(DBTask) \
                .filter(DBTask.task_id.in_(task_ids)) \
                .all()

    @staticmethod
    def query_tasks_by_image_name(image_name: str) -> List[DBTask]:
        with Session() as session:
            return session.query(DBTask) \
                .filter(DBTask.target_image_name.like(f"%{image_name}%")) \
                .all()

    @staticmethod
    def save(record: DBTask) -> DBTask:
        """新增或者更新一组集群信息"""
        with Session() as session:
            session.add(record)
            session.commit()
        return record


    @staticmethod
    def del_task(task_record: DBTask):
        """删除镜像构建任务信息"""
        with Session() as session:
            session.delete(task_record)
            session.commit()
        return 'Image deleted successfully'


    @staticmethod
    def update_task_to_abort(record: DBTask):
        DBTaskService.update_task_state(record.task_id, ImageState.BUILD_ABORT.value)

    @staticmethod
    def query_running_tasks() -> List[DBTask]:
        with Session() as session:
            return session.query(DBTask) \
                .filter(DBTask.state.in_(ImageState.running_states())) \
                .all()

    @staticmethod
    def query_queued_tasks() -> List[DBTask]:
        """检索正在排队的镜像构建任务"""
        with Session() as session:
            return session.query(DBTask) \
                .filter(DBTask.state == ImageState.queue_state()) \
                .all()

    @staticmethod
    def update_task_state(task_id: int, state: str):
        with Session() as session:
            task_record: DBTask = session.query(DBTask).filter(DBTask.task_id == task_id).first()
            task_record.state = state
            session.commit()

    @staticmethod
    def get_tasks_by_create_time_before(target_datetime):
        with Session() as session:
            return session.query(DBTask) \
                .filter(DBTask.create_time > target_datetime) \
                .all()

    @staticmethod
    def query_latest_task_by_image_name(image_name: str) -> DBTask:
        with Session() as session:
            return session.query(DBTask) \
                .filter(DBTask.base_image_name == image_name) \
                .order_by(DBTask.create_time.desc()) \
                .first()
