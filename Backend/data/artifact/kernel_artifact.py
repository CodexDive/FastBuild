#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/3 10:51
@desc: 内核制品，用于检查镜像内部的内核版本
"""
from data.artifact.artifact import Artifact


class KernelArtifact(Artifact):
    def __init__(self, version: str) -> None:
        super().__init__("Linux", True, version)


