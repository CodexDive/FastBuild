#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/10 9:51
@desc: 镜像安装器
"""
import os.path

from data.install.apt_installer import AptInstaller
from data.install.conda_installer import CondaInstaller
from data.dockerfile_command_generator import DockerfileCommandGenerator
from data.image_descriptor import ImageDescriptor
from data.install.image_installer_config import ImageInstallerConfig
from data.install.installer import Installer, append_new_line
from data.install.installer_config import InstallerConfig
from data.artifact.interact_config import InteractConfig
from data.artifact.jupyter_lab import JupyterLab
from data.artifact.pip_installer import PipInstaller
from data.install.python_environment import PythonEnvironment
from data.artifact.sshd import Sshd
from data.install.yum_installer import YumInstaller


class ImageInstaller:
    """
    该类型用于聚集镜像安装器，起初时用于获取默认的安装器
    """
    python_env: PythonEnvironment
    package_manager_installer: Installer
    pip_installer: Installer
    conda_installer: CondaInstaller
    sshd: Sshd
    jupyter_lab: JupyterLab
    image_descriptor: ImageDescriptor
    start_script_name = "start.sh"
    task_id: str
    image_start_program: str

    def __init__(self, python_env, package_manager_installer, pip_installer, conda_installer, sshd,
                 jupyter_lab) -> None:
        super().__init__()
        self.python_env = python_env
        self.package_manager_installer = package_manager_installer
        self.pip_installer = pip_installer

        self.conda_installer = conda_installer
        self.sshd = sshd
        self.jupyter_lab = jupyter_lab

    @classmethod
    def get_image_installer(cls, image_installer_config: ImageInstallerConfig, image_descriptor: ImageDescriptor):
        python_env_cfg = image_installer_config.python_env
        pip_install_cfg = image_installer_config.pip_installer_config
        conda_install_cfg = image_installer_config.conda_installer_config

        python_descriptor = image_descriptor.python
        pip_descriptor = image_descriptor.pip
        conda_descriptor = image_descriptor.conda

        package_manager = cls._initialize_packager_installer(
            image_installer_config.package_manager_installer_config)
        pip_installer = PipInstaller(pip_install_cfg, pip_descriptor, python_env_cfg, python_descriptor)

        conda_installer = CondaInstaller(conda_install_cfg, conda_descriptor, python_env_cfg, python_descriptor)

        sshd = cls.get_sshd(package_manager, image_installer_config.webSSHSecret, image_descriptor)

        jupyter_lab = cls.get_jupyter_lab(package_manager, pip_installer, image_installer_config.jupyterLabSecret)
        return cls(python_env_cfg, package_manager, pip_installer, conda_installer, sshd, jupyter_lab)

    @staticmethod
    def get_jupyter_lab(package_manager, pip_installer, password):
        jupyter_lab_config = InteractConfig(password=password,
                                            config_open=len(password) != 0)
        jupyter_lab = JupyterLab(password=jupyter_lab_config.password,
                                 config_open=jupyter_lab_config.config_open,
                                 pip_installer=pip_installer,
                                 package_manager_installer=package_manager)
        return jupyter_lab

    @staticmethod
    def get_sshd(package_manager, sshd_password, image_descriptor):

        sshd_config = InteractConfig(password=sshd_password,
                                     config_open=len(sshd_password) != 0)
        sshd = Sshd(password=sshd_config.password, config_open=sshd_config.config_open,
                    package_manager_installer=package_manager, image_descriptor=image_descriptor)
        return sshd

    @staticmethod
    def _initialize_packager_installer(package_manager_installer_config: InstallerConfig):
        if package_manager_installer_config.installer_name == "apt":
            return AptInstaller(package_manager_installer_config)
        else:
            return YumInstaller(package_manager_installer_config)

    def get_commands(self, log_path):
        with open(log_path, "w") as log:
            result = []
            log.write(f"生成包管理工具: {self.package_manager_installer.installer_config.installer_name}相关命令\n")
            result.extend(self.package_manager_installer.get_commands())
            result.append("\n")
            log.write(f"生成python环境安装命令\n")
            result.extend(self.python_env.get_python_install_commands())
            result.append("\n")
            log.write(f"生成pip安装器相关的安装指令\n")
            result.extend(self.pip_installer.get_commands())
            result.append("\n")
            log.write(f"生成conda安装器相关的安装指令\n")
            result.extend(self.conda_installer.get_commands())
            result.append("\n")
            log.write(f"生成sshd交互器相关的安装指令\n")
            result.extend(self.sshd.get_deploy_commands())
            result.append("\n")
            log.write(f"生成jupyterlab交互器相关的安装指令\n")
            result.extend(self.jupyter_lab.get_deploy_commands())
            result.append("\n")
            result.extend(self.get_metadata_commands())
            if self.needs_start_script():
                log.write(f"生成sshd、jupyterlab交互器启动脚本")
                result.extend(self.get_start_commands())
            return append_new_line(result)

    def get_start_commands(self):
        """在工作目录下生成启动脚本"""
        if not self.needs_start_script():
            return []

        return [f"COPY {self.start_script_name} .",
                f"ENTRYPOINT bash {self.start_script_name}"]

    def needs_start_script(self):
        # sshd和jupyterlab不可用，表明两个服务未安装，此时需要启动脚本来负责拉起两个服务
        return self.needs_install_sshd() or self.needs_install_jupyterlab()

    def needs_install_jupyterlab(self):
        return not self.image_descriptor.jupyter_lab.available and self.jupyter_lab.config_open

    def needs_install_sshd(self):
        return not self.image_descriptor.sshd.available and self.sshd.config_open

    def handle_start_script(self, work_dir):
        if not self.needs_start_script():
            return
        script_path = os.path.join(work_dir, "start.sh")
        with open(script_path, "w") as script:
            script.write("#/bin/bash\n\n")
            if not self.image_start_program:
                script.writelines([self.image_start_program + " &"])
                script.write("\n")

            if self.sshd.config_open:
                script.writelines(self.sshd.start_commands())
            script.write("\n")
            if self.needs_install_jupyterlab():
                script.writelines(self.jupyter_lab.start_commands())

            script.write("\n")
            script.write("tail -f /var/log/lastlog")
            script.write("\n")

    def handle_preparations(self, work_dir):
        """处理镜像构建钱准备工作"""
        self.handle_python_preparations(work_dir)
        print("完成python环境安装的准备工作")
        self.handle_installer_preparation(work_dir)
        print("完成pip、conda、包管理工具安装器准备工作: 安装器源文件、源文件")

        self.handle_interact_preparations(work_dir)
        print("完成交互通信框架sshd、jupyter准备工作: 配置检测结果，生成启动文件")

    def handle_interact_preparations(self, work_dir):
        """处理交互软件sshd和jupyter是否需要安装
        :param work_dir:
        """
        self.handle_sshd_preparations()
        self.handle_jupyterlab_preparations()
        self.handle_start_script(work_dir)

    def handle_sshd_preparations(self):
        """如果检测结果表明，sshd服务已经可用，则不需要再次安装"""
        self.sshd.exist = self.image_descriptor.sshd.available

    def handle_jupyterlab_preparations(self):
        """如果检测结果表明，jupyterlab服务已经可用，则不需要再次安装"""
        self.jupyter_lab.exist = self.image_descriptor.jupyter_lab.available

    def handle_python_preparations(self, work_dir):
        """
        python更新准备工作：
            1. 将python安装包拷贝到Dockerfile工作目录
            2. 将python相关的依赖导入到包管理工具中
        :param work_dir:
        :return:
        """
        if not self.python_env.update:
            return


        # 拷贝压缩包到工作目录
        self.python_env.copy2(work_dir)
        package_name = self.get_package_manager_name()
        dependencies = PythonEnvironment.get_python_dependency().valid_dependencies(package_name)
        self.package_manager_installer.append_softwares(dependencies)

    def handle_installer_preparation(self, work_dir):
        self.package_manager_installer.handle_preparation(work_dir)
        self.pip_installer.handle_preparation(work_dir)
        self.conda_installer.handle_preparation(work_dir)

    def get_package_manager_name(self):
        """
        获取包管理工具名称
        :return:
        """
        return self.package_manager_installer.installer_config.installer_name

    def get_metadata_commands(self):
        return [DockerfileCommandGenerator.label("constructor", "FastBuild"),
                DockerfileCommandGenerator.label("task_id", self.task_id)]
