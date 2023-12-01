"""
@Description :dockerfile中的操作命令转换函数,如from，run，copy等。
@Datetime :2022/11/17 14:25:22
@Author :梅哲炜
@email :meizhewei@zhejianglab.com
"""


class DockerfileCommandGenerator:
    """dockerfile中的方法"""

    @staticmethod
    def from_command(image_name: str) -> str:
        """镜像来源"""
        return "FROM %s" % image_name + "\n"

    @staticmethod
    def maintainer_command(maintainer_desc: str):
        """镜像作者"""
        return "MAINTAINER %s" % maintainer_desc + "\n"

    @staticmethod
    def label(key: str, value: str):
        """为镜像指定标签"""
        assert key, "在Dockerfile语法中，LABEL key不允许为空"
        assert value, "在Dockerfile语法中，LABEL value不允许为空"
        return "LABEL %s=%s" % (key, value) + "\n"

    def add(self):
        """
        复制一个文件或压缩文件，也可以是url，类似于wget。
        如果是一个文件目录，会复制目录下的文件，不会复制目录本身
        """

    def copy(self):
        """复制一个文件，COPY的只能是本地文件，其他用法与add一致。"""

    def expose(self):
        """暴漏容器运行时的监听端口给外部。"""

    def env(self):
        """设置环境变量"""

    def run(self):
        """
        运行指定的命令
        1. RUN <command>
        2. RUN ["executable", "param1", "param2"]
        第一种后边直接跟shell命令
        在linux操作系统上默认 /bin/sh -c
        在windows操作系统上默认 cmd /S /C
        第二种是类似于函数调用。
        可将executable理解成为可执行文件，后面就是两个参数。
        """

    @staticmethod
    def bash_shell():
        return "SHELL [\"/bin/bash\", \"-c\"]" + "\n"

    def cmd(self):
        """容器启动时的默认命令或参数
        CMD ["executable","param1","param2"]
        CMD ["param1","param2"]
        CMD command param1 param2
        """

    def entrypoint(self):
        """
        容器启动时运行的启动命令
        ENTRYPOINT ["executable", "param1", "param2"]
        ENTRYPOINT command param1 param2
        ENTRYPOINT [ "/bin/bash", "-c", "/etc/init.d/ssh start && /usr/local/bin/jupyter-lab --allow-root" ]
        """

    def volume(self):
        """挂载宿主机的目录到容器中"""

    def user(self):
        """
        设置容器启动后的内部用户
        USER daemo
        USER UID
        """

    @staticmethod
    def workdir(work_dir):
        """设置工作目录，对RUN,CMD,ENTRYPOINT,COPY,ADD生效。如果不存在则会创建，也可以设置多次。"""
        return f"WORKDIR {work_dir}" + "\n"

    def arg(self):
        """
        在容器build过程中使用的参数，可通过--build-arg =来指定参数
        FROM busybox
        ARG user1
        ARG build=1
        """
