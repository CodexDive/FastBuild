#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/3 11:11
@desc: 制品提取器，用于提取一个容器中的基础环境信息
"""
from typing import List

from docker.models.containers import Container

from data.artifact.apt_artifact import AptArtifact
from data.artifact.artifact import Artifact
from data.artifact.centos_artifact import CentosArtifact
from data.artifact.conda_artifact import CondaArtifact
from data.fb_exception import FBException
from data.image_descriptor import ImageDescriptor
from data.install.installer_name import InstallerName
from data.artifact.jupyter_lab_artifact import JupyterLabArtifact
from data.artifact.kernel_artifact import KernelArtifact
from data.artifact.pip_artifact import PipArtifact
from data.artifact.python_artifact import PythonArtifact
from data.artifact.sshd_artifact import SshdArtifact
from data.artifact.ubuntu_artifact import UbuntuArtifact
from data.artifact.yum_artifact import YumArtifact


# TODO 思考ArtifactExtractor与ImageDescriptor是否需要糅合


class ArtifactExtractor:
    """
    制品提取器，主要用于提取容器中的重要环境是否可用，版本信息等
    """
    container: Container
    image_name: str

    def __init__(self, image_name, container: Container) -> None:
        super().__init__()
        self.image_name = image_name
        self.container = container
        self.image_id = self.container.image.id

    def get_kernel_artifact(self) -> Artifact:
        return KernelArtifact(self.get_kernel_version())

    def get_sshd_artifact(self) -> Artifact:
        if self.contains_sshd_service():
            return SshdArtifact(True, version=self.get_sshd_version())
        return SshdArtifact(False)

    def get_jupyter_lab_artifact(self) -> Artifact:
        if self.contains_jupyter_lab_service():
            return JupyterLabArtifact(True, version=(self.get_jupyterlab_version()))
        return JupyterLabArtifact(False)

    def contains_jupyter_lab_service(self):
        return self.contains_service("ps -ef", "jupyter-lab")

    def get_jupyterlab_version(self):
        raw_out_put = self.get_command_result("jupyter-lab --version")
        return self.expected_first_line_result(raw_out_put)

    @staticmethod
    def expected_first_line_result(raw_out_put):
        """
        命令的原始輸出中取第1行結果
        :param raw_out_put: '\n@eaDir\nCommon\nLICENSE\nxxxfold_v0_debug_v0\nxxxfold_v0_test\n"
        :return:
        """
        return raw_out_put.splitlines(keepends=False)[0]

    @staticmethod
    def expected_all_line_result(raw_out_put) -> List[str]:
        return raw_out_put.splitlines(keepends=False)

    def contains_sshd_service(self):
        return self.contains_service("ps -ef", "sshd")

    def contains_service(self, command, service_name):
        lines = self.get_command_result(command).splitlines()
        for line in lines:
            if service_name in line:
                return True
        return False

    def get_kernel_version(self):
        return self.expected_first_line_result(self.get_command_result("uname -a"))

    def get_os_artifact(self) -> Artifact:
        if self.__is_ubuntu():
            return UbuntuArtifact(self.get_ubuntu_version())
        if self.__is_centos():
            return CentosArtifact(self.get_centos_version())
        print("in get_os_artifact, os 内容： " + "\n".join(self.get_os_release_contents()))
        raise FBException("镜像系统版本不符，仅支持ubuntu:{18.04,20.04},centos:{7,8}")

    def get_os_release_contents(self):
        return self.expected_all_line_result(self.get_command_result("cat /etc/os-release"))

    def get_ubuntu_version(self):
        contents = self.get_os_release_contents()
        for line in contents:
            if not line.startswith("VERSION="):
                continue
            # 18.04.6 LTS (Bionic Beaver)
            return line.split("=")[1].replace('"', '')
        raise FBException("Ubuntu /etc/os-release 无法解析有效Ubuntu 版本信息")

    def get_sshd_version(self):
        return self.expected_first_line_result(self.get_command_result("ssh -V"))

    def get_centos_version(self):
        return self.expected_first_line_result(self.get_command_result("cat /etc/centos-release"))

    def get_pip_artifact(self) -> Artifact:
        version_info = self.get_multiple_pip_version()

        pip_source = self.get_pip_source(is_apt=self.is_ubuntu())
        return PipArtifact(version=version_info, source=pip_source)

    def get_multiple_pip_version(self):
        version_info = []
        for pip_command in ["pip -V", "pip2 -V", "pip3 -V"]:
            if self.command_not_exist(pip_command):
                continue
            python_version = self.get_pip_version(pip_command)
            version_info.append(f"{pip_command.split()[0]}({python_version})")
        return version_info

    def get_pip_version(self, pip_command):
        return self.expected_first_line_result(self.get_command_result(pip_command))

    def get_conda_artifact(self) -> Artifact:
        if self.command_not_exist("conda -v"):
            return CondaArtifact("", [], [])

        return CondaArtifact(version=self.get_conda_version(), environments=(self.get_conda_environments()),
                             source=self.get_conda_source(is_apt=self.is_ubuntu()))

    def get_conda_version(self):
        return self.expected_first_line_result(self.get_command_result("conda -V"))

    def get_conda_environments(self) -> List[str]:
        """获取镜像中存在的环境列表"""

        # # conda environments:
        # #
        # base                  *  /usr/local/dros/conda
        # default                  /usr/local/dros/conda/envs/default
        result = self.expected_all_line_result(self.get_command_result("conda env list"))
        envs = []
        # for item in result:
        #     if item.startswith("#") or len(item) == 0:
        #         continue
        #     envs.append(item.split()[0])

        return [item.split()[0] for item in result if not len(item) == 0 and not item.startswith("#")]

    def get_yum_artifact(self) -> Artifact:
        result = self.get_command_result("yum --version")
        print(f"yum 版本信息为: {result}")

        return YumArtifact(self.expected_first_line_result(result), source=self.get_yum_source())

    def get_apt_artifact(self) -> Artifact:

        source = self.get_apt_source()
        return AptArtifact(self.get_apt_version(), source=source)

    def get_pip_source(self, is_apt=False):
        return self.get_source("cat /root/.pip/pip.conf", is_apt)

    def get_conda_source(self, is_apt=False):
        return self.get_source("cat /root/.condarc", is_apt)

    def get_yum_source(self):
        return self.get_source("grep baseurl -r /etc/yum.repos.d/")

    def get_apt_source(self):
        return self.get_source("grep deb -r /etc/apt", is_apt=True)

    def get_apt_version(self):
        return self.expected_first_line_result(self.get_command_result("apt -v"))

    def get_source(self, extract_contents_command, is_apt=False):
        if not self.command_success(extract_contents_command):
            return []

        contents = self.expected_all_line_result(self.get_command_result(extract_contents_command))
        source = []
        for source_type in self.get_available_source_types():
            if has_source(contents, source_type, is_apt=is_apt):
                source.append(source_type)
        return source

    @staticmethod
    def get_available_source_types():
        return ["aliyun", "163", "tsinghua", "utsc"]

    def get_python_artifact(self) -> Artifact:
        return PythonArtifact(self.get_multiple_python_version())

    def get_multiple_python_version(self):
        version_info = []
        for command in ["python -V", "python2 -V", "python3 -V"]:
            if not self.command_not_exist(command):
                python_version = self.get_python_version(command)
                version_info.append(f"{command.split()[0]}({python_version})")
        return version_info

    def get_python_version(self, command):
        return self.expected_first_line_result(self.get_command_result(command))

    def get_image_descriptor(self) -> ImageDescriptor:
        """
        获取镜像描述信息
        :return:
        """
        descriptor = ImageDescriptor(self.image_name)
        descriptor.kernel = self.get_kernel_artifact()

        descriptor.os = self.get_os_artifact()
        descriptor.package_manager = self.get_package_manager_artifact()
        descriptor.pip = self.get_pip_artifact()
        descriptor.conda = self.get_conda_artifact()
        descriptor.python = self.get_python_artifact()
        descriptor.image_id = self.image_id

        descriptor.sshd = self.get_sshd_artifact()
        descriptor.jupyter_lab = self.get_jupyter_lab_artifact()
        return descriptor

    def get_package_manager_name(self):
        if self.__is_ubuntu():
            return InstallerName.APT.value
        else:
            return InstallerName.YUM.value

    def get_package_manager_artifact(self) -> Artifact:
        if self.__is_ubuntu():
            return self.get_apt_artifact()
        if self.__is_centos():
            return self.get_yum_artifact()
        raise FBException("在获取系统包管理工具时，抛出异常，镜像系统非centos， ubuntu")

    def __is_ubuntu(self) -> bool:
        return "ubuntu" in self.get_command_result("cat /etc/issue").lower()

    def __is_centos(self) -> bool:
        contents = self.get_os_release_contents()
        for line in contents:
            if "centos" in line.lower():
                return True
        return False

    def is_ubuntu(self) -> bool:
        return self.__is_ubuntu()

    def command_not_exist(self, cmd):
        exit_code, output = self.container.exec_run(cmd)
        return "not found" in output.decode()

    def command_success(self, cmd) -> bool:
        """
        判断命令执行成功与否，成功表示命令存在，如果为假，表示命令不存在或者命令执行失败(比如说传入了不支持的选项)
        :param cmd: 待校验命令
        :return: 判断命令执行结果是否成功
        """
        exit_code, output = self.container.exec_run(cmd)
        return exit_code == 0

    def get_command_result(self, cmd: str) -> str:
        """
        :param cmd:
        :return:
        """
        assert self.command_success(cmd)
        exit_code, output = self.container.exec_run(cmd)
        return output.decode("utf-8")


def has_source(contents: List[str], source_type, is_apt=False):
    for line in contents:
        content = get_content_from_line(line, is_apt)
        if has_valid_source(content, source_type):
            return True
    return False


def has_valid_source(content, source_type):
    """如果待校验的content中不以#"""
    return not content.startswith("#") and source_type in content


def get_content_from_line(line: str, is_apt=False):
    if not is_apt:
        return line.strip()

    if ":" in line:
        return "".join(line.split(":")[1:]).strip()
    return line.strip()
