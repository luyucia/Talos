#coding:utf-8
import tornado.web
import os
import redis
import ConfigParser
import json

config = ConfigParser.ConfigParser()  
with open('config/config.ini','r') as cfgfile:  
    config.readfp(cfgfile)
    redis_host = config.get('redis-config','host')
    redis_port = int(config.get('redis-config','port')) 
    redis_password = config.get('redis-config','password')
    redis_db = int(config.get('redis-config','db'))
    port     = int(config.get('web-config','port'))

r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db , password=redis_password)
print 'redis connect'

# talos.dashbord.list 原名 别名

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world")
        # self.write(self.get_argument('a'))
        key_list = []
        for x in os.listdir('logs'):
            key_list.append( os.path.splitext(x)[0] )
        logstash_key = key_list[0]
        key_list.sort()
        
        dashbord_list =  r.hgetall('talos.dashbord.list')

        self.render('tpl/index.html',logstash_key=logstash_key,key_list=key_list,dashbord_list=dashbord_list,action=logstash_key)


    def post(self):
        self.write("Hello, world")


class LogShowHandler(tornado.web.RequestHandler):
    def get(self,action):
        # self.write("Hello, world")
        # self.write(self.get_argument('logstash_key'))
        # self.write(logstash_key)
        key_list = []
        for x in os.listdir('logs'):
            key_list.append( os.path.splitext(x)[0] )
        key_list.sort()
        self.render('tpl/logshow.html',logstash_key=action,key_list=key_list,action=action)

class KafkaHandler(tornado.web.RequestHandler):
    def get(self):
        key_list = []
        for x in r.keys('talos_kafka_agent:*'):
            key_list.append( x[18:] )
        key = self.get_argument('key','')
        key_list.sort()
        self.render('tpl/kafka.html',key=key,key_list=key_list)

class DashbordHandler(tornado.web.RequestHandler):
    def get(self,action):
        # key_list = []
        # for x in r.keys('talos_kafka_agent:*'):
        #     key_list.append( x[18:] )
        # key = self.get_argument('key','')
        # key_list.sort()

        # 获取面板列表
        dashbord_list =  r.hgetall('talos.dashbord.list')
        title = dashbord_list[action]
        # 获取面板集合
        dashbord_collection = r.hgetall('talos.dashbord.%s'%(action))
        for x in dashbord_collection:
            dashbord_collection[x] = json.loads(dashbord_collection[x])

        self.render('tpl/dashbord.html',action=title,dashbord_list=dashbord_list,key=action,dashbord_collection=dashbord_collection)
    # 填加一个面板
    def post(self,key):
        json_data = {}
        json_data['name'] = self.get_argument('name')
        json_data['key']  = self.get_argument('key')
        json_data['type'] = self.get_argument('type')
        json_data['desc'] = self.get_argument('desc')
        # 这里key可以加hash
        rtn  =  r.hset('talos.dashbord.%s'%(key),json_data['key'],json.dumps(json_data))
        self.write('{"code":0}')

class DashbordListHandler(tornado.web.RequestHandler):
    def get(self,action):
        pass
    # 填加一个面板
    def post(self):
        dashbord_name= self.get_argument('dashbord_name')

        # 这里key可以加hash
        rtn  =  r.hset('talos.dashbord.list',dashbord_name,dashbord_name)
        self.write('{"code":0}')