#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/6/30 14:36
@desc: 用于保存TLS配置信息
"""


class FBTlsConfig:
    client_cert_path: str
    client_key_path: str
    ca_path: str

    def __init__(self, client_cert_path, client_key_path, ca_path) -> None:
        self.client_cert_path = client_cert_path
        self.client_key_path = client_key_path
        self.ca_path = ca_path
        super().__init__()
