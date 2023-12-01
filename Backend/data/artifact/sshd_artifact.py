#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/3/16 9:30
@desc: 用于描述镜像启动的容器中是否有sshd服务
"""
from data.artifact.artifact import Artifact


class SshdArtifact(Artifact):
    def __init__(self, available: bool, version: str = "") -> None:
        super().__init__("sshd", available, version)