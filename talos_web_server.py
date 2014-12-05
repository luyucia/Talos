#coding:utf-8
import tornado.websocket
import tornado.ioloop
import tornado.web
import os
import redis
import ConfigParser

config = ConfigParser.ConfigParser()  
with open('config/config.ini','r') as cfgfile:  
    config.readfp(cfgfile)
    redis_host = config.get('redis-config','host')
    redis_port = int(config.get('redis-config','port')) 
    redis_password = config.get('redis-config','password')
    redis_db = int(config.get('redis-config','db'))
    port     = int(config.get('web-config','port'))

r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db , password=redis_password)



class LogEchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print "WebSocket opened"
        logstash_key = self.get_argument('logstash_key')
        self.fp = open('logs/%s.log'%(logstash_key),'rw+')
        # 如果文件大于1mb，则从文件末尾1mb处开始读取
        self.fp.seek(0,os.SEEK_END)
        pos_last =  self.fp.tell()
        if pos_last>1048576:
            self.fp.seek(-1048576,os.SEEK_END)
        else:
            self.fp.seek(0)

    def on_message(self, message):
        if message=='get_data':
            while True:
                line = self.fp.readline()
                if not line:
                    return
                self.write_message(line)
        elif message=='clean_log':
            self.fp.seek(0)
            self.fp.truncate()
            print 'clean log finish'
        
    def on_close(self):
        print "WebSocket closed"

class KafkaJmxWebsocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print "WebSocket opened"
        self.key = self.get_argument('key')

    def on_message(self, message):
        if message=='get_data':
            json_data  =  r.get(self.key)
            if json_data!=None:
                self.write_message(r.get(self.key))
        elif message=='clean_log':
            print 'clean log finish'
        
    def on_close(self):
        print "WebSocket closed"


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world")
        # self.write(self.get_argument('a'))
        key_list = []
        for x in os.listdir('logs'):
            key_list.append( os.path.splitext(x)[0] )
        logstash_key = key_list[0]
        key_list.sort()
        self.render('web/tpl/index.html',logstash_key=logstash_key,key_list=key_list)

    def post(self):
        self.write("Hello, world")

class LogShowHandler(tornado.web.RequestHandler):
    def get(self,logstash_key):
        # self.write("Hello, world")
        # self.write(self.get_argument('logstash_key'))
        # self.write(logstash_key)
        
        key_list = []
        for x in os.listdir('logs'):
            key_list.append( os.path.splitext(x)[0] )
        key_list.sort()
        self.render('web/tpl/index.html',logstash_key=logstash_key,key_list=key_list)

class KafkaHandler(tornado.web.RequestHandler):
    def get(self):
        key_list = []
        for x in r.keys('talos_kafka_agent:*'):
            key_list.append( x[18:] )
        key = self.get_argument('key','')
        key_list.sort()
        self.render('web/tpl/kafka.html',key=key,key_list=key_list)


application = tornado.web.Application([
    (r"/web/(.*)", tornado.web.StaticFileHandler, {"path": "web/"}),
    (r"/", MainHandler),
    (r"/logshow/(.*)", LogShowHandler),
    (r"/kafka", KafkaHandler),
    (r"/ws", LogEchoWebSocket),
    (r"/jmx", KafkaJmxWebsocket),
])

if __name__ == "__main__":
    print 'server start'
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()