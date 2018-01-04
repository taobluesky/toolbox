#-*- coding:utf-8 -*-

import os
import base64
import smtplib
import xlrd

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
from email.utils import formataddr

smtp_host = 'smtp.qq.com'
port = 465
sender= ''    # 发件人邮箱账号
sender_name = ''
password = '' # 发件人邮箱密码

subject = u"【pre-A】车加家-可共享和预约车位的停车平台【智能硬件/静态交通】"
data = xlrd.open_workbook('to.xlsx')
mail_body = open('body.txt', 'rb').read().decode('utf-8')
pdf_file = open(u'车加家智慧停车场商业计划书_v5.0.pdf', 'rb').read()
img_file = open('img.png', 'rb').read()
attachment_name = u'车加家智慧停车场商业计划书.pdf' # 附件显示的文件名


def send_mail(sender, sender_name, to, to_name):
    ret = True
    
    try:
        msg = MIMEMultipart('related')
        msg['From']=formataddr([sender_name, sender])
        msg['To'] = formataddr(['', to])
        msg['Subject']= Header(subject, 'utf-8')
        
        # 正文图片
        img = MIMEImage(img_file)
        img.add_header('Content-ID', '<image1>')
        msg.attach(img)
        
        # 正文
        if to_name:
            body = mail_body.replace('{% name %}', to_name + u'，')
        else:
            body = mail_body.replace('{% name %}', '')
        msg.attach(MIMEText(body, 'html', 'utf-8'))
        
        # 附件
        att1 = MIMEText(pdf_file, 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        
        #att1["Content-Disposition"] = 'attachment; filename="车加家智慧停车场商业计划书.pdf"'
        # 解决中文名乱码
        att1.add_header('Content-Disposition', 'attachment', \
            filename= '=?utf-8?b?' + base64.b64encode(attachment_name.encode('UTF-8')) + '?=')
        
        msg.attach(att1)
        
        server = smtplib.SMTP_SSL(smtp_host, port)
        server.login(sender, password)
        server.sendmail(sender, [to,], msg.as_string())
        server.quit()
        
    except Exception,e:
        print e
        ret = False
        
    return ret

def main():
    table = data.sheets()[0]
    for i in range(table.nrows):
        to_mail = table.row_values(i)[0]
        to_name = table.row_values(i)[1] if len(table.row_values(i)) > 1 else u''
        
        if to_mail:
            ret = send_mail(sender, sender_name, to_mail, to_name)
            
            if ret:
                if to_name:
                    print(u"<%s>%s邮件发送成功" % (to_name, to_mail))
                else:
                    print(u"%s邮件发送成功" % (to_mail,))
            else:
                if to_name:
                    print(u"<%s>%s邮件发送失败" % (to_name, to_mail))
                else:
                    print(u"%s邮件发送失败" % (to_mail,))
                    
    os.system("pause")
    
    
if __name__ == "__main__":
    main()
    