# 简介

> 本项目用于快速构建镜像

# 启动命令
> docker run --rm  -v /var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker -v /mnt/nas_self-define/fastbuild:/mnt/nas_self-define/fastbuild  -p 8001:8001  -itd  10.101.12.128/project/fastbuild:1.0 

# 基础环境镜像
> 10.101.12.128/project/fastbuild_base_image:1.0

 调试命令
>docker run --rm --name fastbuild -v /var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker -v /mnt/nas_self-define/meizhewei/fastbuild:/mnt/nas_self-define/meizhewei/fastbuild -v /home/mzw/fastbuild:/home/fastbuild -p 8001:8001 -itd 10.101.12.128/project/fastbuild_base_image:1.0 
# 服务镜像
> 10.101.12.128/project/fastbuild:1.0

# 服务访问地址

[访问地址](http://127.0.0.1:18002/docs#)

# 容器化服务构建
使用服务镜像，启动服务。

# 宿主机非容器化环境搭建
## 前提
> 本软件的部署基于ubuntu18.04操作系统，且需要包含sqlite3驱动的python。
> 
> 若无python，可根据以下步骤进行安装。
## 基础环境
> from ubuntu:18.04 
> 
> apt-get update
## 安装python3.7.14
> 从官网下载python安装包 Python-3.7.14.tgz 到服务器/tmp目录，解压后开始安装
```bash
tar -zxvf Python-3.7.14.tgz
cd Python-3.7.14
# 在ubuntu18.04上安装: 
apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev
./configure --prefix=/usr/local/python3.7 --enable-loadable-sqlite-extensions --enable-shared
make -j 6 && make install
echo /usr/local/python3.7/lib/ >> /etc/ld.so.conf
/sbin/ldconfig
rm -rf /usr/local/bin/python
ln -s /usr/local/python3.7/bin/python3.7 /usr/local/bin/python
rm -rf /usr/local/bin/pip
ln -s /usr/local/python3.7/bin/pip3.7 /usr/local/bin/pip
```
### 配置环境变量启动顺序
```bash
vim /etc/profile
# 增加环境变量
export PATH="/usr/local/python3.7/bin/:$PATH"
# 生效环境变量
source /etc/profile
# 测试
python -V
```
## 安装虚拟环境 virtualenv
> pip3 install virtualenv -i https://pypi.tuna.tsinghua.edu.cn/simple/

## 安装服务
> 拷贝最新代码，到服务器目录
> 
> 在同级目录下，创建虚拟环境
```bash
virtualenv -p python3.7 fastbuild_virtualenv
cd fastbuild_virtualenv/
source bin/activate
```
### 安装依赖

> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

### 添加systemd守护进程
> cp Fastbuild/fastbuild.sercice /etc/systemd/system/

修改fastbuild.sercice配置文件中的路径
```bash
[Unit]
Description=FastBuild Service, A Tool used for building Docker Images quickly which can handle Source Management, Python Environment Management, Package dependency Management, at the same time, can also handle virtual environment management.
After=network.service
[Service]
Type=simple
User=root
Group=root
# 更新main.py所在目录
WorkingDirectory=/home/fastbuild/FastBuild
# 更新为虚拟环境所在python /home/fastbuild/FastBuild/fastbuild_virtualenv/bin/python
ExecStart=/home/fastbuild/FastBuild/fastbuild/bin/python main.py
Restart=always
[Install]
WantedBy=multi-user.target
```
### 生效守护进程
```bash
systemctl restart fastbuild
systemctl daemon-reload
systemctl enable fastbuild
```
## 快捷进入虚拟环境
```bash
~/.bashrc
# 在下面加如下参数
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias fb='cd /home/fastbuild/FastBuild; source fastbuild_virtualenv/bin/activate'
# 生效
source ~/.bashrc
```
