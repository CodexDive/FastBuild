#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@file: yml_utils.py
@time: 2022/12/14 15:35
@desc: 用于解析yml文件，获取不同操作系统下的依赖环境
"""
import os.path
from typing import List

import yaml

# 注，该方案已经遗弃了。
source_file_path = "config"


def get_sources(os_str: str, version: str, source_name: str):
    """
    根据
    :param os_str:
    :param version:
    :param source_name:
    :return:
    """
    source_dict = get_source_dict(os_str, version)
    return get_sources_with_name(source_dict, source_name)


def get_sources_with_name(source_dict, name: str) -> List[str]:
    if name not in source_dict:
        raise Exception(f"在source_dict中不存在名称为{name}的源")
    return source_dict[name]


def centos_yml_path():
    """centos的source源配置文件"""
    return os.path.join(source_file_path, "centos.yml")


def ubuntu_yml_path():
    """ubuntu的source源配置文件路径"""
    os.system("pwd")
    return os.path.join(source_file_path, "ubuntu.yml")


def get_source_path(os_str: str) -> str:
    """
    根据操作系统为ubuntu或者centos获取配置文件的位置
    :param os_str:
    :return:
    """
    if os_str.lower() == "ubuntu":
        return ubuntu_yml_path()
    elif os_str.lower() == "centos":
        return centos_yml_path()
    else:
        raise Exception("不支持的操作系统: %s" % os_str)


def get_source_dict(os_str, version: str) -> dict:
    """
    根据操作系统名称和版本获取源的配置信息
    :param os_str: ubuntu或者centos
    :param version: 对于ubuntu而言，16.04,18.04,20.04，对于centos而言7
    :return:
    """
    file = open(get_source_path(os_str), 'r', encoding='utf-8')
    result = yaml.load_all(file.read(), Loader=yaml.FullLoader)
    for document in result:
        if version not in document:
            continue
        return document[version]
    raise Exception("不支持的系统版本%s:%s" % (os_str, version))


if __name__ == '__main__':
    print(get_sources("centos", "18.04", "ali"))
    print(get_sources("ubuntu", "18.04", "ali"))