#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/1/4 10:19
@desc: 页面传递的dockerfile_json字符串,用来生成json文件
"""

from pydantic import BaseModel

from data.install.image_installer_config import ImageInstallerConfig


class DockerfileJson(BaseModel):
    """DockerfileJson配置文件映射类"""
    base_image: str
    maintainer: str

    class Config:
        arbitrary_types_allowed = True

    # 安装器信息， 主要包括apt、yum、conda
    image_installer_config: ImageInstallerConfig
