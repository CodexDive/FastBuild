#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/24 10:02
@desc: 用于描述数据库相关配置
"""


class DBConfig:
    def __init__(self, db_file: str):
        super().__init__()
        self._db_file = db_file

    def get_db_file(self):
        return self._db_file
