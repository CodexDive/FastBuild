#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/3 11:08
@desc: ubuntu制品，用于检测容器所依赖的ubuntu版本等信息
"""
from data.artifact.artifact import Artifact


class UbuntuArtifact(Artifact):
    def __init__(self, version: str) -> None:
        super().__init__("Ubuntu", True, version)

