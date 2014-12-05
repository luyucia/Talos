#coding:utf-8
# 原文处理器，仅仅把收到的日志记录到logs目录下，名字和logstash中的key一致
def handle(logmsg,fp):
    # logmsg['host']
    # print logmsg['message']
    fp.write(logmsg['host']+' '+logmsg['message']+'\n')
    fp.flush()
    # logmsg['path']
    # print logmsg['@timestamp']