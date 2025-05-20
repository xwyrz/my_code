#!/bin/bash

# 检查是否为 root 用户
if [ "$(id -u)" -ne 0 ]; then
    echo "请使用 root 用户或 sudo 运行此脚本！"
    exit 1
fi

echo "===== 开始清理 systemd 日志并设置限制 ====="

# 1. 查看当前日志占用情况
echo -e "\n📊 当前日志占用空间："
journalctl --disk-usage

# 2. 清理日志（保留最近 1 周的日志）
echo -e "\n🧹 清理日志，只保留最近 7 天的日志..."
journalctl --vacuum-time=7days

# 3. 修改 journald 配置，限制日志大小（100MB，1 周）
echo -e "\n⚙️ 设置日志限制：最大 100MB，最多保留 7 天..."
mkdir -p /etc/systemd/journald.conf.d
cat > /etc/systemd/journald.conf.d/00-limits.conf <<EOF
[Journal]
SystemMaxUse=100M
RuntimeMaxUse=100M
MaxRetentionSec=1week
EOF

# 4. 重启 journald 服务
echo -e "\n🔄 重启 systemd-journald 服务..."
systemctl restart systemd-journald

# 5. 检查是否生效
echo -e "\n✅ 清理完成！当前日志占用："
journalctl --disk-usage

echo -e "\n✨ 已设置日志限制："
grep -E "SystemMaxUse|RuntimeMaxUse|MaxRetentionSec" /etc/systemd/journald.conf.d/00-limits.conf

echo -e "\n===== 操作完成！====="
