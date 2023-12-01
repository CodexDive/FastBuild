"""
@Description :
@Datetime :2022/11/17 14:25:22
@Author :meizhewei
@email :meizhewei@zhejianglab.com
"""
import os.path
from typing import List

from data.installer_config import InstallerConfig
from data.software import Software


class Installer:
    """
    安装器基类，无论是yum、apt、conda和pip均继承自该类型
    """

    def __init__(self, installer_config: InstallerConfig) -> None:
        self.installer_config = installer_config
        self.config_file_dir = ""
        self.config_file_name = ""

    def get_config_file_name(self) -> str:
        """
        获取安装器的配置文件名
        :return:
        """
        return self.config_file_name

    def get_config_file_dir(self) -> str:
        """
        获取配置文件所在的目录
        :return:
        """
        return self.config_file_dir

    def handle_preparation(self, work_dir):
        """
        处理安装器准备工作
        1. 比如说生成源文件到工作目录
        2. 拷贝安装安装器需要的文件到工作目录
        """
        # 生成配置文件
        self.generate_source_file(work_dir)
        self.generate_installer_file(work_dir)

    def get_commands(self):
        """
        获取与该安装器所有的命令集合
        :return:
        """
        result = []
        result.extend(self.get_substitute_commands())
        result.extend(self.get_install_me_commands())
        result.extend(self.get_update_commands())
        result.extend(self.get_install_commands())
        return result

    def append_softwares(self, softwares: List[Software]):
        self.installer_config.software_list.extend(softwares)

    def generate_source_file(self, work_dir):
        """
        生成源文件，在工作目录生成yum的源文件.repo和apt的源文件.list
        文件会存放至工作目录
        :param work_dir:
        """
        source = self.installer_config.source
        source.copy2(work_dir)

    def generate_installer_file(self, work_dir):
        pass

    def get_substitute_commands(self) -> List[str]:
        """
        获取替换命令,即将文件拷贝到指定位置
        :return:
        """
        source = self.installer_config.source
        # 如果用户未选择源文件名，则不需要在dockerfile拷贝源文件
        if not source.source_file_exist():
            return []

        return [f"COPY {source.file_name} {self.get_default_config_file_path()}"]

    def get_default_config_file_path(self):
        """
        获取默认的配置文件绝对路径，该路径位于容器中。
        apt: /etc/apt/sources.list
        yum: /etc/yum/Centos-Base-Dros.list # 自己定义的
        pip: /root/.pip/pip.conf
        conda: /root/.condarc
        :return:
        """
        return os.path.join(self.get_config_file_dir(), self.get_config_file_name())

    def get_install_commands(self):
        if not self.installer_config.get_full_software_names():
            # 不需要使用安装器安装软件
            return []
        return [self.get_install_command_prefix() + self.installer_config.get_full_software_names()]

    def get_install_command_prefix(self):
        return ""

    def get_update_commands(self):
        return []

    def get_install_me_commands(self):
        """
        获取安装自身对应的指令，即原先无pip，重新安装pip的dockerfile指令组
        :return:
        """
        return []


def append_new_line(targets: List[str]) -> List[str]:
    result = []
    for line in targets:
        result.append(line + "\n")
    return result


# 注意，该函数不属于Installer类
def get_installers_commands(installers: List[Installer], work_dir) -> List[str]:
    """
    根据一组安装器获取其对应的安装器指令
    :param work_dir:
    :param installers:
    :return: 安装器相关的替换、更新、安装软件
    """
    result = []
    for installer in installers:
        result.extend(installer.get_commands())
    return result
