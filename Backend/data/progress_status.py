#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/8/18 14:38
@desc: 描述镜像构建进度
"""
from enum import Enum


class ProgressStatus(Enum):
    PULL = "pull"
    CHECK = "check"
    PREPARE = "prepare"
    BUILD = "build"
    PUSH = "push"
