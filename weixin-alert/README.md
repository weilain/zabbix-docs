# weixin-alert
# 本项目是一个企业微信消息发送的程序，可以作为运维告警使用，支持任意可调用的运维系统，包括Zabbix，Nagios，shell脚本

支持Zabbix的告警,使用方法见微信公众号
http://url.cn/4A37R4z

Zabbix告警的使用方法
# 脚本位置:
```
wget https://raw.githubusercontent.com/OneOaaS/weixin-alert/master/weixin_linux_amd64
cp weixin_linux_amd64 /etc/zabbix/alertscripts/weixin
chmod 755 /etc/zabbix/alertscripts/weixin
chown zabbix:zabbix /etc/zabbix/alertscripts/weixin
```

# 脚本测试
```
/etc/zabbix/alertscripts/weixin --corpid=wxee***********81aa --corpsecret=Mm0mHwI8iVsjA*JUGySxOFMIlbosoVEkWIEiw --msg="您好</br>告警测试" --user=oneoaas --agentid=1000003
返回数据:
{"errcode":0,"errmsg":"ok","invaliduser":""}
```

# 查看帮助
```
./weixin_linux_amd64 --help
Usage of ./weixin_linux_amd64:
  -agentid string
    	agentid
  -author string
    	http://www.oneoaas.com
  -corpid string
    	corpid
  -corpsecret string
    	corpsecret
  -msg string
    	Send Message
  -user string
    	which user to send msg
```

# 支持群组发送
```
Usage of weixin_linux_amd64_toparty:
  -agentid string
        agentid
  -author string
        http://www.oneoaas.com
  -corpid string
        corpid
  -corpsecret string
        corpsecret
  -msg string
        Send Message
  -toparty string
        which toparty to send msg
  -totag string
        which totag to send msg
  -user string
        which user to send msg

        其中toparty,totag,user三个参数任选其一发送即可
```