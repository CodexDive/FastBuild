#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: meizhewei
@time: 2023/11/10 15:17
@desc: 用于判断用户是使用harbor还是dockerhub
"""



class RepositoryConfig:
    """"仓库配置，用于判断用户是使用harbor还是dockerhub"""
    username: str = ""
    password: str = ""
    needs_push = False

    def get_auth_config_dict(self):
        return {}

    def login(self, docker_client, api_client):
        # modify

    def needs_push(self):
        return needs_push




