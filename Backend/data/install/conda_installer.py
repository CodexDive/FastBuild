#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/1/3 15:39
@desc: conda的安装器，设置Dockerfile中与conda有关的部分
"""
import os
import re

from data.artifact.conda_artifact import CondaArtifact
from data.install.installer import Installer
from data.install.installer_config import InstallerConfig
from data.install.installer_name import InstallerName
from data.artifact.python_artifact import PythonArtifact
from utils.config_utils import system_config
from utils.file_utils import copy2


class CondaInstaller(Installer):
    # conda安装器配置，使用的源和安装软件列表
    conda_installer_config: InstallerConfig
    # conda描述子， 镜像检测时conda的结果
    conda_descriptor: CondaArtifact
    # python环境的安装配置
    python_env_cfg: InstallerConfig
    # python描述子，镜像检测时，python的结果
    python_descriptor: PythonArtifact

    def __init__(self, conda_installer_config: InstallerConfig, conda_descriptor, python_env_cfg, python_descriptor):
        self.conda_descriptor = conda_descriptor
        self.python_env_cfg = python_env_cfg
        self.python_descriptor = python_descriptor

        conda_installer_config.set_delimiter("=")
        conda_installer_config.install.install_loc = "/usr/local/dros/conda"
        conda_installer_config.set_installer_name_to_source(InstallerName.CONDA.value)
        self.conda_installer_config = conda_installer_config

        super().__init__(conda_installer_config)

        self.config_file_dir = "/root/"
        self.config_file_name = ".condarc"
        # 需要引入环境变量，以防止构建出的镜像的基础python环境被破坏
        self.virtualenv = "default"
        self.check_environments = []

    @classmethod
    def get_default_conda_installer(cls):
        return cls(InstallerConfig.get_installer_config(InstallerName.CONDA.value, "="))

    def get_install_command_prefix(self):
        return "RUN conda install -y "

    def get_install_commands(self):
        if not self.installer_config.get_full_software_names():
            # 不需要使用安装器安装软件
            return []
        # 判断镜像内部是否有default，没有执行如下的语句，如果有，则更换语句，先激活环境
        if self.virtualenv not in self.check_environments:
            return [f"RUN conda create -n {self.virtualenv} -y {self.installer_config.get_full_software_names()}"]

        return [f"RUN . {self.installer_config.install.install_loc}/bin/activate  \\",
                f"  && conda activate {self.virtualenv} \\"
                f"  && conda info \\",
                f"  && conda install -y {self.installer_config.get_full_software_names()}"]

    def get_install_me_commands(self):
        install_loc = self.installer_config.install.install_loc
        if not self.installer_config.install.update:
            return []
        return [f"COPY {self.installer_config.install.target} .",
                f"RUN set -ex \\ ",
                f"    && bash {self.installer_config.install.target} -b -p {install_loc} \\",
                f"    && rm -rf {self.installer_config.install.target} ",
                "\n",
                "RUN set -ex \\",
                f"    && ln -s {install_loc}/bin/conda /usr/local/bin/conda \\",
                f"    && ln -s {install_loc}/etc/profile.d/conda.sh /etc/profile.d/conda.sh \\",
                f"    && /bin/bash -c 'source /etc/profile.d/conda.sh' \\",
                f"    && echo . {install_loc}/etc/profile.d/conda.sh >> ~/.bashrc \\",
                f"    && conda --version"]

    def generate_installer_file(self, work_dir):
        if not self.installer_config.install.update:
            return

        if not (self.valid_anaconda() or self.valid_miniconda()):
            raise Exception(f"用户输入的target文件名无效，无法进行conda的安装, target: {self.installer_config.install.target}")
        print(f"将{self.installer_config.install.target}拷贝到Dockerfile工作目录")

        if not os.path.exists(self.get_conda_path()):
            raise Exception("用户选择的conda sh文件在系统中不存在")

        copy2(self.get_conda_path(), os.path.join(work_dir, self.installer_config.install.target))

    def get_conda_path(self):
        conda_dir = system_config.get_conda_dir()
        return os.path.join(conda_dir, self.installer_config.install.target)

    def valid_conda_target(self):
        conda_file_name = self.installer_config.install.target
        return ("Miniconda" in conda_file_name or "Anaconda" in conda_file_name) and "x86_64" in conda_file_name

    def is_anaconda(self):
        conda_file_name = self.installer_config.install.target
        return "Anaconda" in conda_file_name

    def valid_miniconda(self):
        conda_file_name = self.installer_config.install.target
        return re.match(self.miniconda_pattern(), conda_file_name)

    def miniconda_pattern(self):
        if self.installer_config.python_is_py2():
            return r"^Miniconda2-.*-Linux-x86_64.sh$"
        return r"^Miniconda3-.*-Linux-x86_64.sh$"

    def valid_anaconda(self):
        conda_file_name = self.installer_config.install.target
        return re.match(self.anaconda_pattern(), conda_file_name)

    def anaconda_pattern(self):
        if self.installer_config.python_is_py2():
            return r"^Anaconda2.*-Linux-x86_64.sh$"
        return r"^Anaconda3.*-Linux-x86_64.sh$"
