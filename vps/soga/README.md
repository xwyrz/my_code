v2b
v2board后端sosga一键脚本

原脚本：

bash <(curl -Ls https://raw.githubusercontent.com/sprov065/soga/master/install.sh)
自己备份：

bash <(curl -Ls https://raw.githubusercontent.com/gugd123/v2b/master/install%20.sh)
、同步时间为北京时间：一般不需要，保险起见，建议还是同步一下。

1：yum -y install ntpdate
2：timedatectl set-timezone Asia/Shanghai
3：ntpdate ntp1.aliyun.com
3、关闭防火墙：必须要做，否则大部分对接上节点但是连接都会无网络连接。

1：systemctl start supervisord
2：systemctl disable firewalld
3：systemctl stop firewalld
1、按照前面的添加好节点，把防火墙或时间同步下，这里就不加上了，输入下列命令安装soga；

bash <(curl -Ls https://raw.githubusercontent.com/sprov065/soga/master/install.sh)
2、安装好后命令行输入：vi /etc/soga/soga.conf 编辑以下几个地方（面板类型、面板域名、通信密钥、节点ID），其它根据自身需求配置；

type=v2board       ## 对接的面板类型，可选v2board/sspanel/vnetpanel
server_type=v2ray  ## 对接的节点类型，可选v2ray/trojan
api=webapi         ## 对接的方式，可选webapi 或 db，表示 webapi 对接或数据库对接
 
##webapi 对接
webapi_url=https://zhujiget.com/  ## 面板域名地址，或自定义个专用后端对接不提供访问的域名
webapi_mukey=zhujigetcom666666    ## 面板设置的通讯密钥
 
##数据库对接
db_host=db.xxx.com  ## 数据库地址
db_port=3306  ## 数据库端口
db_name=name  ## 数据库名
db_user=root  ## 数据库用户名
db_password=asdasdasd  ## 数据库密码
 
node_id=1   ## 前端节点id
soga_key=  ## 授权密钥，社区版无需填写，最多支持88用户，商业版无限制
user_conn_limit=0  ## 限制用户连接数，0代表无限制，v2board 必填！！！
user_speed_limit=0   ## 用户限速，0代表无限制，单位 Mbps，v2board 必填！！！
check_interval=100   ## 同步前端用户、上报服务器信息等间隔时间（秒），近似值
force_close_ssl=false ## 设为true可强制关闭tls，即使前端开启tls，soga也不会开启tls，方便用户自行使用nginx、caddy等反代
forbidden_bit_torrent=true  ## 设为true可禁用bt下载
default_dns=8.8.8.8,1.1.1.1  ## 配置默认dns，可在此配置流媒体解锁的dns，以逗号分隔
3、编辑好自己需要的设置后保存退出，命令行输入soga，输入数字4启动soga，可输入7或8查看状态和日记，没意外的话面板已经亮灯了，自行测试是否能上网；
