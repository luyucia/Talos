#encoding:utf8



import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado import template
import ConfigParser
import redis
import tornadoredis
import logging
import sys
from talos import daemon

import os
import json

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='logs/talos_webserver.log'
    )

cf = ConfigParser.ConfigParser()
cf.read('config.ini')
r = redis.Redis(host=cf.get('redis','host'),port=cf.get('redis','port'),db=cf.get('redis','db'),password=cf.get('redis','password'))


# c = tornadoredis.Client(cf.get('redis','host'),int(cf.get('redis','port')) )
# c.connect()
# c.select(cf.get('redis','db'))
# c.auth(cf.get('redis','password'))



class MainHandler(tornado.web.RequestHandler):

    def get(self):
        loader = template.Loader("html")
        self.write(loader.load("index.html").generate(myvalue="XXX"))
        self.finish()

class WebSocket(tornado.websocket.WebSocketHandler):

    # def __init__(self, *args, **kwargs):
    #     super(WebSocket, self).__init__(*args, **kwargs)
    #     self.listen()


    def open(self):
        print("WebSocket opened")
        self.listen()

    @tornado.gen.engine
    def listen(self):
        # self.client = tornadoredis.Client(cf.get('redis','host'),int(cf.get('redis','port')))
        # self.client.connect()
        # self.client.select(cf.get('redis','db'))
        # self.client.auth(cf.get('redis','password'))
        # yield tornado.gen.Task(self.client.subscribe, 'talos:q:show')
        # self.client.listen(self.on_message)

        self.ps = r.pubsub()
        self.ps.subscribe(['talos:q:show'])
        # # yield tornado.gen.Task(self.ps.subscribe,'talos:q:show')
        # for item in self.ps.listen():
        #     yield item
        #     tornado.ioloop.IOLoop.instance().add_callback(self.on_message,item)
        #     print item

    @tornado.gen.engine
    def on_message(self, message):
        # for i in self.listen():
        #     print i
        for item in self.ps.listen():
            if item['type']=='message':
                yield item['data']
                self.write_message(item['data'])

    def on_close(self):
        print("WebSocket closed")
        # if self.client.subscribed:
        #     self.client.unsubscribe('talos:q:show')
        #     self.client.disconnect()



class testHandler(tornado.web.RequestHandler):
    def get(self):
        message = 'kk'
        r.publish('talos:q:show', message)
        self.set_header('Content-Type', 'text/plain')
        self.write('sent: %s' % (message,))


file_offset_cache = {}

class Logwebsocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("LogShow WebSocket opened")

    def on_message(self, message):
        # if message:
        # print message
        self.log_file_path = 'logs'
        filename = message
        fullfilename = self.log_file_path+'/'+filename
        f = open(fullfilename,'r')
        f.seek(file_offset_cache[fullfilename])
        lst = list()
        for l in f:
            lst.append(l)
        rtn         = {}
        rtn['code'] = 0
        rtn['data'] = lst
        file_offset_cache[fullfilename] = f.tell()
        f.close()
        self.write_message(json.dumps(rtn))

    def on_close(self):
        print("WebSocket closed")

class LogShow(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        super(LogShow, self).__init__(*args, **kwargs)
        self.log_file_path = 'logs'
        # self.file_offset_cache = {}

    def open(self):
        print("LogShow WebSocket opened")

    def on_message(self, message):
        # if message:
        filename = message
        fullfilename = self.log_file_path+'/'+filename
        f = open(fullfilename,'r')
        f.seek(file_offset_cache[fullfilename])
        lst = list()
        for l in f:
            lst.append(l)
        rtn         = {}
        rtn['code'] = 0
        rtn['data'] = lst
        file_offset_cache[fullfilename] = f.tell()
        self.write_message(json.dumps(rtn))

    def on_close(self):
        print("WebSocket closed")

    def get(self,action=''):
        cmd = 'self.%s()'%action
        print cmd
        if action!='':
            eval(cmd)

    def log_init(self):
        # filename = 'talos_webserver.log'
        filename = self.get_query_argument('f')
        fullfilename = self.log_file_path+'/'+filename
        f = open(fullfilename, 'r+')
        fsize = os.path.getsize(fullfilename)
        lst = list()
        if fsize>1024*64:
            print 'here'
            f.seek(fsize-1024*64)
            while True:
                l = f.readline()
                if l:
                    lst.append(l)
                else:
                    break

            # filelines = f.readlines(1024)
            # print filelines
            # for l in filelines:
            #     lst.append(l)
        else:
            for l in f:
                lst.append(l)
        rtn         = {}
        rtn['code'] = 0
        rtn['data'] = lst
        file_offset_cache[fullfilename] = f.tell()
        f.close()
        self.write(json.dumps(rtn))

    def log_list(self):
        lst = os.listdir(self.log_file_path)
        rtn = {}
        rtn['code'] = 0
        rtn['data'] = lst
        self.write(json.dumps(rtn))


class MyDaemon(daemon.daemon):
    """docstring for MyDaemon"""
    def run(self):
        application = tornado.web.Application([
            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "html/static"}),
            (r"/common/(.*)", tornado.web.StaticFileHandler, {"path": "html/common"}),
            (r"/(.*html)", tornado.web.StaticFileHandler, {"path": "html"}),
            (r"/", MainHandler),
            (r"/ws", WebSocket),
            (r"/test", testHandler),
            (r"/logs/(.*)", LogShow),
            (r"/logws", Logwebsocket),
        ])
        port  = 9008
        logging.info('talos web server started on port:%s'%port)
        application.listen(port)
        tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    # d = MyDaemon('/home/talos/talos_webserver.pid')
    d = MyDaemon('/home/talos/talos_webserver.pid')

    if len(sys.argv) >=2:
        if sys.argv[1]=='start':
            d.start()
        elif sys.argv[1]=='stop':
            logging.info('server stop')
            d.stop()
        elif sys.argv[1]=='restart':
            logging.info('server restart')
            d.restart()
        elif sys.argv[1]=='debug':
            d.run()
        else:
            print "usage: %s start|stop|restart"%sys.argv[0]
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart"%sys.argv[0]
        sys.exit(2)

