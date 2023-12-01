#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: meizhewei
@email:
@time: 2023/8/18 9:59
@desc: 用于镜像定期清理的数据库表
"""
from datetime import datetime, timedelta
from typing import List

from sqlalchemy import and_

from db.db_element import Session
from db.db_image_life import DBImageLife


class DBImagesLifeService:
    """镜像生命周期记录存储服务"""

    @staticmethod
    def query_all() -> list:
        with Session() as session:
            return session.query(DBImageLife) \
                .order_by(DBImageLife.generator_time.desc()) \
                .all()

    @staticmethod
    def query_image_by_generate_time_before_days(reserved_days) -> List[DBImageLife]:
        target_datetime = get_datetime_before(reserved_days)
        return DBImagesLifeService.query_image_life_by_generate_time_before_datetime(target_datetime)

    @staticmethod
    def query_image_life_by_generate_time_before_datetime(target_datetime) -> List[DBImageLife]:
        with Session() as session:
            return session.query(DBImageLife) \
                .filter(and_(DBImageLife.generator_time < target_datetime, DBImageLife.delete_time.is_(None))) \
                .all()

    @staticmethod
    def query_image_life_by_image_name(image_name: str) -> DBImageLife:
        with Session() as session:
            return session.query(DBImageLife) \
                .filter(DBImageLife.image_name == image_name) \
                .order_by(DBImageLife.generator_time.desc()) \
                .first()

    @staticmethod
    def save(record: DBImageLife) -> DBImageLife:
        """新增或者更新一组集群信息"""
        with Session() as session:
            session.add(record)
            session.commit()
        return record

    @staticmethod
    def save_batch(records: List[DBImageLife]):
        with Session() as session:
            session.add_all(records)
            session.commit()

    @staticmethod
    def update_images_delete_time(delete_images: List[DBImageLife]):
        now = datetime.now()
        for image in delete_images:
            image.delete_time = now
        DBImagesLifeService.save_batch(delete_images)

    @staticmethod
    def modify(image_id, delete_time):
        """新增或者更新一组集群信息"""
        with Session() as session:
            image_record: DBImageLife = session.query(DBImageLife).filter(DBImageLife.image_id == image_id).first()
            image_record.delete_time = delete_time
            session.commit()

    @staticmethod
    def get_db_image(image_name, image_type="pull") -> DBImageLife:
        record = DBImageLife(
            image_name=image_name,
            image_type=image_type,
            generator_time=datetime.now(),
            create_time=datetime.now()
        )
        return record


def get_datetime_before(reserve_days):
    return datetime.now() - timedelta(days=reserve_days)
