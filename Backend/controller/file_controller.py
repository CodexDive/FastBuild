#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: meizhewei
@email: meizw@zhejianglab.com
@time: 2023/2/10 17:11
@desc: 
"""

from typing import List

from fastapi import APIRouter
from fastapi import File, UploadFile

from data import file_transfer
from utils.response import Response

router = APIRouter(
    prefix="/api/fast-build/file",
    tags=["file"],
    responses={404: {"description": "file module error"}}
)


@router.get("/welcome")
async def welcome():
    return {"message": "Welcome To File Module"}


@router.get("/list-source")
def list_source():
    data = file_transfer.list_source()
    return Response.success(data=data)


@router.get("/list-software")
def list_software():
    data = file_transfer.list_software()
    return Response.success(data=data)


@router.post("/upload")
async def upload_file(file_type: str, files: List[UploadFile] = File(...)):
    if file_type == "source":
        data = await file_transfer.upload_source(files)
        return Response.success(data=data)
    if file_type in ["python", "pip", "conda"]:
        data = await file_transfer.upload_software(file_type, files)
        return Response.success(data=data)
    else:
        return Response.error(data="file_type error")
