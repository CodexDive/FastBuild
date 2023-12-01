#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/24 9:59
@desc: 用于映射镜像构建任务的数据库表
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from db.db_element import Base


class DBImage(Base):
    """表示运行作业表，其对应slurm中正在运行的作业"""
    __tablename__ = 'fb_image_table'

    primary_id = Column(Integer, primary_key=True)

    """关联的构建任务id，程序生成，唯一"""
    task_id = Column(Integer)

    """记录创建时间"""
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    """更新时间"""
    update_time = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now, comment="修改时间")

    """镜像名称 """
    name = Column(String, nullable=False)
    """镜像标签 """
    tag = Column(String)
    """镜像id"""
    id = Column(String, nullable=False)
    """镜像类型:base/customized"""
    type = Column(String)
    """镜像描述"""
    description = Column(String)
    """镜像大小"""
    size = Column(String)
    """镜像交互"""
    interaction = Column(String)

    def __repr__(self):
        return f"<DBTask(primary_id={self.primary_id}, task_id={self.task_id}, name={self.name}))>"