#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/8 11:22
@desc: 用于建模镜像重要的环境变化，当前仅包括python
"""

from pydantic import BaseModel

from data.install.upgrade import Upgrade


class EnvironmentChange(BaseModel):
    """
    建模镜像重要的环境变化
    """
    python_env_change: Upgrade


