#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/3/17 18:00
@desc: 用于描述FastBuild服务所在的域名和端口信息
"""


class HostConfig:
    """用于描述FastBuild所占据的主机域名"""
    host: str
    port: int

    def __init__(self, host, port) -> None:
        super().__init__()
        self.host = host
        self.port = port

    def get_static_resource_prefix(self):
        return "http://" + self.host + ":" + str(self.port) + "/task" +"/"
