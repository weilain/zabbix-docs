#!/bin/bash
exe_path=/usr/bin/redis-cli
R_COMMAND="$1"
R_PORT="3333"  #根据实际情况调整端口
R_SERVER="172.16.48.31"  #根据具体情况调整IP地址
PASSWD=""    #如果没有设置Redis密码,为空即可
redis_ping(){
    $exe_path -h $R_SERVER -p $R_PORT  ping | grep -c PONG
}
redis_maxclients(){
    $exe_path -h $R_SERVER -p $R_PORT  CONFIG GET maxclients |sed -n '2p'
}
redis_status(){
   (echo -en "AUTH $PASSWD\r\nINFO\r\n";sleep 1;) | /usr/bin/nc "$R_SERVER" "$R_PORT" > /tmp/redis_"$R_PORT".tmp
      REDIS_STAT_VALUE=$(grep "$R_COMMAND:" /tmp/redis_"$R_PORT".tmp | cut -d ':' -f2)
       echo "$REDIS_STAT_VALUE"
}

case $R_COMMAND in
    redis_ping)
    redis_ping;
    ;;
    redis_maxclients)
    redis_maxclients;
    ;;
    used_cpu_user_children)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    used_cpu_sys)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    total_commands_processed)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    role)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    lru_clock)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    latest_fork_usec)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    keyspace_misses)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    keyspace_hits)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    keys)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    expires)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    expired_keys)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    evicted_keys)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    connected_clients)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    changes_since_last_save)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    bgsave_in_progress)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    used_memory_peak)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    used_memory)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    used_cpu_user)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    used_cpu_sys_children)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    db0)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    db1)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    db2)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    db3)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    db4)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    db5)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    total_connections_received)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    redis_version)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    uptime_in_seconds)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    used_memory_rss)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    used_memory_lua)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    rdb_last_bgsave_status)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    aof_last_bgrewrite_status)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    aof_last_write_status)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    total_net_output_bytes)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    total_net_input_bytes)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    redis_mode)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    client_recent_max_input_buffer)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    client_recent_max_output_buffer)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    blocked_clients)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    loading)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    rdb_bgsave_in_progress)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    rdb_changes_since_last_save)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    rdb_current_bgsave_time_sec)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    rdb_last_save_time)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    aof_enabled)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    pubsub_channels)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    pubsub_patterns)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    master_host)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    master_link_status)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    master_port)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    rdb_last_cow_size)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    instantaneous_ops_per_sec)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    total_system_memory)
    redis_status "$R_PORT" "$R_COMMAND"
    ;;
    *)
    echo $"USAGE:$0 {redis_maxclients|redis_ping|total_system_memory|redis_version|instantaneous_ops_per_sec|rdb_last_cow_size|master_host|master_link_status|master_port|pubsub_patterns|pubsub_channels|aof_enabled|rdb_last_save_time|rdb_last_bgsave_time_sec|rdb_last_bgsave_status|rdb_current_bgsave_time_sec|rdb_changes_since_last_save|rdb_bgsave_in_progress|loading|client_recent_max_output_buffer|redis_mode|client_recent_max_input_buffer|used_memory_lua|total_net_output_bytes|total_net_input_bytes|uptime_in_seconds|aof_last_bgrewrite_status|used_memory_rss|used_cpu_user_children|db0|db1|db2|db3|db4|db5|used_cpu_sys|total_commands_processed|role|lru_clock|latest_fork_usec|keyspace_misses|keyspace_hits|keys|expires|expired_keys|connected_clients|changes_since_last_save|blocked_clients|used_memory_peak|used_memory|used_cpu_user|used_cpu_sys_children|total_connections_received}"
    esac
