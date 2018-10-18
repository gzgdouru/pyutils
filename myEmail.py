import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import sys

class MyEmail(object):
    def __init__(self, smtpServer, sender, senderPasswd, receiver=[], charset="utf-8"):
        self.smtpServer = smtpServer
        self.sender = sender
        self.senderPasswd = senderPasswd
        self.receiver = receiver
        self.charset = charset

    def set_receiver(self, receiver):
        self.receiver = receiver

    def add_receive(self, receiver):
        self.receiver.append(receiver)

    def send_email(self, subject, content, msgRoot=None, mimeType="plain"):
        try:
            server = smtplib.SMTP_SSL(self.smtpServer, 465)
            server.login(self.sender, self.senderPasswd)

            if msgRoot:
                contentApp = MIMEText(content, mimeType ,_charset=self.charset)
                msgRoot.attach(contentApp)
                msg = msgRoot
            else:
                msg = MIMEText(content, mimeType, self.charset)

            msg["Subject"] = subject
            msg["From"] = self.sender
            msg["To"] = ",".join(self.receiver)
            result = server.sendmail(self.sender, self.receiver, msg.as_string())
            stderr = result if result else None
        except Exception as e:
            stderr = str(e)
        return stderr

    def send_file(self, subject, content, file):
        try:
            filename = os.path.basename(file)
            msgRoot = MIMEMultipart("relate")

            fileApp = MIMEApplication(open(file, "rb").read())
            fileApp.add_header("Content-Type", "application/octet-stream")
            fileApp.add_header("Content-Disposition", "attachment", filename=filename)
            msgRoot.attach(fileApp)

            stderr = self.send_email(subject, content, msgRoot)
        except Exception as e:
            stderr = str(e)
        return stderr

    def send_dir(self, subject, content, path):
        sys.path.insert(0,  os.path.dirname(os.path.abspath(__file__)))
        from compressFile import ZipCompress
        try:
            path = os.path.normcase(os.path.abspath(path))
            filename = "{}.zip".format(path.split(os.sep)[-1])
            ZipCompress.zip_file(path, filename)
            stderr = self.send_file(subject, content, filename)
            os.remove(filename)
        except Exception as e:
            stderr = str(e)
        return stderr

if __name__ == "__main__":
    smtpServer = "smtp.163.com"
    sender = "18719091650@163.com"
    passWd = "qq5201314ouru"
    receiver = ["gzgdouru@163.com"]

    myemail = MyEmail(smtpServer, sender, passWd, receiver)
    # print(myemail.send_email("8折大酬宾", "全场商品一律8折, 快来抢购吧!"))
    # print(myemail.send_file("8折大酬宾", "全场商品一律8折, 快来抢购吧!", "myEmail.py"))
    # print(myemail.send_dir("8折大酬宾", "全场商品一律8折, 快来抢购吧!", "."))



