"""
@Description :
@Datetime :2022/11/17 14:25:22
@Author :meizhewei
@email :meizhewei@zhejianglab.com
"""
from typing import List

from data.install.installer_config import InstallerConfig
from data.install.installer_name import InstallerName
from data.install.package_manager_installer import PackageManagerInstaller


class AptInstaller(PackageManagerInstaller):
    """
    该类主要负责生成apt的配置文件到工作目录下，然后获取覆盖指令，更新指令， 安装软件指令
    """

    def __init__(self, installer_config: InstallerConfig) -> None:
        installer_config.set_installer_name_to_source(InstallerName.APT.value)
        super().__init__(installer_config)

        self.config_file_dir = "/etc/apt"
        self.config_file_name = "sources.list"

    @classmethod
    def get_default_apt_installer(cls):
        return cls(InstallerConfig.get_installer_config(InstallerName.APT.value))

    def get_install_command_prefix(self):
        return "RUN DEBIAN_FRONTEND=noninteractive apt-get install -y "

    def get_update_commands(self):
        return ["RUN DEBIAN_FRONTEND=noninteractive apt-get clean \\",
                "  && apt-get update"]

    def get_install_commands(self):
        if not self.installer_config.get_full_software_names():
            # 不需要使用安装器安装软件
            return []
        return [f"{self.get_install_command_prefix()} {self.installer_config.get_full_software_names()}"]

    def get_substitute_commands(self) -> List[str]:
        source = self.installer_config.source
        if not source.source_file_exist():
            return []
        # 备份第一行，是为了防止类似CUDA的 gpgkey的问题
        return [
            f"RUN if [ -e /etc/apt/sources.list.d ]; then mv /etc/apt/sources.list.d /etc/apt/sources.list.d.bak; fi",
            f"COPY {source.file_name} {self.get_default_config_file_path()}"]
