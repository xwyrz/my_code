#!/bin/bash

# 检查当前系统类型
if [ -f /etc/debian_version ]; then
    # Debian/Ubuntu 系统
    echo "Debian/Ubuntu 系统，安装 tcptraceroute..."
    sudo apt update
    sudo apt install -y tcptraceroute
elif [ -f /etc/redhat-release ]; then
    # RHEL/CentOS 系统
    echo "RHEL/CentOS 系统，安装 tcptraceroute..."
    sudo yum install -y tcptraceroute
else
    echo "未识别的操作系统类型，请手动安装 tcptraceroute。"
    exit 1
fi

# 下载并安装 tcping
echo "下载并安装 tcping..."
sudo wget http://www.vdberg.org/~richard/tcpping -O /usr/bin/tcping
sudo chmod +x /usr/bin/tcping

# 完成
echo "安装完成！可以使用 tcping 命令了。"
