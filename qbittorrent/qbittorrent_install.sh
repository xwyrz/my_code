#!/bin/bash

# 定义颜色代码
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 定义架构名称（转换为小写以统一比较）
arch=$(uname -m | tr '[:upper:]' '[:lower:]')

echo -e "${BLUE}检测系统架构...${NC}"
echo -e "当前架构: ${YELLOW}$arch${NC}"

# 根据架构名称选择架构标识
case "$arch" in
    "arm64"|"aarch64")
        arch_tag="aarch64"
        echo -e "${GREEN}检测到ARM64/aarch64架构${NC}"
        ;;
    "amd64"|"x86_64")
        arch_tag="x86_64"
        echo -e "${GREEN}检测到AMD64/x86_64架构${NC}"
        ;;
    *)
        echo -e "${RED}错误：不支持的架构类型：$arch${NC}"
        echo -e "${YELLOW}支持的架构包括: arm64/aarch64, amd64/x86_64${NC}"
        exit 1
        ;;
esac

# 选择 qBittorrent 版本
echo -e "${BLUE}请选择要安装的 qBittorrent 版本：${NC}"
echo -e "  ${GREEN}1)${NC} 4.4.5"
echo -e "  ${GREEN}2)${NC} 5.2.0"
read -rp "请输入选项 [1-2] (默认 1): " version_choice

case "$version_choice" in
    "2")
        qb_version="5.2.0"
        ;;
    "1"|"")
        qb_version="4.4.5"
        ;;
    *)
        echo -e "${RED}无效选项，默认使用 4.4.5${NC}"
        qb_version="4.4.5"
        ;;
esac

echo -e "${GREEN}已选择 qBittorrent 版本: $qb_version${NC}"

# 根据版本和架构拼接下载地址
# 说明：userdocs/qbittorrent-nox-static 的 release tag 形如 release-<qb>_v<libtorrent>
# 4.4.5 对应 libtorrent 1.2.17；5.2.0 对应 libtorrent 2.0.11
case "$qb_version" in
    "4.4.5")
        lt_version="1.2.17"
        ;;
    "5.2.0")
        lt_version="2.0.11"
        ;;
esac

base_url="https://github.com/userdocs/qbittorrent-nox-static/releases/download/release-${qb_version}_v${lt_version}"
url="${base_url}/${arch_tag}-qbittorrent-nox"

echo -e "${BLUE}下载地址: ${YELLOW}$url${NC}"

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
After=network.target network-online.target
Wants=network-online.target

[Service]
LimitNOFILE=512000
User=root
ExecStart=/root/qbittorrent-nox
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 更新配置并启动服务
echo -e "${BLUE}启动qBittorrent服务...${NC}"
systemctl daemon-reload
systemctl enable qbittorrent
systemctl start qbittorrent
echo -e "${GREEN}服务已启动${NC}"
echo -e "${YELLOW}服务状态如下：${NC}"
systemctl status qbittorrent --no-pager

echo -e "\n${GREEN}安装完成！${NC}"
echo -e "${YELLOW}已安装版本: qBittorrent $qb_version (libtorrent $lt_version)${NC}"
echo -e "${YELLOW}默认 WebUI 端口通常为: 8080${NC}"
echo -e "${YELLOW}默认用户名: admin , 默认密码: adminadmin (新版本可能在日志中生成临时密码，请留意上方状态栏)${NC}"
