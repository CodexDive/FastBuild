#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/9 14:16
@desc: 用于建模python环境的变化
"""
import os
import re
import shutil
from typing import List, Union

from pydantic import BaseModel

from data.artifact.dependency import Dependency
from data.software import Software
from utils.config_utils import system_config


class PythonEnvironment(BaseModel):
    """
    专用类，用于建模Python环境的变化
    """
    present: Union[list, str]
    update: bool = False
    target: Union[list, str]
    install_loc: str = "/usr/local/dros/python"

    def copy2(self, work_dir: str):
        try:
            shutil.copyfile(self.get_target_file(), os.path.join(work_dir, self.target))
        except IOError as e:
            print("Unable to copy file. %s" % e)

    @staticmethod
    def get_python_dependency() -> Dependency:
        # 读取配置文件获取框架有关的依赖
        dependency = Dependency()

        apt_result = []
        for item in "build-essential zlib1g-dev libbluetooth-dev libbz2-dev libc6-dev libexpat1-dev " \
                    "liblzma-dev libncursesw5-dev libncurses5-dev tk-dev uuid-dev xz-utils zlib1g-dev " \
                    "libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev".split(
                " "):
            apt_result.append(Software(name=item))
        dependency.apt_dependencies = apt_result

        yum_result = []
        for item in "gcc make openssl openssl-devel readline readline-devel zlib* libffi-devel bzip2 sqlite-devel".split(" "):
            yum_result.append(Software(name=item))
        dependency.yum_dependencies = yum_result
        return dependency

    def get_python_install_commands(self) -> List[str]:
        """
        在源码安装python时，同时使用源码安装中的pip为pip
        :return:
        """
        result = []
        if not self.update:
            return []
        # 将python压缩包拷贝到镜像工作目录
        symbolic_dir = "/usr/local/bin"
        result.append(f"ADD {self.target} .")
        result.append(f"RUN set -eux \\")
        result.append(f"    && cd {self.get_target_file_uncompressed_name()} \\")
        result.append(
            f"    && ./configure --prefix={self.install_loc} --enable-loadable-sqlite-extensions --enable-shared\\")
        result.append(f"    && nproc=$(nproc) \\")
        result.append(f"    && make -j $nproc && make install \\")
        result.append(f"    && echo {self.install_loc}/lib/ >> /etc/ld.so.conf \\")
        result.append(f"    && /sbin/ldconfig \\")
        result.append(f"    && rm -rf {symbolic_dir}/python \\")
        result.append(
            f"    && ln -s {self.install_loc}/bin/python{self.get_python_minor_point_format_version()} {symbolic_dir}/python \\")
        result.append(f"    && rm -rf {symbolic_dir}/pip \\")
        result.append(
            f"    && ln -s {self.install_loc}/bin/pip{self.get_python_minor_point_format_version()} {symbolic_dir}/pip \\")
        result.append(f"    && cd .. \\")
        result.append(f"    && rm -rf {self.get_target_file_uncompressed_name()} \\")
        result.append(f"    && python -V \\")
        result.append(f"    && pip --version")
        result.append(f"ENV PATH={self.install_loc}/bin:$PATH")
        return result

    def get_target_file(self) -> str:
        """
        获取python 文件的绝对路径
        :return:
        """
        python_dir = system_config.get_python_dir()
        python_tar_file = os.path.join(python_dir, self.target)
        print(f"python 压缩包文件为: {python_tar_file}")
        assert os.path.exists(python_tar_file)
        return python_tar_file

    def is_target_python2(self):
        """
        判断预期安装的python版本是否为2
        :return:
        """
        return self.get_target_python_version() == "2"

    def get_target_python_version(self) -> str:
        "Python-3.11.1.tgz"
        assert self.valid_target(), "python_env中的target要么为Python安装包名称，要么为Python版本信息"
        if "Python-3" or "Python 3" in self.target:
            return "3"
        return "2"

    def get_python_minor_point_format_version(self):
        python_version = self.get_target_python_tuple_version()
        """
        Python 3.7.14 返回3.7
        :return:
        """
        return python_version[0] + "." + python_version[1]

    def get_target_python_tuple_version(self) -> tuple:
        # 从"Python-3.11.1.tgz"中获取(3, 11, 1)
        assert self.valid_target(), "python_env中的target要么为Python安装包名称，要么为Python版本信息"
        return self.get_python_version_tuple(self.target)

    @staticmethod
    def get_python_version_tuple(version_str: str):
        """
        获取python版本的元组(3, 7, 14)
        :param version_str: 形如Python-3.7.14.tgz 或者Python 3.7.10
        :return:
        """

        return tuple(re.findall(r'\d+', version_str))

    def valid_target(self):
        return re.match(r"Python[ -][23].*", self.target)

    def get_target_file_uncompressed_name(self):
        return "Python-" + ".".join(map(str, self.get_target_python_tuple_version()))
