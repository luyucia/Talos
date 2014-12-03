
fp = open('logs/kafka-server.log', 'a')

def handle(logmsg):
    # logmsg['host']
    print logmsg['message']
    fp.write(logmsg['message']+'\n')
    fp.flush()
    # logmsg['path']
    # print logmsg['@timestamp']