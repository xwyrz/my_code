#!/bin/bash

# 定义架构名称
arch="$(uname -m)"

# 根据架构名称选择下载地址
if [ "$arch" == "arm64" ] || [ "$arch" == "aarch64" ]; then
  url="https://github.com/userdocs/qbittorrent-nox-static/releases/download/release-4.4.5_v2.0.8/arm64-qbittorrent-nox"
elif [ "$arch" == "armhf" ]; then
  url="https://github.com/userdocs/qbittorrent-nox-static/releases/download/release-4.4.5_v2.0.8/armhf-qbittorrent-nox"
elif [ "$arch" == "amd64" ] || [ "$arch" == "x86_64" ]; then
  url="https://github.com/userdocs/qbittorrent-nox-static/releases/download/release-4.4.5_v2.0.8/x86_64-qbittorrent-nox"
else
  echo "不支持的架构类型：$arch"
  exit 1
fi

# 下载qbittorrent-nox并赋予可执行权限
cd /root || { echo "无法进入/root目录"; exit 1; }
wget "$url" -O qbittorrent-nox || { echo "下载失败"; exit 1; }
chmod +x qbittorrent-nox

# 配置systemd服务
cat << "EOF" > /etc/systemd/system/qbittorrent.service
[Unit]
Description=qBittorrent Daemon Service
After=network.target

[Service]
LimitNOFILE=512000
User=root
ExecStart=/root/qbittorrent-nox

[Install]
WantedBy=multi-user.target
EOF

# 更新配置并启动服务
systemctl daemon-reload
systemctl start qbittorrent
systemctl status qbittorrent
