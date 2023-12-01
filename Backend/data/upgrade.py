#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/8 11:09
@desc: 软件升级，用于建模一个软件的变化，从之前的版本升级到目标版本
"""
from typing import Union

from pydantic import BaseModel


class Upgrade(BaseModel):
    """
    升级类，用于表征一个软件从之前的版本升级到另外一个版本。
    """

    # 镜像中指定软件的当前版本信息
    present: Union[list, str] = ""
    # 如果需要升级，则target指示了升级的安装包文件名称
    target: Union[list, str] = ""
    # 安装器安装位置
    install_loc = ""
    # 是否升级，如果不修改当前软件，则update为False
    if target:
        update: bool = True
    else:
        update: bool = False
    @classmethod
    def get_default_upgrade(cls):
        return cls()
