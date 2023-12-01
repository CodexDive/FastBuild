#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/3/2 14:00
@desc: 
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from utils.config_utils import db_config

__all__ = ["engine", "Session", "Base"]

engine = create_engine(db_config.get_db_file(), connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
