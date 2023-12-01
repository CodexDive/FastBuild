#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/13 17:09
@desc: 镜像安装器配置
"""
from pydantic import BaseModel

from data.install.installer_config import InstallerConfig
from data.python_environment import PythonEnvironment


class ImageInstallerConfig(BaseModel):
    python_env: PythonEnvironment
    pip_installer_config: InstallerConfig

    package_manager_installer_config: InstallerConfig
    conda_installer_config: InstallerConfig
    webSSHSecret: str = ""
    jupyterLabSecret: str = ""

    def initialize_python_version(self, tuple_version: tuple):
        """
        由用户选择的安装python文件，确定conda和pip依赖的python环境
        :return:
        """
        self.set_python(tuple_version)

    def set_python(self, tuple_version):
        self.pip_installer_config.python_version = tuple_version
        self.conda_installer_config.python_version = tuple_version
