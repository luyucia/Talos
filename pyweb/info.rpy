from twisted.web.resource import Resource
import redis
r       = redis.StrictRedis(host='10.0.0.239', port=6379, db=0 , password='6KGz$1mub')

class getInfo(Resource):
    isLeaf = True
    def __init__(self, ip):
        Resource.__init__(self)
        self.ip = ip

    def render_GET(self, request):
        # return self.ip
        key = self.ip+':sysinfo'
        rs = r.get(key)
        if rs:
            return rs
        else:
            return '{"code":0}'

class getService(Resource):
    isLeaf = True
    def __init__(self, ip):
        Resource.__init__(self)
        self.ip = ip

    def render_GET(self, request):
        # return self.ip
        request.setHeader("content-type", "text/plain")
        request.setHeader("Access-Control-Allow-Origin", "*")
        key = self.ip+':service'
        rs = r.get(key)
        if rs:
            return rs
        else:
            return '{"code":0}'


class sysinfo(Resource):

    def render_GET(self, request):
        return ''
    def getChild(self,name,request):
        return getInfo(name)

class service(Resource):

    def render_GET(self, request):
        return ''
    def getChild(self,name,request):
        return getService(name) 




class RouterResource(Resource):
    
    def render_GET(self, request):
        # k = r.keys()
        # a = ''
        # for x in k:
        #     a+=x+'<br>'
        # help(request)
        # return "<html>Hello, world!%s</html>"%(a)
        # return r.get("kafka_master:kafka:AllTopicsMessagesInPerSec")
        # url = request.URLPath()
        # return url[0]
        # return request.args['ip'][0]
        return ''

    def getChild(self,name,request):
        if name=='sysinfo':
            return sysinfo()
        elif name=='service':
            return service()

resource = RouterResource()