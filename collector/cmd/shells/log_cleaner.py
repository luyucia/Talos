#encoding:utf8

import os
import datetime
import time
import re

dirlist = ['/var/log/wifi_server','/usr/local/kafka/kafka_2.11-0.9.0.1/logs']

rule = re.compile(r".*\.log")

for d in dirlist:
    for f in os.listdir(d):
        # print os.path.abspath(f)
        # print os.path.getmtime(f)
        fullpath =  os.path.join(d,f)
        if (time.time() - os.path.getmtime(fullpath)) > 3600*24*7:
            if rule.search(fullpath):
                # os.remove(fullpath)
                print "%s is deleted"%fullpath
