#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/8/18 11:09
@desc: 
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from db.db_element import Base


class DBProgress(Base):
    """表示镜像构建任务进度表"""
    __tablename__ = 'fb_progress_table'

    primary_id = Column(Integer, primary_key=True)
    """任务id，程序生成唯一"""
    task_id = Column(Integer, nullable=False)
    """任务名称"""
    task_name = Column(String)

    """记录创建时间"""
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    """更新时间"""
    update_time = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now, comment="修改时间")
    """任务构建进度对应的动作"""
    action = Column(String, nullable=False)
    status = Column(String, nullable=False)
    """目标镜像构建名称"""
    target_image_name = Column(String)
    """基础镜像名称"""
    base_image_name = Column(String)
    """过程开始时间"""
    start_time = Column(DateTime, nullable=False)
    """过程结束时间"""
    end_time = Column(DateTime, nullable=False)
    """该过程所经历的毫秒数"""
    duration = Column(Integer)
    """该过程产生的日志文件"""
    log_path = Column(String, nullable=False)
    """日志文件对应的url"""
    log_url = Column(String, nullable=False)

    def __repr__(self):
        return f"<DBProgress(primary_id={self.primary_id}, task_id={self.task_id}, action={self.action})>"
