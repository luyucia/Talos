#encoding:utf8
# import json
import re



def analysis(talos,data):
    # print '[%s][%s] analysis service'%(data['date'],data['host'])
    # print data['content']
    # print data
    # talos.show(data['content'],'207 accesslog','plain')
    if 'name' in data:
        filename = data['name']
    else:
        filename = data['filename']

    f = open('/home/talos/logs/'+filename, 'a')
    f.write(data['content'])
    f.close()


# def handle(talos,s):
    # print 'service %s is down'%s
    # 邮件
    # talos.sendmail(to=['704207999@qq.com','luyucia@163.com'],title='端口检查报警',content='%s 端口服务挂掉了..'%s)
    # talos.show('')
    # 命令
    # http请求
    # 日志
    # 写库
    # web显示



