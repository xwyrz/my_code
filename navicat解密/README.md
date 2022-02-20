解密 Navicat 保存的数据库密码
 
将 mysql 的密码保存到了 Navicat ，忘记了之前的密码是多少，遂 Google 了一番。

经过查看网络上的分析可知，Navicat 使用 AES 加密，加密模式为 AES-CBC，密钥为：libcckeylibcckey，向量 IV 为 libcciv libcciv ，注意后边还有一个空格。

加密的密码保存位置可以在 Navicat -> 文件 -> 导出连接 中导出的 ncx 文件中找到。

或者可以在注册表中 HKEY_CURRENT_USER\Software\PremiumSoft\Navicat\Servers\你的连接 中对应 ip 地址中 Pwd 键值中找到。

部分代码参考自： https://github.com/DoubleLabyrinth/how-does-navicat-encrypt-password
