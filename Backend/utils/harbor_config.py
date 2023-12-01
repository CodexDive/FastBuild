#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/9/19 14:25
@desc: 
"""

from data.repository_config import RepositoryConfig

class HarborConfig(RepositoryConfig):
    """存储系统所存储的Harbor配置"""
    registry: str
    need_push = True
    def __init__(self, username, password, registry) -> None:
        super().__init__()
        self.username = username
        self.password = password
        self.registry = registry

    def get_auth_config_dict(self):
        return {"username": self.username, "password": self.password, "registry": self.registry}

    def login(self, docker_client, api_client):
        docker_client.login(username=self.username, password=self.password, registry=self.registry)


