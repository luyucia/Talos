#encoding:utf8
# import ConfigParser
import json
import logging
import socket
import os
import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
host          = socket.gethostname()


# logger = logging.getLogger()
# fh = logging.FileHandler('cmd.log')
# fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
# logger.setHandler(fh)
r = False

scheduler = BackgroundScheduler()
def myjob(c):
    # 获取日期
    # 获取HOST信息
    # analyzer
    if c['enable']:
        tmp = os.popen(c['cmd']).readlines()
        data = {}
        data['content']  = tmp
        data['analyzer'] = c['analyzer']
        data['host']     = host
        data['date']     = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['param']    = c['param']
        r.publish('talos:q:cmd',json.dumps(data))

def cronstart(configPath):
    try:
        json_config    = open(configPath, 'r')
        jsons          = json.loads(json_config.read())
    except Exception, e:
        print 'cmd collector config Error!!!'
        print e
        return

    scheduler.remove_all_jobs()

    for c in jsons:
        cron = c['time'].split(' ')
        job = scheduler.add_job(myjob,args=[c],trigger='cron', year=cron[5], month=cron[4], day=cron[3], hour=cron[2], minute=cron[1], second=cron[0])
    print 'add job finished.'

def init(msgQueue,talosPath,redis):
    global r
    r = redis
    cronstart(talosPath)
    scheduler.start()
    while True:
        time.sleep(1)
        msg = msgQueue.get()
        if msg=='update':
            print 'cron collector config reloaded'
            cronstart(talosPath)
