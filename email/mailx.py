#!/usr/bin/python
# -*- coding:utf-8 -*-
import smtplib
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(receiver,title,body):
    """第三发送测试报告"""

    smtpserver = "smtp.qq.com"  # 发件服务器

    port = 25  # 非SSL协议端口号

    sender = "957488199@qq.com"
    psw = "sdkandlansldanldna" #需要授权码不是密码

    send = "告警机器人🤖️"

    receiver = receiver  # 单个接收人也可以是 list

    # with open(report, 'rb+') as f:
    #     mail_body = f.read()
    # body
    msg = MIMEMultipart()
    # msg["from"] = sender  # 发件人
    msg["from"] = send  # 发件人
    msg["to"] = receiver  # 收件人
    # msg["to"] = ";".join(receiver) # 多个收件人 list 转 str
    msg["subject"] = title  # 主题

    # 正文
    body = MIMEText(body, "html", "utf-8")
    msg.attach(body)

    # # 附件
    # att = MIMEText(mail_body, "base64", "utf-8")
    # att["Content-Type"] = "application/octet-stream"
    # att["Content-Disposition"] = 'attachment; filename="test_report.html"'  # 附件的名称
    # msg.attach(att)

    # ----------3.发送邮件------
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)  # 连服务器
        smtp.login(sender, psw)
    except:
        smtp = smtplib.SMTP_SSL(smtpserver, port)  # QQ 邮箱
        smtp.login(sender, psw)  # 登录
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

#
# if __name__ == '__main__':
#     file_name = r'C:\Users\daiba\jiaxu\baihao\111.txt'
#     # send_mail(file_name)
#     send_mail('6513797005','标题','内容')
import sys
if __name__ == "__main__":
    send_mail(sys.argv[1], sys.argv[2], sys.argv[3])
