#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/3/16 10:02
@desc: 用于描述镜像启动的容器中jupyterlab服务是否启动
"""
from data.artifact.artifact import Artifact


class JupyterLabArtifact(Artifact):
    def __init__(self, available: bool, version: str = "") -> None:
        super().__init__("jupyterlab", available, version)
