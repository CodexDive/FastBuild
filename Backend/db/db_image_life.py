#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: meizhewei
@email:
@time: 2023/8/18 9:59
@desc: 用于镜像定期清理的数据库表
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from db.db_element import Base


class DBImageLife(Base):
    """表示镜像生命周期表"""
    __tablename__ = 'fb_image_life_table'

    primary_id = Column(Integer, primary_key=True)
    """镜像构建名称"""
    image_name = Column(String, nullable=False)
    """镜像构建方式-拉取镜像/构建镜像"""
    image_type = Column(String, nullable=False, default="pull")
    """镜像拉取/生成时间"""
    generator_time = Column(DateTime, nullable=False)
    """镜像删除时间"""
    delete_time = Column(DateTime)
    """记录创建时间"""
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    """更新时间"""
    update_time = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now, comment="修改时间")

    def __repr__(self):
        return f"<DBImageLife(primary_id={self.primary_id}, image_name={self.image_name}, image_type={self.image_type}, generator_time={self.generator_time}, delete_time={self.delete_time}))>"
