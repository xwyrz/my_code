#!/bin/bash

# 一键安装 & 使用 Ookla speedtest CLI（官方推荐方式）

set -e

echo "📦 正在更新软件包..."
sudo apt update

echo "📥 安装 curl..."
sudo apt install -y curl

echo "🌐 添加 Ookla 官方仓库（packagecloud.io）..."
curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | sudo bash

echo "⚙️ 安装 speedtest CLI..."
sudo apt install -y speedtest

echo "🚀 开始测速..."
speedtest

echo "✅ 测试完成！"
