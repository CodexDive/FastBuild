#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/24 14:23
@desc: 枚举类，用于表示镜像构建状态
"""
from enum import Enum


class ImageState(Enum):
    """镜像构建和推送状态"""
    """构建状态"""
    QUEUED = "QUEUED"
    STARTED = "STARTED"
    PULL_SUCCESS = "PULL_SUCCESS"
    PULL_FAILED = "PULL_FAILED"
    PREPARE_SUCCESS = "PREPARE_SUCCESS"
    PREPARE_FAILED = "PREPARE_FAILED"
    CHECK_SUCCESS = "CHECK_SUCCESS"
    CHECK_FAILED = "CHECK_FAILED"
    # 正在构建
    BUILDING = "BUILDING"
    # 构建成功，开始推送
    BUILD_SUCCESS = "BUILD_SUCCESS"
    # 构建失败
    BUILD_FAILED = "BUILD_FAILED"

    """大小检测"""
    # 大小符合
    CHECK_IMAGE_SIZE_SUCCESS = "CHECK_IMAGE_SIZE_SUCCESS"
    # 大小超限
    CHECK_IMAGE_SIZE_FAILED = "CHECK_IMAGE_SIZE_FAILED"

    # 推送成功
    PUSH_SUCCESS = "PUSH_SUCCESS"
    # 推送失败
    PUSH_FAILED = "PUSH_FAILED"

    BUILD_ABORT = "BUILD_ABORT"

    @staticmethod
    def running_states():
        running_states = [ImageState.STARTED, ImageState.PULL_SUCCESS, ImageState.PREPARE_SUCCESS,
                          ImageState.CHECK_SUCCESS, ImageState.BUILDING, ImageState.BUILD_SUCCESS,
                          ImageState.CHECK_IMAGE_SIZE_SUCCESS]
        return [state.value for state in running_states]

    @staticmethod
    def queue_state():
        return ImageState.QUEUED.value

    @staticmethod
    def failed_states():
        failed_states = [ImageState.PULL_FAILED, ImageState.PREPARE_FAILED, ImageState.CHECK_FAILED,
                         ImageState.BUILD_FAILED, ImageState.CHECK_IMAGE_SIZE_FAILED, ImageState.PUSH_FAILED]
        return [state.value for state in failed_states]

    @staticmethod
    def normal_end_states():
        states = []
        states.extend(ImageState.failed_states())
        states.extend([ImageState.PUSH_SUCCESS.value])
        return states

    @staticmethod
    def end_states():
        states = ImageState.normal_end_states()
        states.extend([ImageState.BUILD_ABORT.value])
        return states
