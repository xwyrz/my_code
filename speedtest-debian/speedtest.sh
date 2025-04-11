#!/bin/bash

# Speedtest 一键安装并测速脚本（适用于 Debian 12）
# Author: YourName
# Repo: https://github.com/xwyrz/my_code/speedtest-debian
# License: MIT

set -e

echo "📦 [1/5] 正在更新软件包..."
sudo apt update

echo "📥 [2/5] 安装必要依赖..."
sudo apt install -y curl gnupg1 apt-transport-https

echo "🌐 [3/5] 添加 Ookla Speedtest 官方软件源..."
curl -s https://install.speedtest.net/app/cli/install.deb.sh | sudo bash

echo "⚙️ [4/5] 安装 speedtest CLI 工具..."
sudo apt install -y speedtest

echo "🚀 [5/5] 开始测速..."
speedtest

# 可选：保存结果为文本
# speedtest > speedtest_result.txt

echo "✅ 测试完成！"
