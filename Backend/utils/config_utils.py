#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Filename :config.py
@Description :
@Datatime :2022/09/30 10:01:56
@Author :meizhewei
@email :yangqinglin@zhejianglab.com
'''
import configparser
import os
from pathlib import Path

__all__ = ["Configuration", "system_config", "db_config", "callback_host_config",
           "host_config", "aes_config", "harbor_config", "dockerhub_config",
           "fb_tls_config", "remote_docker", "repository_config"]

from data.repository_config import RepositoryConfig
from utils.DockerHubConfig import DockerHubConfig
from utils.HostConfig import HostConfig
from utils.FBTlsConfig import FBTlsConfig
from utils.RemoteDockerHostConfig import RemoteDockerHostConfig
from utils.aes_config import AESConfig
from utils.callback_host_config import CallBackHostConfig
from utils.db_config import DBConfig
from utils.harbor_config import HarborConfig
from utils.system_config import SystemConfig


class _Config:
    def __init__(self, config, sec: str) -> None:
        self.sec = sec
        self.secs = {}
        for o in config.options(sec):
            self.secs[o] = config.get(sec, o)

    def __getattr__(self, opt):
        try:
            return self.secs[opt]
        except:
            return f"{self.sec} has not attr of {opt}"


class ConfigReader:
    def __init__(self, configFile) -> None:
        self.parser = configparser.ConfigParser()
        self.config_file = Path(__file__).parent.parent.joinpath(configFile)
        self.parser.read(self.config_file)
        self.sections = self.parser.sections()
        self.index = 0

    def config(self, sec):
        assert sec in self.parser.sections();
        f"{sec} not in {self.config_file}"
        return _Config(self.parser, sec)

    def config_in(self, sec):
        return sec in self.parser.sections()

    def __iter__(self):
        return self

    def __next__(self):
        if self.index > len(self.sections) - 1:
            raise StopIteration
        sec = self.sections[self.index]
        self.index += 1
        return sec, _Config(self.parser, sec)


def get_config_file():
    config_file = "config/fb-test.ini"
    if "FB_ENV" not in os.environ:
        return config_file
    env_val = os.environ["FB_ENV"]
    if env_val not in ["dev", "prod", "test"]:
        return config_file

    return "config/" + "fb-" + env_val + ".ini"


class Configuration:

    @staticmethod
    def system_config() -> SystemConfig:
        config = ConfigReader(get_config_file()).config("fb")
        return SystemConfig(config.source_dir, config.task_dir, config.tools_dir)

    @staticmethod
    def host_config() -> HostConfig:
        config = ConfigReader(get_config_file()).config("fb")
        return HostConfig(config.host, config.port)

    @staticmethod
    def db_config() -> DBConfig:
        db_config = ConfigReader(get_config_file()).config("db")
        return DBConfig(db_config.file)

    @staticmethod
    def callback_host_config() -> CallBackHostConfig:
        config = ConfigReader(get_config_file()).config("callback")
        return CallBackHostConfig(config.host, config.port)

    @staticmethod
    def aes_config() -> AESConfig:
        config = ConfigReader(get_config_file()).config("aes")
        assert len(config.iv) == 16 and len(config.key) == 16
        return AESConfig(iv=config.iv, key=config.key)

    @staticmethod
    def fb_tls_config() -> FBTlsConfig:
        tls = ConfigReader(get_config_file()).config("tls")
        client_cert_path = tls.client_cert_path
        client_key_path = tls.client_key_path
        ca_path = tls.ca_path
        return FBTlsConfig(client_cert_path=client_cert_path,
                           client_key_path=client_key_path,
                           ca_path=ca_path)

    @staticmethod
    def remote_docker() -> RemoteDockerHostConfig:
        config = ConfigReader(get_config_file()).config("remote-docker")
        return RemoteDockerHostConfig(host=config.host, port=config.port)


    @staticmethod
    def harbor_config():
        if ConfigReader(get_config_file()).config_in("harbor"):
            config = ConfigReader(get_config_file()).config("harbor")
            return HarborConfig(username=config.username, password=config.password, registry=config.registry)
        return False

    @staticmethod
    def docker_hub_config():
        if ConfigReader(get_config_file()).config_in("docker-hub"):
            config = ConfigReader(get_config_file()).config("docker-hub")
            return DockerHubConfig(username=config.username, password=config.password)
        return False

    @staticmethod
    def repository_config():
        if ConfigReader(get_config_file()).config_in("docker-hub") and ConfigReader(get_config_file()).config_in("harbor"):
            raise Exception("不支持docker-hub和harbor同时存在")

        if ConfigReader(get_config_file()).config_in("docker-hub"):
            config = ConfigReader(get_config_file()).config("docker-hub")
            return DockerHubConfig(username=config.username, password=config.password)

        if ConfigReader(get_config_file()).config_in("harbor"):
            config = ConfigReader(get_config_file()).config("harbor")
            return HarborConfig(username=config.username, password=config.password, registry=config.registry)

        return RepositoryConfig()



db_config = Configuration.db_config()
system_config = Configuration.system_config()
host_config = Configuration.host_config()
callback_host_config = Configuration.callback_host_config()
aes_config = Configuration.aes_config()
fb_tls_config = Configuration.fb_tls_config()
remote_docker = Configuration.remote_docker()
harbor_config = Configuration.harbor_config()
dockerhub_config = Configuration.docker_hub_config()
repository_config = Configuration.repository_config()

if __name__ == '__main__':
    fb_config = Configuration.system_config()
    print("任务目录: " + f"{fb_config.get_task_dir()}")
    print("pip2目录: " + f"{fb_config.get_pip2_dir()}")
