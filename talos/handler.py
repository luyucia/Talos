#encoding:utf8

from talos.mail import mail
import redis
import ConfigParser
import json

class handler():
    """docstring for handler"""
    def __init__(self, cfg_path):
        self.cfg_path = cfg_path
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.cfg_path)
        self.redis = redis.Redis(host=self.cf.get('redis','host'),port=self.cf.get('redis','port'),db=self.cf.get('redis','db'),password=self.cf.get('redis','password'))


    def sendmail(self,to='',title='',content='',cc='',attachment=''):
        config = {}
        config['smtp_host'] = self.cf.get('email','smtp_host')
        config['username']  = self.cf.get('email','username')
        config['password']  = self.cf.get('email','password')
        m = mail(config)
        m.send(to,title,content,cc,attachment)

    def show(self,content,title,show_type='plain'):
        data = {}
        data['content']   = content
        data['title']     = title
        data['show_type'] = show_type
        self.redis.publish('talos:q:show',json.dumps(data))
