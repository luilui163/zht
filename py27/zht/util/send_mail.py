# coding=utf-8
'''
Created on 2015年8月26日

@author: 熙腾
'''

import smtplib
from email.mime.text import MIMEText

mailto_list = ['986340770@qq.com', '13163385579@163.com']
# ===============================================================================
# mail_host="smtp.163.com"  #设置服务器

# mail_postfix="163.com"  #发件箱的后缀
# ===============================================================================

mail_host = "smtp.qq.com"

mail_pass =
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
    except Exception, e:
        # if isinstance(e,tuple):
        # for eee in ee:
        print str(e[0])
        print str(e[1]).encode('unicode_escape').decode('string_escape')
        # else:
        #    print str(e).encode('utf-8')
        return False


if __name__ == '__main__':
    if send_mail("hello", "hello world!"):
        print "发送成功"
    else:
        print "发送失败"


# https://www.joinquant.com/post/1435