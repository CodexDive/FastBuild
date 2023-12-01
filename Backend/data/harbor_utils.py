#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: meizhewei
@time: 2023/11/10 15:17
@desc: 用于与harbor服务器进行交互
"""

import docker
from docker import TLSConfig

from data.artifact.artifact_extractor import ArtifactExtractor
from utils.config_utils import fb_tls_config, remote_docker, harbor_config


class HarborUtils:
    """
    镜像工具包，用于对镜像进行检测，处理启动容器，执行语句，构建镜像
    """
    # docker sdk中上层的api，需要使用远端的docker server执行镜像构建
    tls_config = TLSConfig(
        client_cert=(fb_tls_config.client_cert_path, fb_tls_config.client_key_path),
        ca_cert=fb_tls_config.ca_path,
        verify=True
    )
    docker_client = docker.DockerClient(base_url=remote_docker.get_base_url(), tls=tls_config)
    # api_client docker sdk进行原始的接口调用，主要用来进行inspect_image进行调用获取镜像元数据
    api_client = docker.APIClient(base_url=remote_docker.get_base_url(), tls=tls_config)

    docker_client.login(username=harbor_config.username, password=harbor_config.password,
                        registry=harbor_config.registry)
    api_client.login(username=harbor_config.username, password=harbor_config.password, registry=harbor_config.registry)

    def __init__(self) -> None:
        super().__init__()

    def collect_image_info(self, image_name):
        container = self.get_image_container(image_name)

        print(f"启动容器, 镜像名称: {image_name}, 容器id: {container.short_id}")
        extractor = ArtifactExtractor(image_name, container)
        descriptor = extractor.get_image_descriptor()
        container.stop()

        print(f"停止并移除容器, 镜像名称: {image_name}, 容器id: {container.short_id}")
        print("镜像类型: " + self.get_image_os_type(image_name))
        print("镜像大小: " + str(self.get_image_size(image_name)) + "G")
        return descriptor

