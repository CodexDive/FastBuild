#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: meizhewei
@email: meizw@zhejianglab.com
@time: 2023/8/21 16:34
@desc: 
"""

import datetime
import sys

from data.image_utils import ImageUtils
from db.db_image_life_service import DBImagesLifeService
from db.db_task_service import DBTaskService


def auto_clean_all(reserve_days: int = 3):
    auto_clean_image(reserve_days)
    auto_clean_material(reserve_days)
    return


def image_not_used_days(image_name):
    task = DBTaskService.query_latest_task_by_image_name(image_name)
    if not task:
        # 系统生成的镜像，可能从来没有作为基础镜像进行镜像构建任务
        return sys.maxsize
    now = datetime.datetime.now()
    delta = now - task.create_time

    return delta.days


def auto_clean_image(reserve_days):
    """
    1.查询镜像列表,筛选镜像
    2.自动删除镜像
    3.更新数据库
    """
    # 获取超过指定天数的所有镜像
    overtime_image_records = DBImagesLifeService.query_image_by_generate_time_before_days(reserve_days)
    deleted_images = get_image_records_to_delete(overtime_image_records, reserve_days)
    ImageUtils().delete_by_image_names(list(set([image.image_name for image in deleted_images])))
    DBImagesLifeService.update_images_delete_time(deleted_images)


def get_image_records_to_delete(overtime_image_records, reserve_days):
    """
    根据保留的天数判断可疑的镜像记录，确定要删除的镜像记录。如果image_not_used_days天数小于reserve_days，说明该
    镜像作为镜像构建任务的基础镜像，时间较近，镜像可能再次使用，跳过。
    :param overtime_image_records:
    :param reserve_days:
    :return:
    """
    deleted_images = []
    for image_record in overtime_image_records:
        # 如果镜像名称在镜像构建任务中 查询有多少天未使用，则判定可删除
        if image_not_used_days(image_record.image_name) <= reserve_days:
            continue
        deleted_images.append(image_record)
    return deleted_images


def auto_clean_material(reserve_days):
    pass
