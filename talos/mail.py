#encoding:utf8
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

class mail(object):
    """docstring for mail"""
    def __init__(self, cfg):
        super(mail, self).__init__()
        self.cfg = cfg


    def send(self,to,title,content,cc,attachment):
        msg = MIMEMultipart()
        msg['to']      = ";".join(to)
        msg['cc']      = ";".join(cc)
        msg['from']    = self.cfg['username']
        msg['subject'] = title

        att1 = MIMEText(content,_subtype='html',_charset='utf8')
        msg.attach(att1)

        if attachment!='' :
            try:
                att2 = MIMEText(open(attachment, 'rb').read(), 'base64', 'utf8')
                att2["Content-Type"] = 'application/octet-stream'
                att2["Content-Disposition"] = 'attachment; filename="%s"'%attachment
                msg.attach(att2)
            except Exception, e:
                print e

        try:
            server = smtplib.SMTP()
            server.connect(self.cfg['smtp_host'])
            server.login(self.cfg['username'],self.cfg['password'])
            server.sendmail(msg['from'], to,msg.as_string())
            server.quit()
            print '发送成功'
        except Exception, e:
            print str(e)
