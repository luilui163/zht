# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-02-10  15:52
# NAME:assetPricing-mailu.py


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


import smtplib
from email.mime.text import MIMEText

mailto_list = ['986340770@qq.com', '13163385579@163.com']
# ===============================================================================
# mail_host="smtp.163.com"  #设置服务器

# mail_postfix="163.com"  #发件箱的后缀
# ===============================================================================

mail_host = "smtp.qq.com"


mail_postfix = "qq.com"


def send_mail(sub, content):
    me = "zht_python_monitor" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype='plain', _charset='gb2312')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(mailto_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.starttls()
        server.login(mail_user, mail_pass)
        server.sendmail(me, mailto_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        # if isinstance(e,tuple):
        # for eee in ee:
        print(str(e[0]))
        print(str(e[1]).encode('unicode_escape').decode('string_escape'))
        # else:
        #    print str(e).encode('utf-8')
        return False


if __name__ == '__main__':
    if send_mail("hello", "hello world!"):
        print("发送成功")
    else:
        print("发送失败")
