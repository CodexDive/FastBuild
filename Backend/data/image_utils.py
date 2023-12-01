#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/3 15:17
@desc: 用于与Docker服务器进行交互获取镜像的信息
"""

import docker
from docker import TLSConfig
from docker.errors import ImageNotFound, APIError

from data.artifact.artifact_extractor import ArtifactExtractor
from utils.config_utils import fb_tls_config, remote_docker, repository_config


class ImageUtils:
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
    '''
    docker_client.login(username=harbor_config.username, password=harbor_config.password,
                        registry=harbor_config.registry)
    api_client.login(username=harbor_config.username, password=harbor_config.password, registry=harbor_config.registry)
    '''
    repository_config.login(docker_client, api_client)
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

    def get_image_container(self, image_name):
        container = self.docker_client.containers.run(image_name, detach=True, remove=True, tty=True)

        if container.status in ["created", "running"]:
            return container

        raise Exception(f"请通过后台检查镜像{image_name}创建容器的过程")

    def get_image_os_type(self, image_name: str):
        res = self.api_client.inspect_image(image_name)
        return res["Architecture"]

    def get_image_size(self, image_name):
        res = self.api_client.inspect_image(image_name)
        image_size = round(float(res["Size"]) / 1000000000, 2)
        return image_size

    def get_image_id(self, image_name):
        res = self.api_client.inspect_image(image_name)
        image_id = res["Id"].split(":")
        return "".join(image_id[1:])

    def get_image_cmd(self, image_name):
        res = self.api_client.inspect_image(image_name)
        image_cmd_list = res["Config"]["Cmd"]
        if not image_cmd_list:
            return ""
        image_cmd_str = "".join(image_cmd_list)
        if image_cmd_str in ["/bin/bash", "/bin/sh", "bash", "dash", "rzsh", "zsh", "static-sh", "sh"]:
            return ""
        return image_cmd_str

    def get_image_entrypoint(self, image_name):
        res = self.api_client.inspect_image(image_name)
        image_entrypoint_list = res["Config"]["Entrypoint"]
        if not image_entrypoint_list:
            return ""
        image_entrypoint_str = "".join(image_entrypoint_list)
        return image_entrypoint_str

    def get_image_start_program(self, image_name):
        print("Image_Cmd: ", self.get_image_cmd(image_name))
        print("Image_Entrypoint: ", self.get_image_entrypoint(image_name))
        image_start_program = self.get_image_cmd(image_name) + " " + self.get_image_entrypoint(image_name)
        return image_start_program

    def get_image(self, image_name):
        return self.docker_client.images.get(image_name)

    def image_exist(self, image_name):
        """函数仅仅判断镜像是否存在"""
        try:
            return self.docker_client.images.get(image_name)
        except ImageNotFound:
            return False

    def pull_image(self, image_name, log_path=None, to_stdout=True):
        """
        仅仅负责拉取镜像
        :param to_stdout: 是否要将镜像拉取日志输出到标准输出
        :param log_path: 待写入的日志文件路径
        :param image_name:基础镜像名称
        :return:
        """
        repository, tag = image_name.split(":", 1)
        auth_config = repository_config.get_auth_config_dict()
        generator = self.api_client.pull(repository, tag, stream=True, auth_config=auth_config)
        self._log_pull_image_process(generator, log_path, to_stdout=to_stdout)

    def _log_pull_image_process(self, generator, log_path=None, to_stdout=True):
        if log_path is not None:
            self._pull_image_log_to_stdout_and_log_file(generator, log_path, to_stdout=to_stdout)
            return
        if to_stdout:
            self._pull_image_log_to_stdout(generator)

    @staticmethod
    def _pull_image_log_to_stdout_and_log_file(generator, log_path, to_stdout=False):
        with open(log_path, "w") as log:
            for line in generator:
                content: dict = eval(line.decode("utf-8"))
                if not to_stdout:
                    print(content['status'])
                log.write(content['status'] + "\n")

    @staticmethod
    def _pull_image_log_to_stdout(generator):
        """将镜像拉取日志写入标准输出"""
        for line in generator:
            content: dict = eval(line.decode("utf-8"))
            print(content['status'])

    def get_image_identifier(self, image_name):
        image = self.docker_client.images.get(image_name)
        return image.id, image_name

    def invalid_os(self, image_name):
        image_os = self.get_image_os_type(image_name)
        return image_os.lower() not in "amd64 x86_64 x64 x86"

    def build(self, working_directory: str, target_image_name: str, build_log: str):
        """构建，并写入日志"""
        try:
            generator = self.api_client.build(path=working_directory, tag=target_image_name)
            line = b""
            with open(build_log, "w") as log:
                for line in generator:
                    content = get_write_log(line)
                    # 防止conda安装时许多无效打印
                    if content in ['-', '|', '\\', '/']:
                        continue
                    print(target_image_name, ":", content)
                    log.write(content)
            return "Successfully tagged" in line.decode("utf-8")

        except APIError as error:
            print("构建过程中，抛出", error)

    def push(self, target_image_name: str, push_log: str):
        """推送，并写入日志"""
        if not repository_config.needs_push():
            print("未配置仓库，无需推送")
            return

        repository, tag = target_image_name.split(":", 1)
        auth_config = repository_config.get_auth_config_dict()
        try:
            generator = self.api_client.push(repository, tag, True, auth_config, True)
            print("-----推送成功----")
            line = {}
            with open(push_log, "w") as log:
                for line in generator:
                    log.write(str(line) + "\n")
            return "progressDetail" in str(line) and "errorDetail" not in str(line)

        except APIError as error:
            print("构建过程中，抛出", error)

    def delete_by_image_name(self, image_name: str):
        try:
            status = self.api_client.remove_image(image_name)
            print(f"删除镜像{status}")
            return "Untagged" in str(status)
        except APIError as error:
            print(f"删除镜像{image_name},抛出异常", error)

    def delete_by_image_id(self, image_id: str):
        try:
            status = self.api_client.remove_image(image_id, force=True)
            print(f"删除镜像{status}")
            return "Untagged" in status
        except APIError as error:
            print(f"删除镜像{image_id},抛出异常", error)

    def delete_by_image_names(self, image_names):
        for image_name in image_names:
            self.delete_by_image_name(image_name)


def get_write_log(line):
    """
    :param line: 根据docker client的生成器得到docker build log中的日志
    :return: 返回每一行对应的内容
    """
    write_log = line.decode("utf-8")
    content: dict = eval(write_log)
    if "stream" in content:
        write_log = content["stream"]
    return write_log
