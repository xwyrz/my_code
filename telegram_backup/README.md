
Telegram 联系人备份
脚本需要python3环境，具体安装教程自行搜索。

测试环境 Ubuntu 18.04.5 LTS & Python 3.6.9

前提

从 https://my.telegram.org/apps 获取自己的Telegram API密钥。

下载脚本

git clone https://github.com/snow922841/telegram_backup.git

使用

进入脚本目录
cd telegram_backup
安装依赖
pip3 install -r requirements.txt
修改telegram_backup.py文件内的 api_id 和 api_hash 为你自己的

运行

python3 telegram_backup.py
按照提示输入telegram绑定的手机号获取验证码并输入

