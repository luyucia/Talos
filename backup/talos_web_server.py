#coding:utf-8
import tornado.websocket
import tornado.ioloop
import tornado.web
import os
# import redis
import ConfigParser
import sys;
# sys.path.append('lib')
# sys.path.append('lib/controller')
sys.path.append('web')
import index_controller
import websocket_controller

config = ConfigParser.ConfigParser()  
with open('config/config.ini','r') as cfgfile:  
    config.readfp(cfgfile)
    port     = int(config.get('web-config','port'))


application = tornado.web.Application([
    (r"/web/(.*)", tornado.web.StaticFileHandler, {"path": "web/"}),
    (r"/", index_controller.MainHandler),
    (r"/logshow/(.*)", index_controller.LogShowHandler),
    (r"/kafka", index_controller.KafkaHandler),
    (r"/dashbord/(.*)", index_controller.DashbordHandler),
    (r"/dashbordList", index_controller.DashbordListHandler),
    (r"/ws", websocket_controller.LogEchoWebSocket),
    (r"/jmx", websocket_controller.KafkaJmxWebsocket),
    (r"/redis", websocket_controller.RedisWebsocket),
])

if __name__ == "__main__":
    print 'server start'
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()