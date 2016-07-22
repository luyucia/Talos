#encoding:utf8
# import json
import re

check_ports = {
    '9000':'php-fpm',
    '8056':'tornado',
    '3001':'dline-http',
    '80':'nginx',
    '8899':'dline-socket',
    '8888':'php-websocket-server',
    # '9092':'kafka-broker',
    '6379':'redis',
    '4730':'gearman',
    # '3321':'test',
}



def analysis(talos,data):
    alive_ports = {}
    print '[%s][%s] analysis service'%(data['date'],data['host'])

    rule = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:(\d*)')
    for line in data['content']:
        m = rule.search(line)
        if m:
            alive_ports[m.groups()[0]] = True
        # print l
    # print alive_ports
    for ports in check_ports:
        if ports not in alive_ports:
            handle(talos,check_ports[ports])
    # if test_php_faile:
    #     trigger('handle_phpdown')


def handle(talos,s):
    print 'service %s is down'%s
    # 邮件
    talos.sendmail(to=['704207999@qq.com','luyucia@163.com'],title='端口检查报警',content='%s 端口服务挂掉了..'%s)

    # 命令
    # http请求
    # 日志
    # 写库
    # web显示



