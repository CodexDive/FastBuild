#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/3 11:15
@desc: 
"""
from typing import List

from data.artifact.artifact import Artifact


class PipArtifact(Artifact):
    source = []
    version: List[str]

    def __init__(self, version, source: List) -> None:
        self.source = source
        super().__init__("pip", True if version else False, version)
