## 在Zabbix-Agent端安装percona Monitoring Plugins
```
[root@Agent ~]# rpm -ivh percona-zabbix-templates-1.1.8-1.noarch.rpm
[root@Agent ~]# yum install php php-mysql
```
## 查看percona安装后的目录结构
```
[root@Agent percona]# tree /var/lib/zabbix/percona
/var/lib/zabbix/percona
├── scripts  #脚本文件路径
│   ├── get_mysql_stats_wrapper.sh
│   └── ss_get_mysql_stats.php
└── templates
    ├── userparameter_percona_mysql.conf  #key文件位置
    └── zabbix_agent_template_percona_mysql_server_ht_2.0.9-sver1.1.6.xml #模板文件位置
```
## 将自定义监控项配置文件复制至/etc/zabbix_agentd.conf.d目录下
```
[root@Agent ~]# cp /var/lib/zabbix/percona/templates/userparameter_percona_mysql.conf  /etc/zabbix/zabbix_agentd.d/percona_mysql.conf
```
## 重启zabbix-agent
```
[root@Agent ~]# systemctl restart zabbix-agent
```
## 修改脚本中的MySQL用户名和密码
生产环境建议创建专门只读账号。
```
[root@Agent scripts]# vim /var/lib/zabbix/percona/scripts/ss_get_mysql_stats.php
$mysql_user = 'root';
$mysql_pass = 's3cret';
$mysql_port = 3306;
```

## 在Zabbix-Server端上使用Zabbix_get获取值(否则会失败)
```
[root@Agent scripts]# /var/lib/zabbix/percona/scripts/get_mysql_stats_wrapper.sh gg
405647
[root@Server ~]# zabbix_get -s 192.168.90.11 -k MySQL.pool-read-requests
223003813
```

//如果获取不到值常见问题

1. 看是否是MySQL密码错误
1. 不要直接执行脚本来获取
1. 删除/tmp/localhost-mysql_cacti_stats.txt文件
1. 权限问题导致

## 问题
1. 权限不足
```
Received value [rm: 无法删除"/tmp/localhost-mysql_cacti_stats.txt": 不允许的操作0] is not suitable for value type [Numeric (float)]

[root@Agent ~]chown -R zabbix:zabbix /tmp/localhost-mysql_cacti_stats.txt
```
2. 导入模版
```
标签无效 "/zabbix_export/date": "YYYY-MM-DDThh:mm:ssZ" 预计。

使用修改的好的监控模版 `templates/zabbix_agent_template-4.4.xml`
```
在Zabbix页面模板选项中导入Percona模板, 模板存放在`/var/lib/zabbix/percona/templates`， 最后关联主机即可。

3. 脚本获取端口问题
默认端口3306 自动生成脚本文件
```
/tmp/localhost-mysql_cacti_stats.txt
```
不使用默认端口 自动生成脚本文件
```
/tmp/localhost-mysql_cacti_stats.txt:3506
```
不使用默认端口修改脚本文件,修改两处
```
cat /var/lib/zabbix/percona/scripts/get_mysql_stats_wrapper.sh

CACHEFILE="/tmp/$HOST-mysql_cacti_stats.txt:3506"
TIMEFLM=`stat -c %Y /tmp/$HOST-mysql_cacti_stats.txt:3506`
```