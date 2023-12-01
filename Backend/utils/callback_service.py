#!/usrstate=Noneython
# -*- coding:UTF-8 -*-

"""
@author: songquanheng
@email: wannachan@outlook.com
@time: 2023/3/17 18:35
@desc: 用于与回调服务进行接口交互
"""
import threading
import time

import requests

from utils.response import Response


class CallBackService:
    """回调服务"""

    @staticmethod
    def post_state(state, callback_url):
        thread_name = f"回调函数{state['taskId']}线程"
        threading.Thread(target=CallBackService.state_upload, args=(state, callback_url),
                         name=thread_name).start()
        return Response.success(msg=f"{thread_name}，请等待回调结束", data=state)

    @staticmethod
    def state_upload(state, url):
        """
        :param url: 回调url
        :param state: 镜像构建任务状态字典，包含任务id，镜像名称，镜像状态，url
        """
        i = 0
        while True:
            i += 1

            headers = {"X-BizType": "DROS", "X-Login-UserId": "1", "Content-Type": "application/json"}
            response = requests.post(url, headers=headers, json=state)
            print(f"尝试第{i}次镜像状态上报. response{response.status_code}")
            if CallBackService.success(response):
                break
            if i > 10:
                print("状态上报已发送11次，状态上报失败")
                break
            time.sleep(60)

    @staticmethod
    def success(response):
        return response.status_code == 200
