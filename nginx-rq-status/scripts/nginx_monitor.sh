#!/bin/bash
NGINX_PORT=70  #如果端口不同仅需要修改脚本即可，否则修改xml很麻烦
NGINX_COMMAND=$1

#Nginx进程监控,进程存在值为1,进程停止值为0
nginx_ping(){
    /sbin/pidof nginx 2>/dev/null | wc -l 
}
#Nginx当前活动客户端连接的数量,包括正在等待的连接
nginx_active(){
    /usr/bin/curl -s "http://127.0.0.1:"$NGINX_PORT"/nginx_status" 2>/dev/null |awk '/Active/ {print $NF}'
}
#Nginx服务器当前正在读取客户端请求头的数量
nginx_reading(){
    /usr/bin/curl -s "http://127.0.0.1:"$NGINX_PORT"/nginx_status" 2>/dev/null |awk '/Reading/ {print $2}'
}
#Nginx服务器当前正在写响应信息的数量
nginx_writing(){
    /usr/bin/curl -s "http://127.0.0.1:"$NGINX_PORT"/nginx_status" 2>/dev/null |awk '/Writing/ {print $4}'
       }
#当前有多少客户端在等待服务器响应
nginx_waiting(){
    /usr/bin/curl -s "http://127.0.0.1:"$NGINX_PORT"/nginx_status" 2>/dev/null |awk '/Waiting/ {print $6}'
       }
#Nginx已经接受客户端的连接总数量
nginx_accepts(){
    /usr/bin/curl -s "http://127.0.0.1:"$NGINX_PORT"/nginx_status" 2>/dev/null |awk 'NR==3 {print $1}'
       }
#Nginx已经处理客户端的连接总数量
nginx_handled(){
    /usr/bin/curl -s "http://127.0.0.1:"$NGINX_PORT"/nginx_status" 2>/dev/null |awk 'NR==3 {print $2}'
       }
#客户端发送的请求的总数量
nginx_requests(){
    /usr/bin/curl -s "http://127.0.0.1:"$NGINX_PORT"/nginx_status" 2>/dev/null |awk 'NR==3 {print $3}'
       }


  case $NGINX_COMMAND in
    ping)
        nginx_ping;
        ;;
    active)
        nginx_active;
        ;;
    reading)
        nginx_reading;
        ;;
    writing)
        nginx_writing;
        ;;
    waiting)
        nginx_waiting;
        ;;
    accepts)
        nginx_accepts;
        ;;
    handled)
        nginx_handled;
        ;;
    requests)
        nginx_requests;
        ;;
          *)
        echo $"USAGE:$0 {ping|active|reading|writing|waiting|accepts|handled|requests}"
    esac