#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/1/4 10:16
@desc: 用于接收页面的请求
"""
from pydantic import BaseModel


class ImageDataRequest(BaseModel):
    """
    用户构建镜像任务的信息
    """
    task_name: str
    callback_url: str
    target_image_name: str
    image_desc: str
    webSSHSecret: str
    jupyterLabSecret: str