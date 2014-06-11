from twisted.web.resource import Resource
import redis
r       = redis.StrictRedis(host='10.0.0.239', port=6379, db=0 , password='6KGz$1mub')


class get(Resource):
    isLeaf = True
    def __init__(self, key):
        Resource.__init__(self)
        self.key = key

    def render_GET(self, request):
        # return self.ip
        request.setHeader("content-type", "text/plain")
        request.setHeader("Access-Control-Allow-Origin", "*")
        key = self.key
        rs = r.get(key)
        if rs:
            return rs
        else:
            return '{"code":0}'

class RouterResource(Resource):
    
    def render_GET(self, request):
        return ''

    def getChild(self,name,request):
        return get(name)

resource = RouterResource()