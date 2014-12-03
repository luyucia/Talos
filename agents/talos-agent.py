#coding:utf-8
# 此脚本用于从登录表和登出表计算出在线时长存在中间表mid_login中
# 用来计算游戏习惯
import sys
import time
import json
import datetime

import redis
import pickle
import socket
import datetime
import platform
import os
# import talos
# import talos.system as sysinfo

# talos_redis  = redis.StrictRedis(host='10.0.0.239', port=6379, db=0 , password='6KGz$1mub')

# cmd = talos.Command()



# sysinfo = talos.Sysinfo()

# info = sysinfo.basic()
# key1 = "%s:%s"%(info['ip'],'service')
# key2 = "%s:%s"%(info['ip'],'sysinfo')

# talos_redis.set(key2,json.dumps(info))



# coding:utf-8

class TalosClient(object):
	"""docstring for TalosClient"""
	def __init__(self, ip,port=2929):
		super(TalosClient, self).__init__()
		self.ip   = ip
		self.port = port
		self.addr = (self.ip,self.port)
		self.cocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

	def send(self,key,content):
		data = {}
		data['key'] = key
		data['content'] = content
		self.cocket.sendto(json.dumps(data),self.addr)

	def close(self):
		self.cocket.close()


class SystemInfo(object):
	"""docstring for SystemInfo"""
	def __init__(self):
		super(SystemInfo, self).__init__()

	def basic(self):
		uname = platform.uname()
		system_info = {}
		system_info['data_type']    = 'system_info'
		system_info['os']           = uname[0]
		system_info['hostname']     = uname[1]
		system_info['kernel']       = uname[2]
		system_info['architecture'] = uname[4]
		system_info['distribution'] = '%s %s %s'%platform.linux_distribution()
		system_info['ip']           = socket.gethostbyname(uname[1])
		system_info['date']         = str(datetime.datetime.now())
		return system_info

	def service(self):
		d = os.popen("netstat -tnlp |awk '{print $4,$7}'").read()
		# d = c.run("netstat -tnlp -A inet|awk '{print $4,$7}'")

		lines = d.split("\n")
		service_dic = []
		for line in lines[2:-1]:
			dic = {}
			p = line.split(' ')
			if p[0][0]==':' :
				ip = []
				ip.append('all')
				ip.append(p[0][3:])
			else:
				ip      = p[0].split(':')
			process = p[1].split('/')
			dic['ip']    = ip[0]
			dic['port']  = ip[1]
			dic['pid']   = process[0]
			dic['pname'] = process[1]
			service_dic.append(dic)

		return service_dic

info = SystemInfo()


client = TalosClient('10.0.0.240')

while 1:
	time.sleep(3)
	try:
		client.send('service',info.service())
	except Exception, e:
		print e
	

# while 1:
# 	# a = time.time()
# 	talos_redis.set(key1,json.dumps(sysinfo.service()),3)
# 	# print time.time()-a
# 	time.sleep(3)

