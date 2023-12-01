#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/24 11:10
@desc: 该类用于实现镜像构建任务记录的管理
"""

from db.db_element import Session
from db.db_image import DBImage
from sqlalchemy import or_

class DBImageService:
    """镜像构建任务存储服务"""

    @staticmethod
    def query_all() -> list:
        with Session() as session:
            return session.query(DBImage).all()

    @staticmethod
    def query_image_by_per_page(page: int, page_size: int, keyword: str, image_type: str):
        # 计算起始索引和结束索引
        start_index = (page - 1) * page_size
        # end_index = start_index + per_page
        with Session() as session:
            db_image = session.query(DBImage).order_by(DBImage.create_time.desc())
            total_count = db_image.count()
            if keyword:
                db_image = db_image.filter(or_(DBImage.tag.ilike(f'%{keyword}%'), DBImage.name.ilike(f'%{keyword}%')))
                total_count = db_image.count()
            if image_type:
                db_image = db_image.filter(DBImage.type == image_type)
                total_count = db_image.count()
            return db_image.offset(start_index).limit(page_size).all(), total_count

    @staticmethod
    def save(record: DBImage) -> DBImage:
        """新增或者更新一组镜像信息"""
        with Session() as session:
            session.add(record)
            session.commit()
        return record

    @staticmethod
    def del_image(name: str, tag: str):
        """删除镜像"""
        with Session() as session:
            record = session.query(DBImage).filter(DBImage.name == name, DBImage.tag == tag).first()
            if record:
                session.delete(record)
                session.commit()
                return 'Image deleted successfully'
            else:
                return 'Image not found'

    @staticmethod
    def search_image_by_name_tag(name: str, tag: str) -> list:
        with Session() as session:
            return session.query(DBImage).filter(DBImage.name == name, DBImage.tag == tag).all()