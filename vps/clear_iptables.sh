#!/bin/bash
# 一键清空 iptables 规则并持久化（无需重启）

echo "🛑 正在清空 iptables 规则..."

# 1. 设置默认策略为 ACCEPT
sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD ACCEPT
sudo iptables -P OUTPUT ACCEPT

# 2. 清空所有规则和自定义链
sudo iptables -F
sudo iptables -X

# 3. 清空 NAT 表
sudo iptables -t nat -F

# 4. 清空 mangle 表（可选，确保彻底）
sudo iptables -t mangle -F

echo "✅ 当前 iptables 规则已清空"

# 5. 安装 iptables-persistent（如果未安装）
if ! command -v iptables-save &> /dev/null; then
    echo "📦 正在安装 iptables-persistent..."
    sudo apt update -qq
    sudo apt install iptables-persistent -y
fi

# 6. 保存规则到持久化文件
echo "💾 正在保存规则到持久化文件..."
sudo iptables-save | sudo tee /etc/iptables/rules.v4 > /dev/null
sudo ip6tables-save | sudo tee /etc/iptables/rules.v6 > /dev/null 2>/dev/null

# 7. 立即加载持久化规则（确保当前生效）
sudo iptables-restore < /etc/iptables/rules.v4 2>/dev/null

echo "✅ 完成！当前规则如下："
echo "─────────────────────────"
sudo iptables -L -n -v --line-numbers | head -20
echo "─────────────────────────"
echo "🎉 所有端口已放开，规则已持久化，无需重启"
