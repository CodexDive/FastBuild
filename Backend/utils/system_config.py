#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@file: sbatch_config.py.py
@time: 2022/11/10 14:47
@desc: 新建配置类，用于存储与脚本有关的信息
"""
import os.path


class SystemConfig:
    """该配置类用于保存系统常用的目录"""

    def __init__(self, source_dir: str, task_dir: str, tools_dir: str):
        self._source_dir = source_dir
        self._task_dir = task_dir
        self._tools_dir = tools_dir

    def get_source_dir(self):
        return self._source_dir

    def get_task_dir(self):
        return self._task_dir

    def get_tools_dir(self):
        return self._tools_dir

    def get_python_dir(self):
        """
        获取python安装包所在的目录
        :return:
        """
        return os.path.join(self.get_tools_dir(), "python")

    def get_conda_dir(self):
        """
        获取conda软件安装目录
        :return:
        """
        return os.path.join(self.get_tools_dir(), "conda")

    def _get_pip_dir(self):
        """
        获取pip中的get_pip.py所在的文件
        :return:
        """
        return os.path.join(self.get_tools_dir(), "pip")

    def get_pip2_dir(self):
        """
        获取pip2安装的get-pip.py所在绝对路径
        :return:
        """
        return os.path.join(self._get_pip_dir(), "pip2", "get-pip.py")

    def get_pip3_dir(self):
        """
        获取pip3所安装的get-pip.py所在的绝对路径
        :return:
        """
        return os.path.join(self._get_pip_dir(), "pip3", "get-pip.py")
