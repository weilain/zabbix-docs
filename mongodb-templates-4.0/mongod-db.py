#!/usr/bin/python
#
from __future__ import print_function
import sys, getopt
from pyzabbix import ZabbixMetric, ZabbixSender
from pymongo import MongoClient
import time
import subprocess
import re
import urllib

ZBSERVER = 'localhost'
ZBPORT = 10051

try:
    opts, args = getopt.getopt(sys.argv[1:],"h:n:p:u:s:")
except getopt.GetoptError:
    print ("Usage:\nmongod-db.py -h <hostname or ip mongod is listening to> -n <hostname in zabbix> -u <user> -s <secret pass> -p <mongod port>")
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        mongohost = arg
    elif opt == '-n':
        zbhost = arg.strip()
    elif opt == '-p':
        mongoport = arg
    elif opt == '-u':
        muser = arg
    elif opt == '-s':
        mpass = arg

arg = "-u " + muser + " -p " + mpass + " -h " + mongohost + ":" + mongoport + " --authenticationDatabase=admin --rowcount 1 --noheaders"
cmd = ['mongostat', "-u", muser, "-p", mpass, "-h", mongohost + ":" + mongoport, "--authenticationDatabase=admin", "--rowcount", "1", "--noheaders"]
r = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = r.communicate()
res = out + err

#print("DEBUG: STR: " + arg)
#print("DEBUG: RES: " + res)
#print("DEBUG: ERR: " + err + str(len(err)))

state = 0
if len(err) > 0:
    packet = [ ZabbixMetric(zbhost, 'mongodb_state', state),
        ZabbixMetric(zbhost, 'mongodb_errstr', err) ]
    result = ZabbixSender(zabbix_port = ZBPORT, zabbix_server = ZBSERVER).send(packet)
    print(err)
    sys.exit(1)
res = res.rstrip()
res = res.replace('*','')
res = re.sub("^ +","",res)
arr = re.split(" +", res)

def str_to_int(s):
    m = re.match('(\d+)(\[a-z]|[A-Z])', s)
    r = re.match('(\d+).(\d+)(\[a-z]|[A-Z])', s)
    if r:
        m = r
    if m:
        i = int(m.group(1))
        if m.group(2) == 'k':
            i = i * 1000
        elif m.group(2) == 'm':
            i = i * 1000 * 1000
    else:
        try:
            i = int(s)
        except:
            i = 0
    return i

def str_to_bytes(s):
    m = re.match('(\d+)(\[a-z]|[A-Z])', s)
    r = re.match('(\d+).(\d+)(\[a-z]|[A-Z])', s)
    if r:
        m = r
    if m:
        i = int(m.group(1))
        if m.group(2) == 'k' or m.group(2) == 'K':
            i = i * 1024
        elif m.group(2) == 'm' or m.group(2) == 'M':
            i = i * 1024 * 1024
        elif m.group(2) == 'g' or m.group(2) == 'G':
            i = i * 1024 * 1024 * 1024
    else:
        try:
            i = int(s)
        except:
            i = 0
    return i

if len(arr) < 18:
    err = 'Unknown error!'
    packet = [ ZabbixMetric(zbhost, 'mongodb_state', state),
        ZabbixMetric(zbhost, 'mongodb_errstr', err) ]
    result = ZabbixSender(zabbix_port = ZBPORT, zabbix_server = ZBSERVER).send(packet)
    print(err)
    sys.exit(1)

# Human readable names for better understanding
insert, query, update, delete, getmore, command, dirty, used, flushes, vsize, resm, qr, ar, netin, netout, conn, rset, repl = arr[:18]
# Add known opcounters to zabbix packet
err = 'OK'
state = 1
packet = [ ZabbixMetric(zbhost, 'mongodb_state', state),
        ZabbixMetric(zbhost, 'mongodb_errstr', err) ]
