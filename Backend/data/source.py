#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/1/12 17:13
@desc: 源定义
"""
import os.path
import shutil

from pydantic import BaseModel

from utils.config_utils import system_config


class Source(BaseModel):
    """
    将本系统管理的源统一放置在一起，yumm、pip、conda、yum，源管理系统
    """
    installer_name: str = ""
    # 源类型： 比如说ali、qinghua、163
    type: str = ""
    file_name: str = ""

    def get_file_path(self):
        """
        配置文件的目录
        :return:
        """
        return os.path.join(system_config.get_source_dir(), self.installer_name, self.type, self.file_name)

    def copy2(self, destination: str):
        """
        将配置文件拷贝到工作目录,同时修改容器中的文件名称,
        :param destination:
        """
        # adding exception handling

        try:
            if self.source_file_exist():
                shutil.copyfile(self.get_file_path(), os.path.join(destination, self.file_name))
        except IOError as e:
            print("Unable to copy file. %s" % e)

    def source_file_exist(self):
        return len(self.file_name) != 0 and len(self.type) != 0 and os.path.exists(self.get_file_path())

    @classmethod
    def get_default_source(cls):
        return cls()

    def __repr__(self):
        return f"<Source(installer_name={self.installer_name}, type={self.type}, file_name={self.file_name}))>"
