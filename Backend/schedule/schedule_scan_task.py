#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@file: schedule_scan_task.py
@time: 2022/12/15 10:30
@desc: 
"""
import sched
import time

from utils.date_utils import DateUtils

s = sched.scheduler(time.time, time.sleep)


def loop_monitor():
    s.enter(50, 1, echo_system_state, ())
    s.run()


def echo_system_state():
    s.enter(50, 1, echo_system_state, ())
    print('do echo_system_state time: ', DateUtils.now_str())

