#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/1/4 10:28
@desc: 安装器配置，保存了安装使用的源以及安装的软件列表和版本列表,类名或需要改善
"""
from typing import List, Optional

from pydantic import BaseModel

from data.software import Software
from data.source import Source
from data.upgrade import Upgrade


class InstallerConfig(BaseModel):
    """安装配置，无法模拟conda的虚拟名称，暂时不重要，或可以采用继承的方式解决"""
    # 安装器名称，可取值为yum、apt、pip、conda
    installer_name: str = ""
    # 该安装器需要升级的信息
    install: Upgrade = Upgrade.get_default_upgrade()
    source: Source = Source.get_default_source()
    # 待使用该安装器获得的软件列表
    software_list: List[Software] = []
    delimiter: str = ""
    # 表征安装器依赖的python版本(2, 7, 14)或者(3, 7, 14)
    python_version: Optional[tuple] = ()

    def set_delimiter(self, delimiter: str):
        self.delimiter = delimiter

    def get_full_software_names(self) -> str:
        """
        获取安装器配置时的软件列表对应的软件名字符串
        :return:
        """
        return self.get_full_software_directly(self.software_list)

    def get_full_software_directly(self, softwares: List[Software]) -> str:
        """
        直接根据配置的软件获取软件名-分隔符-版本字符串
        :param softwares:
        :return:
        """
        software_full_names = []
        for software in softwares:
            software_full_names.append(software.get_name_with_delimiter(self.delimiter))

        return " ".join(software_full_names)

    def set_installer_name_to_source(self, installer_name: str):
        self.source.installer_name = installer_name

    @classmethod
    def get_installer_config(cls, installer_name: str, delimiter=""):
        config = cls()
        config.install = None
        config.installer_name = installer_name
        config.software_list = []
        config.delimiter = delimiter
        return config

    def python_is_py2(self):
        return self.get_python_major_version() == "2"

    def get_python_major_version(self) -> str:
        """
        获取安装器依赖的python版本-大版本号major： 2或者3
        :return:
        """
        return self.python_version[0]

    def get_python_minor_version(self) -> str:
        """
        Python 3.7.14 返回37
        :return:
        """
        return self.python_version[0] + self.python_version[1]

    def get_python_minor_point_format_version(self):
        """
        Python 3.7.14 返回3.7
        :return:
        """
        return self.python_version[0] + "." + self.python_version[1]
