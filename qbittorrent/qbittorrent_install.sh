#!/bin/bash

# 定义颜色代码
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 定义架构名称
arch="$(uname -m)"

echo -e "${BLUE}检测系统架构...${NC}"
echo -e "当前架构: ${YELLOW}$arch${NC}"

# 根据架构名称选择下载地址
if [ "$arch" == "arm64" ] || [ "$arch" == "aarch64" ]; then
  url="https://github.com/userdocs/qbittorrent-nox-static/releases/download/release-4.4.5_v2.0.8/arm64-qbittorrent-nox"
  echo -e "${GREEN}检测到ARM64/aarch64架构${NC}"
elif [ "$arch" == "armhf" ]; then
  url="https://github.com/userdocs/qbittorrent-nox-static/releases/download/release-4.4.5_v2.0.8/armhf-qbittorrent-nox"
  echo -e "${GREEN}检测到ARMHF架构${NC}"
elif [ "$arch" == "amd64" ] || [ "$arch" == "x86_64" ]; then
  url="https://github.com/userdocs/qbittorrent-nox-static/releases/download/release-4.4.5_v2.0.8/x86_64-qbittorrent-nox"
  echo -e "${GREEN}检测到AMD64/x86_64架构${NC}"
else
  echo -e "${RED}错误：不支持的架构类型：$arch${NC}"
  exit 1
fi

# 下载qbittorrent-nox并赋予可执行权限
echo -e "${BLUE}开始下载qBittorrent...${NC}"
cd /root || { echo -e "${RED}错误：无法进入/root目录${NC}"; exit 1; }
wget "$url" -O qbittorrent-nox || { echo -e "${RED}错误：下载失败${NC}"; exit 1; }
chmod +x qbittorrent-nox
echo -e "${GREEN}下载完成并设置可执行权限${NC}"

# 配置systemd服务
echo -e "${BLUE}配置systemd服务...${NC}"
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
echo -e "${BLUE}启动qBittorrent服务...${NC}"
systemctl daemon-reload
systemctl start qbittorrent
echo -e "${GREEN}服务已启动${NC}"
echo -e "${YELLOW}服务状态如下：${NC}"
systemctl status qbittorrent --no-pager

echo -e "\n${GREEN}安装完成！${NC}"
