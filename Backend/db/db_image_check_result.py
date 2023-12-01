#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/3/2 10:19
@desc: 用于保存镜像检测结果
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from db.db_element import Base


class DBImageCheckResult(Base):
    """镜像检测的结果"""
    __tablename__ = 'fb_image_check_result_table'
    primary_id = Column(Integer, primary_key=True)
    """镜像id"""
    image_id = Column(String)
    """镜像名称"""
    image_name = Column(String, nullable=False)

    result = Column(String, nullable=False)
    """记录创建时间"""
    create_time = Column(DateTime, nullable=False, default=datetime.now())
    """更新时间"""
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now(), comment="更新时间")

    def __repr__(self):
        return f"<DBImageCheckResult(image_id={self.image_id}, image_name={self.image_name}, result={self.result}))>"
