#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/7/3 11:17
@desc: 用于描述远端docker的服务主机信息
"""


class RemoteDockerHostConfig:
    host: str
    port: str

    def __init__(self, host, port) -> None:
        super().__init__()
        self.host = host
        self.port = port

    def get_base_url(self):
        return f'tcp://{self.host}:{self.port}'
