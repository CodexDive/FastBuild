#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/8/29 14:32
@desc: 用于查询镜像拉取历史
"""

from fastapi import APIRouter

from db.db_image_life_service import DBImagesLifeService
from utils.response import Response

router = APIRouter(
    prefix="/api/fast-build/image-life",
    tags=["image-life"],
    responses={404: {"description": "image-life module error"}}
)


@router.get("/welcome")
async def welcome():
    return {"message": "Welcome To Image Life Module"}


@router.get("/all")
async def query_all():
    """根据镜像名获取拉取历史记录"""
    return Response.success(data=DBImagesLifeService.query_all())
