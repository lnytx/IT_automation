'''
Created on 2017年3月26日

@author: admin
文本邮件
'''
import smtplib
import string
from email import header
s='a'
s.join()
HOST = "smtp.gmail.com"
SUBJECT = "Test email from Python"
TO = "test@qq.com"
FROM = "test@gmail.com"
text = "Python rules them all!"
BODY = header('python邮件测试','utf_8')


server = smtplib.SMTP()
server.connect(HOST,"25")
server.starttls()
server.login("test@gmail.com","123456")
server.sendmail(FROM, [TO], BODY.as_string())
server.quit()
