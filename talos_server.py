#coding:utf-8
#!/usr/bin/python
import logging
import socket
import select 
import sys
import time
import json
import eventlet
import ConfigParser
import redis


talos_redis  = redis.StrictRedis(host='10.0.0.239', port=6379, db=0 , password='6KGz$1mub')

port = 2929

def handle(data,ip):
	d = json.loads(data)
	key = d['key']
	if key=='online':
		talos_redis.hset(key,ip,d['content']['count'])
	elif key=='service':
		talos_redis.set(ip+':'+key,json.dumps(d['content']))
		
if __name__ == "__main__":
	print 'Talos is watching.....'
	ADDR = ('0.0.0.0',2929)  
	BUFSIZE = 10240
	udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udp_socket.bind(ADDR)
	while 1:
		data, addr = udp_socket.recvfrom(BUFSIZE)
		handle(data,addr[0])

	# server = eventlet.listen(('0.0.0.0', port),backlog=4096)
	# pool = eventlet.GreenPool(10000)
	# print "Talos is watching on  %s..."%port
	# while True:
	# 	try:
	# 		new_sock, address = server.accept()
	# 		print address
	# 		pool.spawn_n(handle, new_sock)
	# 	except (SystemExit, KeyboardInterrupt):
	# 		break
