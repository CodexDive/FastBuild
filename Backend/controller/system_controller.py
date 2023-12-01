#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: meizhewei
@time: 2023/8/6 16:44
@desc: 用于查询系统所在服务器中镜像相关信息，供用户进行选择基础镜像，
因为用户生成镜像必须使用已有镜像，以通过避免从DockerHub拉取镜像来降低程序执行时间，
"""
from fastapi import APIRouter

from schedule.schedule_clean_image import auto_clean_all
from utils.response import Response

router = APIRouter(
    prefix="/api/fast-build/system",
    tags=["system"],
    responses={404: {"description": "system module error"}}
)


@router.get("/welcome")
async def welcome():
    return {"message": "Welcome To System Module"}


@router.post("/auto_clean_image")
async def auto_clean_image(reserve_days: int):
    """根据指定天数，自动清理无效镜像"""
    cleaned_image_list = auto_clean_all(reserve_days)
    if cleaned_image_list:
        return Response.success(msg="镜像自动清理成功", data=cleaned_image_list)
    return Response.error(msg="镜像自动清理失败", data=cleaned_image_list)