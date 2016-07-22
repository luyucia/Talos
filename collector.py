#encoding:utf8
from multiprocessing import Process
from multiprocessing import Queue
import time
import os
import sys
import ConfigParser
import redis
import pyinotify

# 主控制进程
# 负责监听配置文件修改 重启子进程
# 检查子进程存活动
# class ControllerProcess(multiprocessing.Process):
#     """docstring for ControllerProcess"""
#     def __init__(self):
#         super(multiprocessing.Process, self).__init__()

#     def run(self):
#         print 'ok'



# p = ControllerProcess()
# p.start()
import collector.file_collector as fc
import collector.cmd_collector as cc

# def controller():
#     print 'ok'



def getTalosWorkPath():
    path =  os.path.split( os.path.realpath( sys.argv[0] ))
    return path[0]

class ConfigChangeEventHandler(pyinotify.ProcessEvent):

    def process_IN_CLOSE(self,event):
        config_name = os.path.split(event.pathname)[1]

        if config_name=='file_collector.json':
            mq_to_file_collector.put('update')
        elif config_name=='cron_collector.json':
            mq_to_cron_collector.put('update')


cf = ConfigParser.ConfigParser()
cf.read('configs/config.ini')
r = redis.Redis(host=cf.get('redis','host'),port=cf.get('redis','port'),db=cf.get('redis','db'),password=cf.get('redis','password'))



# 初始化子进程通信消息队列
mq_to_file_collector = Queue()
mq_to_cron_collector = Queue()

# 文件收集进程
p = Process(target=fc.init,args=(mq_to_file_collector,getTalosWorkPath()+'/configs/file_collector.json',r) )
p.start()

# 定时任务收集进程
p1 = Process(target=cc.init,args=(mq_to_cron_collector,getTalosWorkPath()+'/configs/cron_collector.json',r) )
p1.start()


# 监听配置文件变更
wm = pyinotify.WatchManager()
wm.add_watch('configs/',pyinotify.IN_CLOSE_WRITE, rec=True)
notifier = pyinotify.Notifier(wm, ConfigChangeEventHandler())
notifier.loop()
