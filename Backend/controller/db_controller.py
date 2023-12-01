"""
@Description :数据接入与转换接口，包含前端下发的json配置文件接收，json转dockerfile，直接接收dockerfile。
@Datetime :2022/11/17 14:25:22
@Author :meizhewei
@email :meizhewei@zhejianglab.com
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/api/fast-build/data",
    tags=["data"],
    responses={404: {"description": "data module error"}}
)


@router.get("/welcome")
async def welcome():
    return {"message": "Welcome To db-controller"}