#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/3 15:44
@desc: 镜像描述类，用于描述镜像的核心信息
"""

import jsonpickle

from data.artifact.artifact import Artifact
from data.artifact.conda_artifact import CondaArtifact
from data.artifact.jupyter_lab_artifact import JupyterLabArtifact
from data.artifact.kernel_artifact import KernelArtifact
from data.artifact.pip_artifact import PipArtifact
from data.artifact.python_artifact import PythonArtifact
from data.artifact.sshd_artifact import SshdArtifact
from db.db_image_check_result import DBImageCheckResult


class ImageDescriptor:
    """镜像描述子，用于描述镜像的重要制品信息"""

    image_name: str
    image_id: str
    os: Artifact
    kernel: KernelArtifact
    pip: PipArtifact
    conda: CondaArtifact
    # Ubuntu镜像为apt，centos镜像为yum
    package_manager: Artifact
    python: PythonArtifact
    sshd: SshdArtifact
    jupyter_lab: JupyterLabArtifact

    def __init__(self, image_name) -> None:
        super().__init__()
        self.image_name = image_name

    def get_db_image_check_result_service(self):
        return DBImageCheckResult(image_id=self.image_id, image_name=self.image_name, result=jsonpickle.dumps(self))

    def is_ubuntu(self):
        return self.os.name == "Ubuntu"

    def is_centos(self):
        return self.os.name == "Centos"
