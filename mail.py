from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os,email.utils

def send_mail(to,subject,body):
    ID ='y.sekimura.sys22@morijyobi.ac.jp'
    PASS= os.environ['MAIL_PASS']
    HOST = 'smtp.gmail.com'
    PORT = 587
    msg = MIMEMultipart()
    # MIME　インスタンス作成
    msg.attach(MIMEText(body,'html'))
    #HTML　形式の本文を設定
    msg['Subject']=subject
    msg['From']=email.utils.formataddr(('システムメール',ID))
    msg['To']=email.utils.formataddr(('ユーザ様',to))
    
    #SMTP　サーバーへ接続
    server = SMTP(HOST, PORT)
    server.starttls()
    server.login(ID,PASS)#ログイン認証
    
    server.send_message(msg)#送信
    
    server.quit() #サーバー切断