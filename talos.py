#encoding:utf8

import redis
import json
import re
import imp
import ConfigParser
import logging

# 根据配置读取队列内容
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from talos import daemon

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='logs/talos_main.log'
    )

def main():
    path        = sys.path[0]
    config_file = path+'/config.ini'
    logging.info(config_file)
    cf = ConfigParser.ConfigParser()
    cf.read(config_file)

    r = redis.Redis(host=cf.get('redis','host'),port=cf.get('redis','port'),db=cf.get('redis','db'),password=cf.get('redis','password'))
    ps = r.pubsub()
    logging.info('talos run connect redis.')
    ps.subscribe(['talos:q:cmd','talos:q:file'])


    sys.path.append(path)
    import talos.handler
    talosHandler = talos.handler.handler(config_file)
    logging.info('talos listening')
    for item in ps.listen():
        if item['type']=='message':
            data = json.loads(item['data'])
            try:
                a = imp.load_source(data['analyzer'],path+'/analyzer/'+data['analyzer']+'.py')
                a.analysis(talosHandler,data)
            except Exception, e:
                # raise e
                logging.error(e)



class MyDaemon(daemon.daemon):
    """docstring for MyDaemon"""
    def run(self):
        main()




if __name__ == "__main__":
    # d = MyDaemon('/home/talos/talos_webserver.pid')
    d = MyDaemon('talos_main.pid',stdout='logs/talos_main.log',stderr='logs/talos_main.log')

    if len(sys.argv) >=2:
        if sys.argv[1]=='start':
            d.start()
        elif sys.argv[1]=='stop':
            logging.info('server stop')
            d.stop()
        elif sys.argv[1]=='restart':
            logging.info('server restart')
            d.restart()
        else:
            print "usage: %s start|stop|restart"%sys.argv[0]
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart"%sys.argv[0]
        sys.exit(2)
