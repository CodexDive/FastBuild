#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/3/10 11:37
@desc: 
"""
import hashlib
from typing import List

from data.dependency import Dependency
from data.package_manager_installer import PackageManagerInstaller
from data.pip_installer import PipInstaller


class JupyterLab:
    package_manager_installer: PackageManagerInstaller
    pip_installer: PipInstaller
    password: str
    config_open: bool
    port = 8888

    def __init__(self, password: str, config_open: bool, package_manager_installer, pip_installer, exist: bool = False):
        self.password = password
        self.config_open = config_open
        self.exist = exist
        self.password = password
        self.config_file = "/root/.jupyter/jupyter_lab_config.py"
        self.password_config_file = "/root/.jupyter/jupyter_server_config.json"
        self.package_manager_installer = package_manager_installer
        self.pip_installer = pip_installer
        super().__init__()

    def get_deploy_commands(self):
        result = []
        if not self.config_open:
            # 页面未开启jupyterlab
            return []

        if self.exist:
            print("镜像内已经部署了sshd服务，不需要再次安装和配置, 本次仅进行密码更新")
            result.extend(self.get_change_password_commands())
            return result

        result.append("# 准备进行JupyterLab的框架的部署")
        result.extend(self.install_dependency_commands())
        result.extend(self.pre_configure_commands())
        result.extend(self.install_commands())
        result.extend(self.post_configure_commands())
        result.extend(self.port_expose_commands())
        result.extend(self.get_change_password_commands())
        return result

    def install_dependency_commands(self):
        return self.package_manager_installer.install_dependency_commands(self.get_jupyter_lab_dependency())

    def pre_configure_commands(self) -> List[str]:
        """安装前配置指令"""
        return []

    def post_configure_commands(self) -> List[str]:
        """安装后为sshd进行后配置，包括创建必要的"""
        result = []
        server_app_setting = "c.ServerApp.ip = \'0.0.0.0\'"
        allow_origin_setting = "c.ServerApp.allow_origin = \'*\'"
        token_setting = "c.ServerApp.token = \'\'"
        result.append(f"RUN rm -rf  {self.config_file} \\")
        result.append(f"  && jupyter lab --generate-config \\")
        result.append(f"  && echo \"{server_app_setting}\" >> {self.config_file} \\")
        result.append(f"  && echo 'c.ServerApp.port = 8888' >> {self.config_file}\\")
        result.append(f"  && echo \"{allow_origin_setting}\" >> {self.config_file} \\")
        result.append(f"  && echo 'c.ServerApp.allow_remote_access = True' >> {self.config_file} \\")
        result.append(f"  && echo 'c.ExtensionApp.open_browser = False' >> {self.config_file}\\")
        result.append(f"  && echo \"{token_setting}\" >> {self.config_file} ")
        return result

    @staticmethod
    def get_jupyter_lab_dependency():
        return Dependency()

    def port_expose_commands(self) -> List[str]:
        """
        暴露22端口
        :return:
        """
        return [f"EXPOSE {self.port}"]

    def get_change_password_commands(self) -> List[str]:
        """
        获取修改密码的命令
        :return:
        """
        if not self.password:
            raise Exception("jupyterlab 密码未正确设置，请首先进行检查")
        salt = "7934fb7a7cb9"
        ret = hashlib.sha1(bytes((self.password + salt).encode("utf-8")))
        ciphertext = 'sha1:{}:{}'.format(salt, ret.hexdigest())
        password_content = "{\"ServerApp\": {\"password\": \"%s\"}}" % ciphertext
        return [f"RUN echo '{password_content}' > {self.password_config_file}"]

    def install_commands(self) -> List[str]:
        # ImportError: urllib3 v2.0 only supports OpenSSL 1.1.1+,
        # currently the 'ssl' module is compiled with 'OpenSSL 1.0.2k-fips  26 Jan 2017'.
        # See: https://github.com/urllib3/urllib3/issues/2168
        return [self.pip_installer.get_install_command_prefix() + "urllib3==1.26.6 jupyterlab==3.4.8"]

    def start_commands(self) -> List[str]:
        """jupyter服务的启动命令"""
        return ["nohup jupyter-lab --allow-root> jupyter.log 2>&1 & "]
