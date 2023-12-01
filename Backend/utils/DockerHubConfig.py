#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/7/3 11:17
@desc: 用于描述远端docker的服务主机信息
"""

from data.repository_config import RepositoryConfig

class DockerHubConfig(RepositoryConfig):
    need_push = True
    def __init__(self, username, password) -> None:
        super().__init__()
        self.username = username
        self.password = password
        #self.needs_push()
    def get_auth_config_dict(self):
        return {"username": self.username, "password": self.password}

    def login(self, docker_client, api_client):
        docker_client.login(username=self.username, password=self.password)