conn = str_to_int(conn)
packet.append(ZabbixMetric(zbhost, "mongodb_conn", conn))
packet.append(ZabbixMetric(zbhost, "mongodb_rs_name", rset))
packet.append(ZabbixMetric(zbhost, "mongodb_rs_status", repl))
m = re.match('(\d+)\|(\d+)',ar)
if m:
    ar = m.group(1)
    aw = m.group(2)
else:
    ar = 0
    aw = 0
packet.append(ZabbixMetric(zbhost, "mongodb_aclients_read", ar))
packet.append(ZabbixMetric(zbhost, "mongodb_aclients_write", aw))
vsize = str_to_bytes(vsize)
packet.append(ZabbixMetric(zbhost, "mongodb_vsize", vsize))
netin = str_to_bytes(netin)
packet.append(ZabbixMetric(zbhost, "mongodb_netin", netin))
netout = str_to_bytes(netout)
packet.append(ZabbixMetric(zbhost, "mongodb_netout", netout))

# Read saved opcounters from previous check
try:
    f = open("/tmp/" + mongohost + "-opcounters")
    s = f.read()
    f.close()
    ts, insert, update, delete, query, getmore, command = s.split(" ")
except Exception as e:
    ts, insert, update, delete, query, getmore, command = [1,0,0,0,0,0,0]
    print(e)

print("History opcounters")
print(ts, insert, update, delete, query, getmore, command)

# Get serverStatus stats
try:
    mo = MongoClient('mongodb://' + muser + ':' + urllib.quote(mpass) + '@' + mongohost + ':' + mongoport + '/admin', connectTimeoutMS=5000)
except Exception as e:
    print ('Can\'t connect to '+mongohost) 
    print ("ERROR:", e)
    sys.exit(1)
res = mo.admin.command('serverStatus')
now = time.time()
#$zab->send("mongodb_insert", int(($res->{opcounters}->{insert} - $insert)/(($now-$ts)/60)));
packet.append(ZabbixMetric(zbhost, "mongodb_insert", int((float(res['opcounters']['insert']) - float(insert))/((now - float(ts))/60))))
packet.append(ZabbixMetric(zbhost, "mongodb_update", int((float(res['opcounters']['update']) - float(update))/((now - float(ts))/60))))
packet.append(ZabbixMetric(zbhost, "mongodb_delete", int((float(res['opcounters']['delete']) - float(delete))/((now - float(ts))/60))))
packet.append(ZabbixMetric(zbhost, "mongodb_query", int((float(res['opcounters']['query']) - float(query))/((now - float(ts))/60))))
packet.append(ZabbixMetric(zbhost, "mongodb_getmore", int((float(res['opcounters']['getmore']) - float(getmore))/((now - float(ts))/60))))
packet.append(ZabbixMetric(zbhost, "mongodb_command", int((float(res['opcounters']['command']) - float(command))/((now - float(ts))/60))))
# Total ops since last run (per minute approx)
total_ops = res['opcounters']['insert'] + res['opcounters']['update'] + res['opcounters']['delete'] + res['opcounters']['query'] + \
        res['opcounters']['getmore'] + res['opcounters']['command'] - int(insert) - int(update) - int(delete) - int(query) - int(getmore) - int(command)
packet.append(ZabbixMetric(zbhost, "mongodb_total_ops", total_ops))

# Save opcounters
try:
    f = open("/tmp/" + mongohost + "-opcounters", 'w')
    f.write(str(int(now)) + ' ' + str(res['opcounters']['insert']) + ' ' + str(res['opcounters']['update']) + ' ' + str(res['opcounters']['delete']) + ' ' + \
            str(res['opcounters']['query']) + ' ' + str(res['opcounters']['getmore']) + ' ' + str(res['opcounters']['command']))
    f.close()
except Exception as e:
    print("Can't update stats!")
    print(e)

t = ZabbixSender(zabbix_port = ZBPORT, zabbix_server = ZBSERVER).send(packet)
print(t)
