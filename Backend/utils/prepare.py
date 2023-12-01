#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: meizhewei
@email: meizw@zhejianglab.com
@time: 2023/11/27 9:23
@desc: 
"""
from data.image_utils import ImageUtils
from db.db_image import DBImage
from db.db_image_service import DBImageService


class Prepare:
    def __init__(self):
        self.image_name = None
        self.image_utils = ImageUtils()

    def prepare_images(self):
        image_list = ["ubuntu:18.04", "ubuntu:20.04", "centos:centos7", "centos:centos8"]
        for image in image_list:
            self.image_name = str(image)
            self.image_utils.pull_image(self.image_name)
            name, tag = tuple(self.image_name.split(":"))
            if not DBImageService.search_image_by_name_tag(name, tag):
                DBImageService.save(self.get_db_image())
                print(f"写入镜像 {self.image_name} 到数据库")
        return "完成官方预置镜像导入"

    def get_db_image(self):
        name, tag = tuple(self.image_name.split(":"))
        record = DBImage(
            task_id=0,
            name=name,
            tag=tag,
            id=self.image_utils.get_image_id(self.image_name),
            type="Base",
            #增加基础镜像
            description="预置镜像",
            size=str(self.image_utils.get_image_size(self.image_name)) + "G" ,
            interaction=""
        )
        return record