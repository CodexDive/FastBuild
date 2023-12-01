#!/bin/bash

# 帮助信息
function show_help {
    echo "Usage: FastBuild [OPTION]"
    echo "Install or uninstall the web application."
    echo ""
    echo "Options:"
    echo "  --install    Install the web application."
    echo "  --uninstall  Uninstall the web application."
    echo "  --help       Show this help message."
}


work_dir="/home/mzw/FB_opensource"
frontend_dir="$work_dir/frontend"
backend_dir="$work_dir/backend"
nginx_dir="$work_dir/nginx"

github_frontend="https://github.com/CodexDive/FastBuild-Web.git"
github_backend="https://github.com/CodexDive/FastBuild-Backend.git"
fastbuild_version="release-1.0"

port="48001"



function install_main {
    #fetch_fastbuild_code
    check_environment
    install_env_requirement
    start_services
}

function fetch_fastbuild_code {
    cd $frontend_dir
    git clone -b $fastbuild_version $github_frontend
    cd $backend_dir
    git clone -b $fastbuild_version $github_backend
}


function check_environment {
    # 检查端口是否被占用
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null; then
        echo "Port $port is already in use. Please make sure it's available before running Nginx."
        exit 1
    fi

    # 检查python版本
    python_version=$(python --version 2>&1 | cut -d' ' -f2)
    if [ "$(echo "$python_version 3.7" | awk '{print ($1 >= $2)}')" -eq 1 ]; then
        echo "Python version is greater than or equal to 3.7"
    else
        echo "Python version is less than 3.7, please install python"
        exit 1
    fi
}


function install_env_requirement {
    install_nginx
    install_backend_requirement
}


function start_services {
    # 启动后端程序
    cd $backend_dir
    nohup python main.py > backend.log 2>&1 &

    # 启动Nginx前端服务
    sudo ... ... ... ... /usr/local/nginx/sbin/nginx
}


function install_nginx {
    # 检查Nginx是否已经安装
    check_ngnix
    # 安装nginx所需依赖
    install_nginx_dependents
    # 下载安装nginx
    load_install_nginx
    # 配置nginx
    configure_nginx
}
 

function check_ngnix {
    get_nginx="command -v nginx"
    if [ -x $get_nginx ]; then
        echo "nginx already exist"
        exit 1
    fi
}


function install_nginx_dependents {
    if [ -f /etc/redhat-release ]; then
        # CentOS
        sudo yum install -y gcc make zlib-devel pcre-devel openssl-devel
    elif [ -f /etc/lsb-release ]; then
        # Ubuntu
        sudo apt update
        sudo apt install -y build-essential libpcre3 libpcre3-dev libssl-dev
    else
        echo "Unsupported system"
        exit 1
    fi
}


function load_install_nginx {
    cd $nginx_dir
    wget "http://nginx.org/download/nginx-1.21.5.tar.gz"
    tar -zxvf nginx-1.21.5.tar.gz
    cd nginx-1.21.5
    ./configure --prefix=$nginx_dir
    make
    sudo make install
}


function configure_nginx {
    # 修改Nginx配置文件
    echo "server {
        listen $port;
        server_name localhost;

        location / {
            root $frontend_dir/dist;
            index index.html;
        }
    }" | sudo tee -a $nginx_dir/conf/nginx.conf

    # 创建符号链接
    nginx_sites_available="/etc/nginx/sites-available"
    nginx_sites_enabled="/etc/nginx/sites-enabled"
    ln -s $nginx_sites_available/fastbuild_frontend $nginx_sites_enabled/

    # 检查Nginx配置文件语法
    nginx -t
}


function install_backend_requirement {
    # 安装pip包
    cd $backend_dir
    pip install -r requirements.txt
}


# 安装函数
function install {
    # 拉取前端代码
    git clone $github_frontend
    cd FastBuild-Web
    # 构建前端代码
    # 这里假设您的前端代码已经构建好了，如果需要构建，请添加构建步骤

    

    # 部署前端代码到nginx
    sudo cp -r dist/* /usr/local/nginx/html/

    # 拉取后端代码
    cd ..
    git clone <backend_repository_url>
    cd backend

    # 检查端口是否被占用
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null; then
        echo "Port 8000 is already in use. Please make sure it's available before running the backend application."
        exit 1
    fi

    # 安装后端依赖
    pip install -r requirements.txt

    # 启动后端程序
    nohup python main.py > backend.log 2>&1 &

    # 前端代码路径
    frontend_path="/home/fastbuild/web/frontend"
    frontend_repository_url="<frontend_repository_url>"



    # 重启Nginx
    systemctl restart nginx

    # 启动Nginx
    sudo /usr/local/nginx/sbin/nginx

}

# 卸载函数
function uninstall {
    # 停止后端程序
    pkill -f "python main.py"

    # 停止nginx
    sudo systemctl stop nginx

    # 移除前端代码
    sudo rm -rf /var/www/html/*

    # 移除后端代码
    cd ..
    sudo rm -rf backend

    # 移除nginx
    sudo apt purge nginx -y
}

# 处理命令行参数
case "$1" in
    --install)
        install_main
        ;;
    --uninstall)
        uninstall
        ;;
    --help)
        show_help
        ;;
    *)
        echo "Invalid option: $1"
        show_help
        exit 1
        ;;
esac
