#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: meizhewei
@email: meizw@zhejianglab.com
@time: 2023/4/18 9:59
@desc: 负责管理镜像构建任务，自动定时删除过期任务数据。
"""
import os
import shutil
from db.db_task import DBTask
from data.image_utils import ImageUtils


def delete_task(task_record: DBTask):
    task_dir = task_record.task_work_dir
    if os.path.exists(task_dir):
        shutil.rmtree(task_dir)
        if not os.path.exists(task_dir):
            print(f"成功删除<{task_dir}>")
            return True
        else:
            return False
    else:
        return False