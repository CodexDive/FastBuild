#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/3 10:48
@desc: Artifact为镜像内制品检测而构建的基类，主要用于获取镜像中的基础信息
"""


class Artifact:
    name: str
    available: bool

    def __init__(self, name: str, available: bool, version) -> None:
        self.name = name
        self.available = available
        self.version = version
        super().__init__()
