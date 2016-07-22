#coding:utf-8
import redis
import ConfigParser
import json
import sys
# sys.path.append("lib")
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append("handlers")
import kafka_handler
import plain_handler

# key为logstash中key value为处理类型
handler_map = {}

config = ConfigParser.ConfigParser()
with open('config/config.ini','r') as cfgfile:  
    config.readfp(cfgfile)
    redis_host = config.get('redis-config','host')
    redis_port = int(config.get('redis-config','port')) 
    redis_password = config.get('redis-config','password')
    redis_db = int(config.get('redis-config','db'))

    for o in config.options('channels'):
        handler_map[o] = config.get('channels',o)

r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db , password=redis_password)

subscribe_list = []
log_fp_dic     = {}
for k in handler_map:
    subscribe_list.append(k)
    log_fp_dic[k] = open('logs/%s.log'%(k), 'a')
ps = r.pubsub()  
ps.subscribe(subscribe_list)

# 监听所有channel
for item in ps.listen():
    log_type = handler_map[ item['channel'] ]
    if item['type'] == 'message': 
        # 消息解析，调用相应的handler
        logmsg =  json.loads(item['data'])
        # if log_type=='kafka-server-log':
        #     kafka_handler.handle(logmsg)
        plain_handler.handle(logmsg,log_fp_dic[ item['channel'] ] )
        