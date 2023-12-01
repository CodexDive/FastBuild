#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/1/4 10:24
@desc: 使用apt、yum、conda、pip安装的软件信息
"""

from pydantic import BaseModel


class Software(BaseModel):
    name: str
    version: str = ""

    def get_full_name(self):
        return self.name + self.version

    def get_name_with_delimiter(self, delimiter: str) -> str:
        if len(self.version) == 0:
            return self.name
        return self.name + delimiter + self.version
