#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/14 16:28
@desc: 用于文件的拷贝
"""
import shutil


def copy2(source: str, destination: str):
    """
    将配置文件拷贝到工作目录,同时修改容器中的文件名称
    注意，destination是文件路径，如果是一个目录，会报错
    :param source: 文件路径，待拷贝的文件
    :param destination: 拷贝到目标文件
    """
    # adding exception handling
    try:
        shutil.copyfile(source, destination)
    except IOError as e:
        print("Unable to copy file. %s" % e)
