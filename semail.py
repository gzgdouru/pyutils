import smtplib
import os
import shutil
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class SendEmail(object):
    def __init__(self, smtp_server, sender, password, charset="utf-8"):
        self.smtp_server = smtp_server
        self.sender = sender
        self.password = password
        self.charset = charset

    def send_email(self, subject, content, receiver, msgRoot=None, mimeType="plain"):
        if not isinstance(receiver, list) and not isinstance(receiver, set):
            return "receiver的类型必须为列表或集合!"

        server = smtplib.SMTP_SSL(self.smtp_server, 465)
        server.login(self.sender, self.password)

        if msgRoot:
            content_app = MIMEText(content, mimeType, _charset=self.charset)
            msgRoot.attach(content_app)
            msg = msgRoot
        else:
            msg = MIMEText(content, mimeType, self.charset)

        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = ",".join(receiver)
        return server.sendmail(self.sender, receiver, msg.as_string())

    def send_file(self, subject, content, receiver, file):
        filename = os.path.basename(file)
        msgRoot = MIMEMultipart("relate")

        fileapp = MIMEApplication(open(file, "rb").read())
        fileapp.add_header("Content-Type", "application/octet-stream")
        fileapp.add_header("Content-Disposition", "attachment", filename=filename)
        msgRoot.attach(fileapp)

        return self.send_email(subject, content, receiver, msgRoot)

    def send_dir(self, subject, content, receiver, path):
        file = shutil.make_archive(os.path.basename(path), "zip", path)
        senderrs = self.send_file(subject, content, receiver, file)
        os.remove(file)
        return senderrs


if __name__ == "__main__":
    smtp_server = "smtp.163.com"
    sender = "18719091650@163.com"
    password = "qq5201314ouru"
    receiver = ["gzgdouru@163.com"]

    sendEmail = SendEmail(smtp_server, sender, password)
    # print(sendEmail.send_email("8折大酬宾", "全场商品一律8折, 快来抢购吧!", receiver))
    # print(sendEmail.send_file("8折大酬宾", "全场商品一律8折, 快来抢购吧!", receiver, file="semail.py"))
    print(sendEmail.send_dir("8折大酬宾", "全场商品一律8折, 快来抢购吧!", receiver, path="."))
