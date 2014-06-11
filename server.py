# from twisted.application import internet, service
# from twisted.web import static, server

# resource = static.File("pyweb")
# application = service.Application('pyweb')
# site = server.Site(resource)
# sc = service.IServiceCollection(application)
# tcpserver = internet.TCPServer(80, site)
# tcpserver.setServiceParent(sc)

# from twisted.web import server, resource
# from twisted.internet import reactor

# import redis
# r       = redis.StrictRedis(host='10.0.0.239', port=6379, db=0 , password='6KGz$1mub')

# class rootResource(resource.Resource):
#     # isLeaf = True

#     def getChild(self, name, request):
#         if name == '':
#             return self
#         return Resource.getChild(self, name, request)
    
#     def render_GET(self, request):
#         self.numberRequests += 1
#         request.setHeader("content-type", "text/plain;charset=utf-8")
#         # k = ''
#         # for a in r.keys():
#         #     k+=a+'<br>'
#         # return "Hello, world! I am located at %r." % (request.prepath,)
#         # return "I am request #" + str(self.numberRequests) + "\n"+k

# class Test(resource.Resource):
#     isLeaf = True
#     def render_GET(self, request):
#         request.setHeader("content-type", "text/plain;charset=utf-8")
#         print request
#         return 'test'


# root = rootResource()
# root.putChild('test',Test())

# reactor.listenTCP(80, server.Site(root))
# reactor.run()


from twisted.application import internet, service
from twisted.web import static, server, script
from twisted.internet import reactor



root = static.File("pyweb")
root.ignoreExt(".rpy")
root.processors = {'.rpy': script.ResourceScript}
application = service.Application('web')
sc = service.IServiceCollection(application)
site = server.Site(root)

# i = internet.TCPServer(80, site)
# i.setServiceParent(sc)


reactor.listenTCP(80, site)
reactor.run()