#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/3/9 17:13
@desc: 用于构建ssh框架
"""
from typing import List

from data.dependency import Dependency
from data.image_descriptor import ImageDescriptor
from data.package_manager_installer import PackageManagerInstaller


class Sshd:
    package_manager_installer: PackageManagerInstaller
    dependency: Dependency
    password: str
    config_open: bool
    port = 22

    def __init__(self, password: str, config_open: bool, package_manager_installer, image_descriptor: ImageDescriptor,
                 exist: bool = False) -> None:
        # needs_install 代表页面是否激活
        # exist: 代表检测结果
        self.dependency = Sshd.get_sshd_dependency()
        self.password = password
        self.exist = exist
        self.config_open = config_open
        self.package_manager_installer = package_manager_installer
        self.image_descriptor = image_descriptor
        self.config_file = "/etc/ssh/sshd_config"
        super().__init__()

    def get_deploy_commands(self):
        result = []

        if not self.config_open:
            # 页面未开启sshd配置
            return []

        if self.exist:
            print("镜像内已经部署了sshd服务，不需要再次安装和配置, 本次仅进行密码更新")
            result.extend(self.get_change_password_commands())
            return result

        result.append("# 准备进行sshd的框架的部署")
        result.extend(self.install_dependency_commands())
        result.extend(self.pre_configure_commands())
        result.extend(self.install_commands())
        result.extend(self.post_configure_commands())
        result.extend(self.port_expose_commands())
        result.extend(self.get_change_password_commands())
        return result

    def install_dependency_commands(self):
        return self.package_manager_installer.install_dependency_commands(self.dependency)

    def pre_configure_commands(self) -> List[str]:
        """安装前配置指令"""
        return self.package_manager_installer.get_update_commands()

    def post_configure_commands(self) -> List[str]:
        """安装后为sshd进行后配置，包括创建必要的"""
        return [f"  && mkdir -p /run/sshd \\",
                f"  && ssh-keygen -A \\",
                f"  && echo 'PermitRootLogin yes' >> {self.config_file}"]

    @staticmethod
    def get_sshd_dependency():
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
            raise Exception("sshd密码未正确设置")
        return [f"RUN echo 'root:{self.password}' | chpasswd"]

    def install_commands(self) -> List[str]:
        return [self.package_manager_installer.get_install_command_prefix() + self.get_sshd_software()]

    def get_sshd_software(self):
        if self.image_descriptor.is_ubuntu():
            return "openssh-server \\"
        return "openssh-server openssh-clients \\"

    def start_commands(self) -> List[str]:
        """sshd服务的启动命令"""
        return ["/usr/sbin/sshd"]
