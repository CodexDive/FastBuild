#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/3/13 10:54
@desc: 控制镜像检测结果控制器
"""

from fastapi import APIRouter

from db.db_image_check_result_service import DBImageCheckResultService
from utils.response import Response

router = APIRouter(
    prefix="/api/fast-build/check-result",
    tags=["check-result"],
    responses={404: {"description": "data module error"}}
)


@router.get("/welcome")
async def welcome():
    return {"message": "Welcome To db-check-result-controller"}


@router.delete("/delete-all-check-result")
async def delete_all_check_result():
    DBImageCheckResultService.delete_all()
    return Response.success(msg="镜像检测结果全部删除")


@router.get("/all-check-result")
async def get_all_check_result():
    return Response.success(msg="获取全部检测结果成功", data=DBImageCheckResultService.query_all())
