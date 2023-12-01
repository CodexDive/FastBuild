#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/3 11:20
@desc: 用于表示在镜像容器中检测出的apt制品信息
"""
from data.artifact import Artifact


class AptArtifact(Artifact):
    source: str = ""

    def __init__(self, version: str, source) -> None:
        self.source = source
        super().__init__("apt", True if version else False, version)
