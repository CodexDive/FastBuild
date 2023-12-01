#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/1/3 15:35
@desc: 
"""
import os.path

from data.fb_exception import FBException
from data.install.installer import Installer
from data.install.installer_config import InstallerConfig
from data.install.installer_name import InstallerName
from data.artifact.pip_artifact import PipArtifact
from data.artifact.python_artifact import PythonArtifact
from data.install.python_environment import PythonEnvironment
from utils.config_utils import system_config
from utils.file_utils import copy2


class PipInstaller(Installer):
    pip_descriptor: PipArtifact
    python_descriptor: PythonArtifact
    python_env_cfg: PythonEnvironment

    def __init__(self, pip_installer_config: InstallerConfig, pip_descriptor, python_env_cfg, python_descriptor):
        self.pip_descriptor = pip_descriptor
        self.python_descriptor = python_descriptor
        self.python_env_cfg = python_env_cfg

        pip_installer_config.set_installer_name_to_source(InstallerName.PIP.value)
        pip_installer_config.set_delimiter("==")
        pip_installer_config.install.install_loc = "/usr/local/dros/pip"
        self.pip_installer_config = pip_installer_config

        super().__init__(pip_installer_config)

        self.config_file_dir = "/root/.pip/"
        self.config_file_name = "pip.conf"

    @classmethod
    def get_default_pip_installer(cls):
        return cls(InstallerConfig.get_installer_config(InstallerName.PIP.value, "=="))

    def get_install_command_prefix(self):
        return "RUN pip install "

    def get_update_commands(self):
        if not self.installer_config.install.update:
            return []
        python_cmd = self.get_valid_python_cmd_to_upgrade_pip()

        return [f"RUN set -eux \\",
                f"    && {python_cmd} -m pip install --upgrade pip \\",
                f"    && pip --version"]

    def get_install_me_commands(self):
        if self.python_env_cfg.update:
            # 源码编译安装了Python 3
            return []

        if not self.installer_config.install.update:
            return []

        if len(self.installer_config.install.target) == 0:
            return []

        # 只要需要安装python，之前init_python_environment会默认使用源码编译安装

        assert self.installer_config.install.target == "get-pip.py"

        python_cmd = self.python_descriptor.get_python3_command()

        return [f"COPY {self.installer_config.install.target} .",
                f"RUN set -eux \\",
                f"    && {python_cmd} {self.installer_config.install.target} \\",
                f"    && pip --version \\",
                f"    && pip install --upgrade pip \\",
                f"    && pip --version \\",
                f"    && rm -rf {self.installer_config.install.target}"]

    def generate_installer_file(self, work_dir):
        if not self.installer_config.install.update:
            return
        if "get-pip.py" == self.installer_config.install.target:
            print("将get-pip.py 拷贝到工作目录")
            copy2(self.get_pip_path(), os.path.join(work_dir, self.installer_config.install.target))
        else:
            print("FastBuild采用安装python的方式直接安装pip，请用户输入有效的文件名")

    def get_pip_path(self):
        if self.installer_config.python_is_py2():
            return system_config.get_pip2_dir()
        return system_config.get_pip3_dir()

    def get_valid_python_cmd_to_upgrade_pip(self):
        if self.python_env_cfg.update:
            return "python"
        if self.python_descriptor.has_python3():
            return self.python_descriptor.get_python3_command()
        raise FBException("在获取用于升级pip的命令时，无法获取有效的python命令")
