#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@file: __init__.py.py
@time: 2022/12/14 15:26
@desc: Task 模拟了一次镜像制作任务，由任务保存了制作信息，目标镜像的信息
"""
import copy
import json
import os
import re
import time
from datetime import datetime

from data.aes_utils import AESUtils
from data.dockerfile_command_generator import DockerfileCommandGenerator
from data.fb_exception import FBException
from data.image_descriptor import ImageDescriptor
from data.install.image_installer import ImageInstaller
from data.image_request import ImageRequest
from data.image_state import ImageState
from data.image_utils import ImageUtils
from data.progress_status import ProgressStatus

from db.db_image_service import DBImageService
from db.db_progress import DBProgress
from db.db_progress_service import DBProgressService
from db.db_task import DBTask
from db.db_task_service import DBTaskService
from db.db_image import DBImage
from db.db_image_life_service import DBImagesLifeService

from utils.callback_service import CallBackService
from utils.config_utils import system_config, host_config
from utils.date_utils import DateUtils
from utils.log import Log

log = Log.ulog("task.log")


class Task:
    """镜像制作任务"""

    def __init__(self, image_descriptor: ImageDescriptor, image_request: ImageRequest):
        self.image_request = image_request
        self.image_utils = ImageUtils()
        self.task_id = int(round(time.time() * 1000))
        self.task_name = self.image_request.image_data.task_name
        self.callback_url = self.image_request.image_data.callback_url
        self.target_image_name = self.image_request.image_data.target_image_name
        self.target_image_desc = self.image_request.image_data.image_desc
        self.base_image_name = self.image_request.dockerfile_json.base_image

        self.image_descriptor = image_descriptor
        self.work_dir_name = DateUtils.now_str_in_millis()
        self.task_work_dir = os.path.join(system_config.get_task_dir(), self.work_dir_name)
        self.dockerfile_json = self.image_request.dockerfile_json
        # 在镜像构建过程中，上述属性都不变，只有record的状态会随着构建的状态而变化
        self.record = self.get_db_task()
        self._create_work_dir()

    def get_front_end_request_json_path(self):
        return os.path.join(self.task_work_dir, "Front_end_request_json")

    def get_raw_front_end_request_json_path(self):
        return os.path.join(self.task_work_dir, "raw_json")

    def work(self):
        self.pull()
        self.check()
        self.prepare()
        self.build()
        self.push()
        # self.callback()
        DBTaskService.save(self.record)

    def pull(self):
        """拉取基础镜像"""
        log.info("拉取基础镜像: {self.image_descriptor.target_image_name}")
        progress = self.get_progress(ProgressStatus.PULL)

        self.image_utils.pull_image(progress.base_image_name, log_path=progress.log_path)

        image_exist = self.image_utils.image_exist(progress.base_image_name)
        final_progress = self.get_final_progress(progress, image_exist)
        self.record.state = ImageState.PULL_SUCCESS.value if image_exist else ImageState.PULL_FAILED.value

        DBProgressService.save(final_progress)

        image_record = DBImagesLifeService.get_db_image(self.base_image_name)
        DBImagesLifeService.save(image_record)

    def check(self):
        """基础镜像检测"""
        if self.record.state != ImageState.PULL_SUCCESS.value: return

        progress = self.get_progress(ProgressStatus.CHECK)

        with open(progress.log_path, "w") as check_log:
            check_log.write(f"任务id: {self.task_id}\n")
            check_log.write(f"任务工作目录: {self.task_work_dir}\n")
            check_log.write(f"基础镜像名: {self.base_image_name}\n")
            check_log.write(f"基础镜像检测结果为: {self.image_descriptor.__dict__}\n")

        self.record.state = ImageState.CHECK_SUCCESS.value
        DBProgressService.save(self.get_success_progress(progress))
        pass

    def prepare(self):
        """材料准备和Dockerfile生成
        1. 存储前端请求
        2. 构建环境初始化
        3. 生成Dockerfile
        4.更新任务进度
        """
        progress = self.get_progress(ProgressStatus.PREPARE)

        self._save_front_end_request_json()
        self._decrypt()
        self.init_pip_environment()
        self.init_conda_environment()
        self.init_python_environment()

        self._generate_dockerfile(log_path=progress.log_path)
        self._list_work_dir()
        DBProgressService.save(self.get_success_progress(progress))

    def _decrypt(self):
        self.dockerfile_json.image_installer_config.webSSHSecret = AESUtils.decrypt(self.image_request.image_data.webSSHSecret)
        self.dockerfile_json.image_installer_config.jupyterLabSecret = AESUtils.decrypt(
            self.image_request.image_data.jupyterLabSecret)

    def build(self):
        log.info("开始构建镜像...")
        progress = self.get_progress(ProgressStatus.BUILD)
        self._log_dir()
        self._update_build_state(self.build_image(log_path=progress.log_path))

        DBProgressService.save(self.get_final_progress(progress, self.record.state == ImageState.BUILD_SUCCESS.value))

    def push(self):
        """镜像推送"""
        log.info("开始推送镜像...")
        progress = self.get_progress(ProgressStatus.PUSH)
        # 开始检测大小(该版本省略)
        #self.update_check_state()
        # 开始推送
        self.update_push_state(self.push_image(progress.log_path))
        DBProgressService.save(self.get_final_progress(progress, self.record.state == ImageState.PUSH_SUCCESS.value))

        DBImagesLifeService.save(DBImagesLifeService.get_db_image(self.target_image_name, image_type="build"))
        DBImageService.save(self.get_db_image())

    def get_final_progress(self, progress: DBProgress, step_success):
        return self.get_success_progress(progress) if step_success else self.get_fail_progress(progress)

    def get_progress(self, action: ProgressStatus):
        """基于当前对象和action实例化进度实例"""

        progress = DBProgress()
        progress.action = action.value
        progress.task_id = self.task_id
        progress.task_name = self.task_name
        progress.base_image_name = self.image_descriptor.image_name
        progress.target_image_name = self.target_image_name

        progress.log_path = os.path.join(self.task_work_dir, action.value + ".log")
        progress.log_url = self.get_log_url(action)
        progress.start_time = datetime.now()
        progress.status = "fail"
        progress.duration = -1
        return progress

    def get_task_http_url(self):
        return host_config.get_static_resource_prefix() + self.work_dir_name + "/"

    def get_log_url(self, action: ProgressStatus):
        return self.get_task_http_url() + action.value + ".log"

    def _log_dir(self):
        print(f"镜像构建任务: {self.task_name}, {self.dockerfile_json.base_image} --> {self.target_image_name}")
        print(f"  Working Home: {self.task_work_dir}")

    def _generate_dockerfile(self, log_path=None):
        """准备材料和生成Dockerfile"""

        """
        1.在目录中创建空dockerfile，并打开。
        2.调用docker_operator中的方法，转换并写入。
        3.转换完成保存
        :param image_descriptor: 镜像描述子
        :param dockerfile_json: dockerfile配置文件对应的映射对象
        :param work_dir: 待保存的dockerfile_path路径
        """
        # 创建空Dockerfile，写入From的target_image_name。
        work_dir = self.task_work_dir
        dockerfile_path = os.path.join(work_dir, "Dockerfile")

        image_installer_config = self.dockerfile_json.image_installer_config
        image_installer = ImageInstaller.get_image_installer(image_installer_config, self.image_descriptor)
        image_installer.image_descriptor = self.image_descriptor
        image_installer.task_id = self.task_id
        image_installer.image_start_program = self.image_utils.get_image_start_program(self.base_image_name)

        print("向安装器传入镜像检测结果")
        # 将conda的虚拟环境列表传入conda安装器
        image_installer.conda_installer.check_environments = self.image_descriptor.conda.environments
        image_installer.handle_preparations(work_dir)
        print("完成生成Dockerfile前准备工作")
        with open(dockerfile_path, "w") as dockerfile:
            dockerfile.write(DockerfileCommandGenerator.from_command(self.dockerfile_json.base_image))
            dockerfile.write(DockerfileCommandGenerator.maintainer_command(self.dockerfile_json.maintainer))
            dockerfile.write(DockerfileCommandGenerator.bash_shell())
            dockerfile.write(DockerfileCommandGenerator.workdir("/root/install"))
            dockerfile.write("\n")
            dockerfile.writelines(image_installer.get_commands(log_path=log_path))

    def _create_work_dir(self):
        """创建任务工作目录"""

        if not os.path.exists(self.task_work_dir):
            os.makedirs(self.task_work_dir)

    def _save_front_end_request_json(self):
        """
        保存传入的dockerfile_json字符串到工作目录中，文件名为dockerfile_json
        :return:
        """
        task_data = {
            "task_name": self.task_name,
            "target_image_name": self.target_image_name
        }
        res = {
            "dockerfile_json": json.loads(self.dockerfile_json.json()),
            "task_data": task_data
        }
        res_json = json.dumps(res, indent=4)
        with open(self.get_front_end_request_json_path(), 'w') as dockerfile_json_file:
            dockerfile_json_file.write(res_json)

        with open(self.get_raw_front_end_request_json_path(), 'w') as raw_json_file:
            raw_json_file.write(self.image_request.json())

    def callback(self):
        state = {"imageName": self.target_image_name, "taskId": self.task_id, "state": self.record.state}
        CallBackService.post_state(state, self.callback_url)

    def check_pip_requirement(self):
        install_config = self.dockerfile_json.image_installer_config
        if install_config.pip_installer_config.install.update:
            # 代表要安装新的pip
            python_update = install_config.python_env.update
            has_python = len(self.image_descriptor.python.version) != 0
            return python_update or has_python
        return True

    def check_package_source_match(self):
        image_installer_config = self.image_request.dockerfile_json.image_installer_config
        package_manager_source_file_name = image_installer_config.package_manager_installer_config.source.file_name
        log.info(f"配置的包管理源文件信息为: {package_manager_source_file_name}")
        if not package_manager_source_file_name:
            return True

        return self.get_version_str(package_manager_source_file_name) in self.image_descriptor.os.version

    def get_version_str(self, package_manager_source_file_name):
        if self.image_descriptor.is_ubuntu():
            return self.get_ubuntu_version_str(package_manager_source_file_name)
        elif self.image_descriptor.is_centos():
            return self.get_centos_version_str(package_manager_source_file_name)
        raise FBException(f"镜像描述符无法确定操作系统, {self.image_descriptor.os.name}")

    @staticmethod
    def get_ubuntu_version_str(package_manager_source_file_name):
        """从源文件名中获取apt源版本信息: 18.04"""
        return ".".join(re.findall(r'\d+', package_manager_source_file_name))

    @staticmethod
    def get_centos_version_str(package_manager_source_file_name):
        """从源文件名中获取centosyum源信息"""
        # CentOS Linux release 8.4.2105

        return "CentOS Linux release " + re.findall(r'\d+', package_manager_source_file_name)[0]

    def build_image(self, log_path=None):
        """
        使用生成的工作目录下必要的内容Dockerfile、配置文件等，生成镜像
        :type log_path: 待写入的文件名称
        :return:
        """
        log.info(self.target_image_name + "镜像开始构建， 时间: " + DateUtils.now_str())
        return ImageUtils().build(working_directory=self.task_work_dir,
                                  target_image_name=self.target_image_name,
                                  build_log=log_path)

    def _update_build_state(self, return_code):
        self.record.state = self.get_build_state(return_code)

    @staticmethod
    def get_build_state(build_success_return_code):
        return ImageState.BUILD_SUCCESS.value if build_success_return_code else ImageState.BUILD_FAILED.value

    def update_check_state(self):
        if self.record.state != str(ImageState.BUILD_SUCCESS.value):
            return
        self.record.state = self.get_target_image_size_check_state()

    def get_target_image_size_check_state(self):
        if self._target_image_size_valid():
            return ImageState.CHECK_IMAGE_SIZE_SUCCESS.value
        return ImageState.CHECK_IMAGE_SIZE_FAILED.value

    def _target_image_size_valid(self):
        """
        检测生成的目标镜像大小，大于50G不推送，回调报错
        :return:
        """
        log.info(self.target_image_name + "校验镜像大小， 时间: " + DateUtils.now_str())
        images_size = self.image_utils.get_image_size(self.target_image_name)
        log.info(f"镜像大小为{str(images_size)}G")
        return images_size <= 50

    def push_image(self, log_path=None):
        """
        推送镜像到harbor镜像仓库
        :return:
        """
        log.info(self.target_image_name + "镜像开始推送， 时间: " + DateUtils.now_str())
        return self.image_utils.push(self.target_image_name, push_log=log_path)

    def update_push_state(self, push_success):
        # 校验镜像大小检测，该版本省略
        # if self.record.state != str(ImageState.CHECK_IMAGE_SIZE_SUCCESS.value):return
        self.record.state = str(ImageState.PUSH_SUCCESS.value) if push_success else str(ImageState.PUSH_FAILED.value)

    def _list_work_dir(self):
        log.info("在工作目录下共有如下文件列表： \n" + "    " + str(os.listdir(self.task_work_dir)))
        pass

    def get_db_task(self):
        record = DBTask(
            task_id=self.task_id,
            name=self.task_name,
            request=self.get_front_end_request_json_path(),
            state=str(ImageState.QUEUED.value),
            base_image_name=self.dockerfile_json.base_image,
            target_image_name=self.image_request.image_data.target_image_name,
            image_name=self.target_image_name,
            description=self.target_image_desc,
            task_work_dir=self.task_work_dir,
            dockerfile_path=os.path.join(self.task_work_dir, "Dockerfile"),
            image_build_log_path=os.path.join(self.task_work_dir, "build.log"),
            work_dir_name=self.work_dir_name,
            callback_url=self.callback_url
        )
        return record

    def have_interaction(self):
        interaction_list = []
        if self.image_descriptor.sshd.available:
            interaction_list.append("WebSSH")
        if self.image_descriptor.jupyter_lab.available:
            interaction_list.append("JupyterLab")
        if self.image_request.image_data.webSSHSecret:
            interaction_list.append("WebSSH")
        if self.image_request.image_data.jupyterLabSecret:
            interaction_list.append("JupyterLab")
        interaction_set = set(interaction_list)
        interaction = ", ".join(interaction_set)
        return interaction

    def get_db_image(self):
        name, tag = tuple(self.target_image_name.split(":"))
        record = DBImage(
            task_id=self.task_id,
            name=name,
            tag=tag,
            id=self.image_utils.get_image_id(self.target_image_name),
            #type="Base",
            type="Customized",
            #增加基础镜像
            description=self.target_image_desc,
            size=str(self.image_utils.get_image_size(self.target_image_name)) + "G" ,
            interaction=self.have_interaction()
        )
        return record

    @staticmethod
    def get_success_progress(progress: DBProgress):
        progress.end_time = datetime.now()
        start_time = progress.start_time
        end_time = progress.end_time
        progress.duration = DateUtils.duration_in_millis(start_time, end_time)
        progress.status = "success"
        return copy.deepcopy(progress)

    @staticmethod
    def get_fail_progress(progress: DBProgress):
        progress.end_time = datetime.now()
        start_time = progress.start_time
        end_time = progress.end_time
        progress.duration = DateUtils.duration_in_millis(start_time, end_time)
        progress.status = "fail"
        return copy.deepcopy(progress)

    def init_pip_environment(self):
        image_installer_config = self.dockerfile_json.image_installer_config
        pip_config = image_installer_config.pip_installer_config
        # 解决bug，仅仅安装pip软件，但不需要更新和设置pip源，有些软件需要最新的pip版本才可以
        # 即只要安装软件列表不空，则将更新pip到最新版本
        # 此时的影响时，只要在更新pip安装器时，只要发现update为true，则要更新
        if pip_config.software_list or self.needs_install_jupyterlab():
            pip_config.install.update = True

    def init_conda_environment(self):
        image_installer_config = self.dockerfile_json.image_installer_config
        conda_installer_config = image_installer_config.conda_installer_config
        if conda_installer_config.software_list:
            log.info(f"由于需要安装conda的软件，需要更新update为True， 之前的update参数为: {conda_installer_config.install.update}")
            conda_installer_config.install.update = True

    def needs_install_jupyterlab(self):
        return len(self.dockerfile_json.image_installer_config.jupyterLabSecret) != 0

    def init_python_environment(self):
        """用于初始化pip的环境"""
        image_installer_config = self.dockerfile_json.image_installer_config
        python_cfg = image_installer_config.python_env
        python_descriptor = self.image_descriptor.python
        if python_cfg.update:
            # 代表本次要安装python3
            version_tuple = python_cfg.get_python_version_tuple(python_cfg.target)
            log.info(f"由于用户配置要使用源码安装python_cfg.target， 更新pip和conda的依赖Python版本元组: f{version_tuple}")
            image_installer_config.set_python(version_tuple)
            return

        if python_descriptor.has_python3():
            python_version_tuple = python_descriptor.get_python3_version_tuple()
            log.info(f"由于用户未使用源码安装python3，使用镜像检测结果的python3来更新pip和conda的依赖版本元组: {python_version_tuple}")
            image_installer_config.set_python(python_version_tuple)
            return

        if not self.needs_python3(image_installer_config):
            # 代表要安装新的pip
            log.info("本次FastBuild构建不需要安装Python3，因此无需初始化")
            return

        self.init_default_python_environment(image_installer_config)

    @staticmethod
    def needs_python3(image_installer_config):
        needs_install_pip = image_installer_config.pip_installer_config.install.update
        needs_install_conda = image_installer_config.conda_installer_config.install.update

        return any([needs_install_pip,
                    needs_install_conda])

    @staticmethod
    def init_default_python_environment(image_installer_config):
        python_env = image_installer_config.python_env
        # 基础镜像没有Python3的运行环境

        python_env.update = True
        python_env.target = "Python-3.7.14.tgz"
        tuple_version = python_env.get_target_python_tuple_version()
        log.info(f"为本次FastBuild构建镜像，为pip和conda安装器初始化默认的Python版本元组信息:{tuple_version}")
        image_installer_config.set_python(tuple_version)
