#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/3 11:03
@desc: 操作系统，诸如Ubuntu和Centos
"""
from data.artifact.artifact import Artifact


class CentosArtifact(Artifact):
    def __init__(self, version: str) -> None:
        super().__init__("Centos", True, version)

