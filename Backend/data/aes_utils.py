#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/3/22 9:35
@desc: 用于进行AES加密解密的使用
"""

import base64

from Crypto.Cipher import _AES

from utils.config_utils import aes_config


class AESUtils:

    @staticmethod
    def decrypt(encrypted):
        # 去掉 PKCS5Padding 的填充
        un_pad = lambda s: s[:-ord(s[len(s) - 1:])]

        # 创建加密对象
        key_encode = aes_config.key.encode("utf-8")
        iv_encode = aes_config.iv.encode("utf-8")
        cipher = _AES.new(key_encode, _AES.MODE_CBC, iv_encode)
        # base64 解码
        decode_text = base64.b64decode(str(encrypted).encode('utf-8'))
        decrypt_text = un_pad(cipher.decrypt(decode_text)).decode('utf8')
        return decrypt_text


if __name__ == '__main__':
    # "Alkaid123456"
    print(AESUtils.decrypt("j7yC3VEVGFAJIRmnel+XVA=="))
    # " "
    print(AESUtils.decrypt("EhbK7QBAQ+DyPSmUS5Ur+Q=="))
    # ""
    print(AESUtils.decrypt("qkrhxQmWOe5kvpJpplvTuQ=="))
