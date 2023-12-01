#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/3/2 13:55
@desc: 用于存取镜像检测结果
"""

from db.db_element import Session
from db.db_image_check_result import DBImageCheckResult


class DBImageCheckResultService:
    """镜像检测结果存储服务，用于进行镜像检测结果的存取"""

    @staticmethod
    def query_all() -> list:
        with Session() as session:
            return session.query(DBImageCheckResult).all()

    @staticmethod
    def save(result: DBImageCheckResult) -> DBImageCheckResult:
        """新增或者更新一组集群信息"""
        with Session() as session:
            session.add(result)
            session.commit()
        return result

    @staticmethod
    def delete_all():
        with Session() as session:
            session.query(DBImageCheckResult).delete()
            session.commit()

    @staticmethod
    def query_result_by_image_id(image_id: str) -> DBImageCheckResult:
        with Session() as session:
            return session.query(DBImageCheckResult) \
                .filter(DBImageCheckResult.image_id == image_id) \
                .first()
