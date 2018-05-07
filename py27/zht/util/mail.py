# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 16:06:22 2016

@author: Administrator
"""

from email.mime.text import MIMEText
msg=MIMEText('hello,send by Python...','plain','utf-8')


smtp_server='hwsmtp.exmail.qq.com'
to_addr='13163385579@163.com'

import smtplib
server=smtplib.SMTP(smtp_server,465)
#server=smtplib.SMTP()
#server.connect(smtp_server)
server.set_debuglevel(1)
server.login(from_addr,password)
server.sendmail(from_addr,to_addr,msg.as_string())
server.quit()

