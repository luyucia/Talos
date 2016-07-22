#encoding:utf8
import ConfigParser
import json
import redis
import subprocess
import os
import datetime
import socket
import pyinotify

cf = ConfigParser.ConfigParser()
cf.read('../../config.ini')
r = redis.Redis(host=cf.get('redis','host'),port=cf.get('redis','port'),db=cf.get('redis','db'),password=cf.get('redis','password'))

file_fd_cache = {}
config_map    = {}
host          = socket.gethostname()

class MyEventHandler(pyinotify.ProcessEvent):

    def process_IN_MODIFY(self, event):
        # print 'modify'
        # print file_fd_cache[event.pathname].readline()
        # if config_map[event.pathname]['watch_type']=='config':
        #     pass
        # else:
        data = {}
        # fullpath = event.pathname.replace('.filepart','')
        fullpath = event.pathname

        config_key = fullpath

        (filepath,filename) = os.path.split(fullpath)
        data['filepath']    = filepath
        data['filename']    = filename
        data['host']        = host
        data['date']        = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 如果是文件夹，文件指针缓存可能不存在
        # if fullpath not in file_fd_cache:
        #     print 'not in cache'
        #     fd = open(fullpath,'r')
        #     # 定位到文件末尾
        #     fd.seek(0,2)
        #     # abs_path                =  os.path.abspath(fullpath)
        #     file_fd_cache[fullpath] = fd
        #     # 如果是文件夹
        #     config_map[fullpath] = config_map[filepath]

        data['content']     = file_fd_cache[fullpath].readline()
        data['analyzer']    = config_map[fullpath]['analyzer']

        if 'name' in config_map[fullpath]:
            data['name']        = config_map[fullpath]['name']

        r.publish('talos:q:file',json.dumps(data))


def init():
    json_config = open('config.json', 'r')
    jsons = json.loads(json_config.read())
    wm = pyinotify.WatchManager()
    eh = MyEventHandler()
    for c in jsons:
        if c['enable']!=True:
            continue

        # 如果是文件 则定位到文件末尾
        if os.path.exists(c['path']) and os.path.isdir(c['path']):
            c['isDir'] = True
            config_map[c['path']]    = c
        else:
            # 如果是文件则传入配置
            fd = open(c['path'],'r')
            # 定位到文件末尾
            fd.seek(0,2)
            abs_path                =  os.path.abspath(c['path'])
            # 文件指针缓存
            file_fd_cache[abs_path] = fd
            # 配置
            config_map[abs_path]    = c

            wm.add_watch(c['path'],pyinotify.IN_MODIFY, rec=True)


    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()




init()




