#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/9/5 10:40
@desc: 实现FastBuild异常类
"""


class FBException(Exception):

    def __init__(self, message, *args: object) -> None:
        self.message = message
        super().__init__(*args)
