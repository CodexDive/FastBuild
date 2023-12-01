#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/3/17 18:28
@desc: 回调服务所在的主机端口信息
"""


class CallBackHostConfig:
    host: str
    port: str

    def __init__(self, host, port) -> None:
        super().__init__()
        self.host = host
        self.port = port
