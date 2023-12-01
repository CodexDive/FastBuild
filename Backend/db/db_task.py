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


class DBTask(Base):
    """表示运行作业表，其对应slurm中正在运行的作业"""
    __tablename__ = 'fb_task_table'

    primary_id = Column(Integer, primary_key=True)
    """任务id，程序生成唯一"""
    task_id = Column(Integer, nullable=False)
    """任务名称"""
    name = Column(String)

    """记录创建时间"""
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    """更新时间"""
    update_time = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now, comment="修改时间")
    """镜像构建任务的请求信息"""
    request = Column(String)
    """镜像构建状态，构建中，成功，失败"""
    state = Column(String, nullable=False)
    """基础镜像名称"""
    base_image_name = Column(String, nullable=False)
    """镜像构建名称 """
    # 历史原因，image_name也放在了代码中
    image_name = Column(String, nullable=False)
    target_image_name = Column(String, nullable=False)
    # 镜像描述
    description = Column(String)
    """构建任务所在目录"""
    task_work_dir = Column(String)
    """dockerfile路径"""
    dockerfile_path = Column(String)
    """镜像构建日志文件路径，位于dockerfile_dir目录下"""
    image_build_log_path = Column(String)
    work_dir_name = Column(String, nullable=False)
    """回调函数url"""
    callback_url = Column(String)
    """回调次数"""
    callback_times = Column(String)
    """构建进程ID"""
    pid = Column(String)

    def __repr__(self):
        return f"<DBTask(primary_id={self.primary_id}, task_id={self.task_id}, name={self.name}, state={self.state}))>"