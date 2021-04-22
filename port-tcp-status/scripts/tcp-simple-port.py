#!/usr/bin/python
import os
import json
#cmd=os.popen(""" netstat -nlpt|grep -v -w -|grep -v rpc|awk -F "[ :]+" '{if($4 ~ /0.0.0.0/ || $4 ~ /127.0.0.1/) print $5}'""")
cmd=os.popen(""" netstat -nlpt|grep -v -w -|grep -v rpc | awk '{print $4}' | awk -F : '{print $4}'""")
ports=[]
for port in cmd.readlines():
    r=port.strip()
    ports += [{"{#PORT}":r}]

#data =  json.dumps(ports,separators=(',',':'),encoding = 'gbk', ensure_ascii=True)
data =  json.dumps(ports,separators=(',',':'), ensure_ascii=True)
print (data)