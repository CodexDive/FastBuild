#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/2/6 16:44
@desc: 用于查询系统所在服务器中镜像相关信息，供用户进行选择基础镜像，
因为用户生成镜像必须使用已有镜像，以通过避免从DockerHub拉取镜像来降低程序执行时间，
"""
from fastapi import APIRouter

from data.image_utils import ImageUtils
from db.db_image_service import DBImageService
from utils.response import Response

router = APIRouter(
    prefix="/api/fast-build/image",
    tags=["image"],
    responses={404: {"description": "task module error"}}
)

@router.get("/welcome")
async def welcome():
    return {"message": "Welcome To Image Module"}

@router.get("/list-all")
async def list_image():
    status = DBImageService.query_all()
    # 直接查询数据库里的
    return Response.success(data=status)


@router.get("/list-image")
async def list_image(page: int, page_size: int, keyword: str = None, image_type: str = None):
    status, total_count = DBImageService.query_image_by_per_page(page, page_size, keyword, image_type)
    # 直接查询数据库里的
    image_data = {"page": {"current": page, "total": total_count, "page_size": page_size}, "image_list": status}
    return Response.success(data=image_data)


@router.delete("/delete-image-by-image-name")
async def delete_image_by_image_name(image_name: str):
    """根据镜像名删除镜像"""
    # 校验数据库，是否被当成base_image使用
    # 若否，则继续。若是，则无法删除。

    # 未删除harbor里的镜像，如何实现？
    image_utils = ImageUtils()
    # if not image_utils.delete_harbor_image(image_name):
    #     return Response.error(data="image delete failed")
    status = image_utils.delete_by_image_name(image_name)
    name, tag = tuple(image_name.split(":"))
    if status:
        result = DBImageService.del_image(name=name, tag=tag)
        return Response.success(data=result)
    return Response.error(data=status)

