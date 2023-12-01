#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/3 11:22
@desc: 用于表示在容器中检测的yum制品信息，仅在Centos镜像中有效
"""
from data.artifact import Artifact


class YumArtifact(Artifact):
    source = []

    def __init__(self, version: str, source) -> None:
        self.source = source
        super().__init__("yum", True, version)
