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


work_dir=$(pwd)
frontend_dir="$work_dir/Web"
backend_dir="$work_dir/Backend"
nginx_dir="$work_dir/nginx"
nginx_setup="$nginx_dir/setup"
mkdir -p $nginx_setup

port="48001"



function install_main {
    check_environment
    install_env_requirement
    start_services
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
    nohup python $backend_dir/main.py > Fastbuild_Backend.log 2>&1 &
    # 启动Nginx前端服务
    $nginx_dir/sbin/nginx -s reload
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
    cd $nginx_setup
    wget "http://nginx.org/download/nginx-1.21.5.tar.gz"
    tar -zxvf nginx-1.21.5.tar.gz
    cd nginx-1.21.5
    ./configure --prefix=$nginx_dir --user=fastbuild --group=fastbuild --with-http_ssl_module --with-http_stub_status_module --with-http_gzip_static_module --with-pcre
    make
    sudo make install
}


function configure_nginx {
    # 修改Nginx配置文件
    sed -i "$i\
    server {\
        listen $port;\
        server_name localhost;\
        \
        location / {\
            root $frontend_dir/dist;\
            index index.html;\
        }\
        location /api {\
            proxy_pass  http://127.0.0.1:40002;\
        }\
    }" $nginx_dir/conf/nginx.conf


    # 检查Nginx配置文件语法
    $nginx_dir/sbin/nginx -t
}


function install_backend_requirement {
    # 安装pip包
    cd $backend_dir
    pip install -r requirements.txt
}


# 卸载函数
function uninstall {
    # 停止后端程序
    pkill -f "python $backend_dir/main.py"

    # 移除nginx
    sudo rm -rf $nginx_dir $nginx_setup
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
