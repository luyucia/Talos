#encoding:utf8
import datetime

def analysis(talos,data):
    # print data
    content_str = ''
    for l in data['content']:
        content_str+=l

    to = ['limingze@calli-tech.com','luyucia@163.com']
    title = 'data report %s'%datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if 'param' in data:
        if 'to' in data['param']:
            to    = data['param']['to']
        if 'title' in data['param']:
            title = data['param']['title']

    if content_str!='':
        talos.sendmail(to,title,content=content_str)


