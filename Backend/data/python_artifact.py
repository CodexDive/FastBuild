#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/3 14:09
@desc: 用以描写容器中的python环境
"""
import re
from typing import List

from data.artifact import Artifact
from data.fb_exception import FBException


class PythonArtifact(Artifact):
    version: List[str]

    def __init__(self, version: List[str]) -> None:
        super().__init__("python", True if version else False, version)

    def has_python3(self):
        has_python3 = False
        for python_ver in self.version:
            if contains_python3_str(python_ver):
                has_python3 = True
        return has_python3

    def get_python3_command(self):
        # 获取版本中对应python3的命令
        if not self.has_python3():
            raise FBException("系统中不包含python3相关指令")
        for python_ver in self.version:
            if not contains_python3_str(python_ver):
                continue
            return python_ver.split("(")[0]

    def get_python3_version_tuple(self):
        if not self.has_python3():
            raise FBException("系统中不包含python3相关指令")
        for python_ver in self.version:
            if not contains_python3_str(python_ver):
                continue
                # Python2(Python 2.7.17)
            return tuple(re.findall(r'\d+', python_ver.split("(")[1]))


def contains_python3_str(python_ver):
    return "python 3" in python_ver.lower()
