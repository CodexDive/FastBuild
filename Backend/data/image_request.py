#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: meizhewei
@email: meizw@zhejianglab.com
@time: 2023/3/21 16:34
@desc: 
"""
from pydantic import BaseModel
from data.image_data_request import ImageDataRequest
from data.dockerfile_json import DockerfileJson


class ImageRequest(BaseModel):
    image_data: ImageDataRequest
    dockerfile_json: DockerfileJson
