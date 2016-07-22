#encoding:utf8
import ConfigParser
import json
import redis
import subprocess
import os
import datetime
import socket
from apscheduler.schedulers.blocking import BlockingScheduler

cf = ConfigParser.ConfigParser()
cf.read('../../config.ini')

r = redis.Redis(host=cf.get('redis','host'),port=cf.get('redis','port'),db=cf.get('redis','db'),password=cf.get('redis','password'))

# scheduler = BlockingScheduler()

# def myjob(cmd,enable,analyzer):
#     # 获取日期
#     # 获取HOST信息
#     # analyzer
#     if enable:
#         tmp = os.popen(cmd).readlines()
#         data = {}
#         data['content']  = tmp
#         data['analyzer'] = analyzer
#         data['host']     = socket.gethostname()
#         data['date']     = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         r.publish('talos:q:cmd',json.dumps(data))

# json_config = open('cmd.json', 'r')
# # print json_config.read()
# jsons = json.loads(json_config.read())

# for c in jsons:
#     cron = c['time'].split(' ')
#     job = scheduler.add_job(myjob,args=[c['cmd'],c['enable'],c['analyzer']],trigger='cron', year=cron[5], month=cron[4], day=cron[3], hour=cron[2], minute=cron[1], second=cron[0])

# ps = r.pubsub()
# r.publish('talos:q',)

# pip install apscheduler

# xpression   Field   Description
# *   any Fire on every value
# */a any Fire every a values, starting from the minimum
# a-b any Fire on any value within the a-b range (a must be smaller than b)
# a-b/c   any Fire every c values within the a-b range
# xth y   day Fire on the x -th occurrence of weekday y within the month
# last x  day Fire on the last occurrence of weekday x within the month
# last    day Fire on the last day within the month
# x,y,z   any Fire on any matching expression; can combine any number of any of the above expressions
# scheduler.start()


class TalosCollectorCron(object):
    """docstring for talosCollectorCron"""
    def __init__(self, redis_conn,config_path):
        super(TalosCollectorCron, self).__init__()
        self.redis_conn  = redis_conn
        self.config_path = config_path
        self.scheduler = BlockingScheduler()
        json_config    = open(config_path, 'r')
        # print json_config.read()
        self.jsons = json.loads(json_config.read())

    def myjob(self,c):
        # 获取日期
        # 获取HOST信息
        # analyzer
        if c['enable']:
            tmp = os.popen(c['cmd']).readlines()
            data = {}
            data['content']  = tmp
            data['analyzer'] = c['analyzer']
            data['host']     = socket.gethostname()
            data['date']     = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data['param']    = c['param']
            r.publish('talos:q:cmd',json.dumps(data))

    def start(self):
        for c in self.jsons:
            cron = c['time'].split(' ')
            job = self.scheduler.add_job(self.myjob,args=[c],trigger='cron', year=cron[5], month=cron[4], day=cron[3], hour=cron[2], minute=cron[1], second=cron[0])
        print 'TalosCollectorCron Start..'
        self.scheduler.start()


t = TalosCollectorCron(r,'cmd.json')
t.start()
