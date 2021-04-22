## 在Zabbix-Agent端安装percona Monitoring Plugins
```
[root@Agent ~]# yum install -y http://www.percona.com/downloads/percona-release/redhat/0.1-3/percona-release-0.1-3.noarch.rpm
yum install -y https://downloads.percona.com/downloads/percona-monitoring-plugins/percona-monitoring-plugins-1.1.8/binary/redhat/7/x86_64/percona-zabbix-templates-1.1.8-1.noarch.rpm
[root@Agent ~]# yum install percona-zabbix-templates -y
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
```
[root@Agent scripts]# vim /var/lib/zabbix/percona/scripts/ss_get_mysql_stats.php
$mysql_user = 'root';
$mysql_pass = 'password';
$mysql_port = 3306;
```

## 在Zabbix-Server端上使用Zabbix_get获取值(否则会失败)
```
[root@Server ~]# zabbix_get -s 192.168.90.11 -k MySQL.pool-read-requests
223003813
```

//如果获取不到值常见问题

1. 看是否是MySQL密码错误
1. 不要直接执行脚本来获取
1. 删除/tmp/localhost-mysql_cacti_stats.txt文件
1. 权限问题导致


在Zabbix页面模板选项中导入Percona模板, 模板存放在`/var/lib/zabbix/percona/templates`， 最后关联主机即可。