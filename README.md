# FastBuild

This project is designed to build docker image.

Moreover, it addresses issues such as high knowledge barriers, inconvenience, and lack of speed.


# Install

Step1. git clone https://github.com/CodexDive/FastBuild.git

Step2. cd FastBuild

Step3. By default, use the fb-test.ini configuration file. Please modify the path, port, and IP address in it    & 配置个人dockerhub仓库/harbor

Step4. Copy source and tools to the location specified by fb-test.ini

Step5. bash fastbuid.sh --install


若要手动重启服务：
删除后端端口、进程：
先查询 netstat -anop |grep 40002
ps -ef |grep main.py

重启前端：
找到nginx目录
./sbin/nginx -s reload
