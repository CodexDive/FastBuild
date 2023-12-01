"""
@Description :build任务接口文件。
@Datetime :2022/11/17 14:25:22
@Author :meizhewei
@email :meizhewei@zhejianglab.com
"""


class Response(object):
    """
    统一的json返回格式
    """
    code: int
    msg: str
    data: object

    def __init__(self, code, msg, data) -> None:
        self.code = code
        self.msg = msg
        self.data = data

    @classmethod
    def success(cls, msg='success', code=0, data=None):
        return cls(code, msg, data)

    @classmethod
    def error(cls, msg='error', code=-1, data=None):
        return cls(code, msg, data)

    def is_successful(self):
        return self.code == 0
