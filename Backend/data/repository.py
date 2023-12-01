#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: meizhewei
@email: meizw@zhejianglab.com
@time: 2023/11/16 11:06
@desc: 用于判断使用harbor还是dockerhub，主要是逻辑部分
"""


from utils.config_utils import harbor_config, dockerhub_config


class Repository:
    @staticmethod
    def repository_type():
        if (harbor_config and not dockerhub_config) or (not harbor_config and dockerhub_config):
            return repository_config
        raise Exception("未配置正确的repository")