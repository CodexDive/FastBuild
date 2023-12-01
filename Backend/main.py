# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Filename :main.py
@Description :
@Datetime :2022/11/17 14:25:22
@Author :meizhewei
@email :meizhewei@zhejianglab.com
@desc : main主入口程序，控制所有的router，并且配置程序端口
"""
import os
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from controller import hello, db_controller, task_controller, image_controller, file_controller, \
    db_check_result_controller, progress_controller, image_life_controller
from db.db_element import engine, Base
from utils.config_utils import host_config, system_config
from utils.prepare import Prepare
from utils.schedule_service import add_schedule_service, scheduler

file = Path(__file__)
sys.path.append(str(file.parent.parent))

description = """
    FastBuild is a docker image automatic and rapid construction software.
"""

app = FastAPI(
    title="FastBuild",
    description=description,
    version="0.0.1",
)

origins = ["*"]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,  # 设置允许的origins来源
                   allow_credentials=True,
                   allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
                   allow_headers=["*"])  # 允许跨域的headers，可以用来鉴别来源等作用。

app.include_router(hello.router)
app.include_router(db_controller.router)
app.include_router(task_controller.router)
app.include_router(image_controller.router)
app.include_router(file_controller.router)
app.include_router(db_check_result_controller.router)
app.include_router(progress_controller.router)
app.include_router(image_life_controller.router)
# 自动创建sqlite表
Base.metadata.create_all(bind=engine)

app.mount("/task", StaticFiles(directory=(system_config.get_task_dir())), name="static_files")

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log")
app.mount("/sys_log", StaticFiles(directory=log_dir), name="static_log_files")

@app.get("/api/fast-build/")
async def root():
    return {"message": "Welcome To FastBuild"}


@app.on_event("startup")
async def scan():
    """添加了定时任务数据条目扫描程序"""
    print("启动应用程序")
    add_schedule_service()
    scheduler.start()
    print("FastBuild 启动成功")

@app.on_event("startup")
async def prepare():
    """添加数据初始化准备程序"""
    print("启动 预置数据导入 程序")
    Prepare().prepare_images()
    print("FastBuild 预置数据导入完成")

@app.on_event("shutdown")
async def shutdown_event():
    print("关闭应用程序")
    scheduler.remove_all_jobs()


@app.get("/api/fast-build/stop")
async def stop():
    print("stop service")


if __name__ == '__main__':
    print("FastBuild 启动ing")
    uvicorn.run(app='main:app', host="0.0.0.0",
                port=int(host_config.port), reload=True, debug=True)
