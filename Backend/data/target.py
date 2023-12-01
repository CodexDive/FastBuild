#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/1/3 15:36
@desc: 映射镜像安装的配置文件类
"""


class Target:
    """
    映射了用户要安装的依赖所表示的配置文件
    """
    def __init__(self, dockerfile_dict):
        self.base_image = dockerfile_dict.base_image
        self.maintainer = dockerfile_dict.maintainer
        self.os = dockerfile_dict.os
        self.os_version = dockerfile_dict.os_version
        self.user = dockerfile_dict.user
        self.toolkit = dockerfile_dict.toolkit
        self.apt = dockerfile_dict.apt
        self.yum = dockerfile_dict.yum
        self.pip = dockerfile_dict.pip
        self.conda = dockerfile_dict.conda