#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/7 17:26
@desc: 依赖，表征不同系统所需的依赖
"""
from typing import List

from data.install.installer_name import InstallerName
from data.software import Software


class Dependency:
    apt_dependencies: List[Software] = []
    yum_dependencies: List[Software] = []

    def valid_dependencies(self, package_name):
        if package_name == InstallerName.APT.value:
            return self.apt_dependencies
        if package_name == InstallerName.YUM.value:
            return self.yum_dependencies
        raise Exception("环境应该仅依赖系统安装工具")
