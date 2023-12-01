#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/1/3 15:38
@desc: Yum 安装器
"""
from typing import List

from data.install.installer_config import InstallerConfig
from data.install.installer_name import InstallerName
from data.install.package_manager_installer import PackageManagerInstaller


class YumInstaller(PackageManagerInstaller):
    def __init__(self, installer_config: InstallerConfig):
        installer_config.set_installer_name_to_source(InstallerName.YUM.value)
        super().__init__(installer_config)
        self.config_file_dir = "/etc/yum.repos.d/"
        self.config_file_name = "Centos-Base-Dros.repo"

    @classmethod
    def get_default_yum_installer(cls):
        return cls(InstallerConfig.get_installer_config(InstallerName.YUM.value))

    def get_install_command_prefix(self):
        return "RUN yum -y install "

    def get_update_commands(self):
        return ["RUN yum clean all && yum makecache"]

    def get_install_commands(self):
        if not self.installer_config.get_full_software_names():
            # 不需要使用安装器安装软件
            return []
        return [f"{self.get_install_command_prefix()} {self.installer_config.get_full_software_names()} \\",
                "  &&  yum clean all"]

    def get_install_me_commands(self):
        return super().get_install_me_commands()

    def get_substitute_commands(self) -> List[str]:
        source = self.installer_config.source
        if not source.source_file_exist():
            return []

        result = [f"RUN rm -rf /etc/yum.repos.d/*"]
        result.extend(super().get_substitute_commands())
        return result
