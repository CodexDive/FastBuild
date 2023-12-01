#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# author: songquanheng
# email: wannachan@outlook.com
# date: 2022/10/19 周三 15:54:16
# description: 日期时间类

from datetime import datetime


class DateUtils:
    """日期时间的辅助类"""

    @staticmethod
    def now_str():
        now = datetime.now()
        return now.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def now_str_in_millis():
        now = datetime.now()
        return now.strftime('%Y-%m-%d-%H-%M-%S-%f')

    @staticmethod
    def now_date():
        return datetime.now().strftime('%Y-%m-%d')

    @staticmethod
    def timestamp_in_millis(now: datetime):
        return int(datetime.timestamp(now) * 1000)

    @staticmethod
    def duration_in_millis(start_time: datetime, end_time: datetime):
        assert isinstance(start_time, datetime)
        assert isinstance(end_time, datetime)
        if start_time < end_time:
            return DateUtils.timestamp_in_millis(end_time) - DateUtils.timestamp_in_millis(start_time)

        return DateUtils.timestamp_in_millis(start_time) - DateUtils.timestamp_in_millis(end_time)


if __name__ == '__main__':
    print(DateUtils.now_str())
