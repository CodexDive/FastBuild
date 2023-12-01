#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: meizhewei
@email: meizw@zhejianglab.com
@time: 2023/2/16 10:40
@desc: 
"""
import os

from utils.config_utils import system_config
# 应该位于系统配置文件中
from utils.log import Log

log = Log.ulog("file_transfer.log")


def list_source():
    # 获取可选源文件列表
    source_list = {}
    system_source_dir = system_config.get_source_dir()
    # 获取到安装器种类列表后，installer_sources_list=['yum', 'apt', 'pip', 'conda']，循环读取文件夹下内容
    installer_sources_list = os.listdir(system_source_dir)

    for installer_source in installer_sources_list:
        source_types_dir = os.path.join(system_source_dir,installer_source)
        source_types_list = os.listdir(source_types_dir)
        # 得到安装器目录，查找安装器源种类。得到source_types_list=['163', 'ali']的结果
        installer_list = []

        for source_type in source_types_list:
            source_type_dir = os.path.join(source_types_dir,source_type)
            sources_dict = {"type": source_type, "name": os.listdir(source_type_dir)}
            installer_list.append(sources_dict)
            # 写入source_list
            source_list[installer_source] = installer_list
    return {"source_list": source_list}


def list_software():
    # 获取可安装软件列表
    python_list = os.listdir(system_config.get_python_dir())
    pip_list = ["get-pip.py"]
    conda_list = os.listdir(system_config.get_conda_dir())
    software_list = {"python": python_list, "pip": pip_list, "conda": conda_list}
    return {"software_list": software_list}


async def upload_source(files):
    # 保存用户上传安装器源文件
    for file in files:
        # 1.读取文件
        contents = await file.read()
        # print("开始读取" + file.filename + "文件")
        # 2.打开文件
        source_dir = system_config.get_source_dir()
        source_filename = os.path.join(source_dir, file.filename)
        with open(source_filename, "wb") as f:
            # 3 将获取的file文件内容，写入到新文件中
            f.write(contents)
    return {"complete upload filenames": [file.filename for file in files]}


async def upload_software(file_type, files):
    if file_type == "python":
        return await upload_python(files)
    if file_type == "pip":
        return await upload_pip(files)
    if file_type == "conda":
        return await upload_conda(files)


async def upload_python(files):
    # 保存用户上传的python源码包文件
    for file in files:
        # 1.读取文件
        contents = await file.read()
        # 2.打开文件
        python_dir = system_config.get_python_dir()
        python_filename = os.path.join(python_dir, file.filename)
        with open(python_filename, "wb") as f:
            # 3 将获取的file文件内容，写入到新文件中
            f.write(contents)
    return {"complete upload filenames": [file.filename for file in files]}


async def upload_pip(files):
    # 存储用户上传安装软件文件
    for file in files:
        # 1.读取文件
        contents = await file.read()
        # 2.打开文件
        python_dir = system_config.get_pip3_dir()
        python_filename = os.path.join(python_dir, file.filename)
        with open(python_filename, "wb") as f:
            # 3 将获取的file文件内容，写入到新文件中
            f.write(contents)
    return {"complete upload filenames": [file.filename for file in files]}


async def upload_conda(files):
    # 存储用户上传安装软件文件
    for file in files:
        # 1.读取文件
        contents = await file.read()
        # 2.打开文件
        python_dir = system_config.get_conda_dir()
        python_filename = os.path.join(python_dir, file.filename)
        with open(python_filename, "wb") as f:
            # 3 将获取的file文件内容，写入到新文件中
            f.write(contents)
    return {"complete upload filenames": [file.filename for file in files]}
