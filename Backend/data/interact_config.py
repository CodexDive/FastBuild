#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/3/10 16:07
@desc: 交互配置
"""
from pydantic import BaseModel


class InteractConfig(BaseModel):
    config_open: bool = True
    password: str = "Alkaid123456"
