#!/usr/bin/python
#  -*- coding: utf-8 -*-

from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import os
import smtplib
import re,urllib2

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

from_addr = 'xx.com'
password = 'xx'
to_addr = 'yy'
smtp_server = 'smtp.163.com'
path="file:///Users/jinceshi/PycharmProjects/untitled1/"
result_dir="//Users/jinceshi/PycharmProjects/untitled1/"
path1="file:///Users/jinceshi/PycharmProjects/untitled2/"
result_dir1="//Users/jinceshi/PycharmProjects/untitled2/"

msg = MIMEMultipart()
msg['From'] = _format_addr('xx <%s>' % from_addr)
msg['To'] = _format_addr('xx <%s>' % to_addr)
msg['Subject'] = Header('自动化测试错误报告', 'utf-8').encode()

l=os.listdir(result_dir)
#为了获取目录下时间最新的文件
l.sort(key=lambda fn: os.path.getmtime(result_dir+"/"+fn) if not os.path.isdir(result_dir+"/"+fn) else 0)
htmlpath=path+l[-1]#html网页文件
htmlpath2=result_dir+l[-1]#该文件路径

l1=os.listdir(result_dir1)
#为了获取目录下时间最新的文件
l1.sort(key=lambda fn: os.path.getmtime(result_dir1+"/"+fn) if not os.path.isdir(result_dir1+"/"+fn) else 0)
htmlpath3=path1+l1[-1]#html网页文件
htmlpath4=result_dir1+l1[-1]#该文件路径

print(htmlpath,htmlpath2,htmlpath3,htmlpath4)
#用Request包装地址
request=urllib2.Request(htmlpath)
#用进行访问地址，并且返回网页源码
response=urllib2.urlopen(request)
#把网页源码转成utf-8访问
content=response.read().decode('utf-8')
#下面包装正则表达式，re.S 标志代表在匹配时为点任意匹配模式，''里面的内容为匹配表达式，(.*?)为我们要找的内容，
pattern=re.compile('<a class="popup_link" onfocus=.*? href=".*?" >(.*?)</a>',re.S)
#findall开始查找，把找到的数据放在列表里返回
mslist=re.findall(pattern,content)

#用Request包装地址
request1=urllib2.Request(htmlpath3)
#用进行访问地址，并且返回网页源码
response1=urllib2.urlopen(request1)
#把网页源码转成utf-8访问
content1=response1.read().decode('utf-8')
#下面包装正则表达式，re.S 标志代表在匹配时为点任意匹配模式，''里面的内容为匹配表达式，(.*?)为我们要找的内容，
pattern1=re.compile('<a class="popup_link" onfocus=.*? href=".*?" >(.*?)</a>',re.S)
#findall开始查找，把找到的数据放在列表里返回
mslist1=re.findall(pattern1,content1)
if len(mslist)>0 or len(mslist1)>0 :
    msg.attach(MIMEText('log for error', 'plain', 'utf-8'))
    if len(mslist)>0 and len(mslist1)>0:
        att = MIMEText(open(htmlpath2,'rb').read(),'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="B2CLatestResult.html"'
        msg.attach(att)

        att1 = MIMEText(open(htmlpath4,'rb').read(),'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="B2BLatestResult.html"'
        msg.attach(att1)

        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
    elif len(mslist) >0:
        att = MIMEText(open(htmlpath2,'rb').read(),'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="B2CLatestResult.html"'
        msg.attach(att)

        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
    else:
        att1 = MIMEText(open(htmlpath4,'rb').read(),'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="B2BLatestResult.html"'
        msg.attach(att1)

        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
else:
    print('there have no error')
    msg.attach(MIMEText('there is no error after bulid', 'plain', 'utf-8'))

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

