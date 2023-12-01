#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/3 11:16
@desc: 用于表示在容器中检查到的conda制品信息
"""
from typing import List

from data.artifact import Artifact


class CondaArtifact(Artifact):
    source = []

    def __init__(self, version: str, environments: List[str], source: List[str]) -> None:
        # 检测的系统conda环境列表
        self.source = source
        self.environments = environments
        super().__init__("conda", True if version else False, version)

    def set_environments(self, environemnts: List[str]):
        self.environments = environemnts
