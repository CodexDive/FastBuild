#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/3/22 11:14
@desc: 用于AESconfig
"""


class AESConfig:
    """用于保存AES加密和解密的两个配置变量一定是要16位"""
    iv: str
    key: str

    def __init__(self, iv, key) -> None:
        super().__init__()
        self.iv = iv
        self.key = key
