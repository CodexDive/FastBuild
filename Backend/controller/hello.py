#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@file: hello.py
@time: 2022/12/27 11:00
@desc: 测试REST请求的文件，无其他特殊的作用
"""
from fastapi import APIRouter

router = APIRouter(prefix="/hello",
                   tags=["hello"],
                   responses={404: {"description": "Not Found Hello eb"}})


@router.get("/welcome")
async def welcome():
    return {"message": "Welcome To hello-controller"}
