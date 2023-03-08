#!/bin/bash

# 下载qbittorrent-nox并赋予可执行权限
cd /root
wget https://github.com/userdocs/qbittorrent-nox-static/releases/download/release-4.3.9_v1.2.15/x86_64-qbittorrent-nox
chmod +x x86_64-qbittorrent-nox

# 配置systemd服务
cat << "EOF" > /etc/systemd/system/qbittorrent.service
[Unit]
Description=qBittorrent Daemon Service
After=network.target

[Service]
LimitNOFILE=512000
User=root
ExecStart=/root/x86_64-qbittorrent-nox

[Install]
WantedBy=multi-user.target
EOF

# 更新配置并启动服务
systemctl daemon-reload
systemctl start qbittorrent
systemctl status qbittorrent
