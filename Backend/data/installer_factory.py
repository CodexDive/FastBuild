"""
@Description :
@Datetime :2022/11/17 14:25:22
@Author :meizhewei
@email :meizhewei@zhejianglab.com
"""

from data.apt_installer import AptInstaller
from data.conda_installer import CondaInstaller
from data.dockerfile_json import DockerfileJson
from data.installer import Installer
from data.installer_config import InstallerConfig
from data.installer_name import InstallerName
from data.pip_installer import PipInstaller
from data.yum_installer import YumInstaller


class InstallerFactory:
    """
    安装器工厂类，用于构建所有的安装器，对每一个模板文件json，实例化一个安装器工厂
    """

    @staticmethod
    def get_installers(dockerfile_json: DockerfileJson):
        """
        根据用户的输入，生成对应的安装器，主要是3个：包管理工具，pip、conda
        :param dockerfile_json:
        :return:
        """
        result = []
        for installer in dockerfile_json.installers:
            result.append(InstallerFactory.get_installer(installer))
        return result

    @staticmethod
    def get_installer(installer_config: InstallerConfig) -> Installer:
        """
        根据安装器配置获取安装器
        :param installer_config:
        :return:
        """
        if installer_config.installer_name == InstallerName.YUM.value:
            yum_installer = YumInstaller(installer_config)
            return yum_installer
        elif installer_config.installer_name == InstallerName.APT.value:
            apt_installer = AptInstaller(installer_config)
            return apt_installer
        elif installer_config.installer_name == InstallerName.PIP.value:
            pip_installer = PipInstaller(installer_config, PipArtifact(), python_cfg, python_descriptor)
            return pip_installer
        elif installer_config.installer_name == InstallerName.CONDA.value:
            conda_installer = CondaInstaller(installer_config, CondaArtifact(), "", PythonArtifact())
            return conda_installer
        else:
            raise Exception(f"不支持的安装器: {installer_config.installer_name}")
