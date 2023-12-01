#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/13 17:34
@desc: 用于描述包管理工具
"""
from data.artifact.dependency import Dependency
from data.install.installer import Installer
from data.install.installer_config import InstallerConfig


class PackageManagerInstaller(Installer):
    def __init__(self, installer_config: InstallerConfig) -> None:
        super().__init__(installer_config)

    def install_dependency_commands(self, dependency: Dependency):
        """获取安装依赖的指令"""
        installer_config = self.installer_config
        installer_name = installer_config.installer_name
        dependencies = dependency.valid_dependencies(installer_name)
        if not dependencies:
            return []

        full_software_names = installer_config.get_full_software_directly(dependencies)
        return [self.get_install_command_prefix() + " " + full_software_names]
