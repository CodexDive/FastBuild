#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/1/16 9:39
@desc: 安装器名称合计
"""

from enum import Enum


class InstallerName(Enum):
    YUM = "yum"
    APT = "apt"
    PIP = "pip"
    CONDA = "conda"

    @staticmethod
    def valid_installer_name(installer_name: str) -> bool:
        """作业正常结束状态，作业不处于这些状态，表明作业异常或者作业正在运行"""
        return installer_name in [InstallerName.YUM.value,
                                  InstallerName.APT.value,
                                  InstallerName.PIP.value,
                                  InstallerName.CONDA.value
                                  ]