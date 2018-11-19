import requests
import json


class YDMHttp:
    apiurl = 'http://api.yundama.com/api.php'

    def __init__(self, username, password, appid=6098, appkey="a939203e868bd9d93a8c09f4c3161901"):
        self.userinfo = dict(
            username=username,
            password=password,
            appid=appid,
            appkey=appkey,
        )

    def login(self):
        data = {"method": "login"}
        data.update(self.userinfo)
        try:
            response = requests.post(self.apiurl, data=data)
            response = json.loads(response.text)
            if response['ret'] < 0:
                raise RuntimeError("[云打码]登录失败, 错误代码:{0}".format(response['ret']))
            else:
                return response['uid']
        except Exception as e:
            raise RuntimeError("[云打码]登录失败, 错误原因:{0}".format(e))

    def balance(self):
        data = {"method": "balance"}
        data.update(self.userinfo)
        try:
            response = requests.post(self.apiurl, data=data)
            response = json.loads(response.text)
            if response['ret'] < 0:
                raise RuntimeError("[云打码]查询余额失败, 错误代码:{0}".format(response['ret']))
            else:
                return response['balance']
        except Exception as e:
            raise RuntimeError("[云打码]查询余额失败, 错误原因:{0}".format(e))

    def decode(self, filename, codetype=1004, timeout=30):
        data = {"method": "upload", "codetype": str(codetype), "timeout": str(timeout)}
        data.update(self.userinfo)

        try:
            file = {"file" : open(filename, "rb")}
            response = requests.post(self.apiurl, data=data, files=file)
            response = json.loads(response.text)
            if response["ret"] < 0:
                raise RuntimeError("[云打码]上传文件失败, 错误代码:{0}".format(response["ret"]))

            data["method"] = "result"
            data["cid"] = str(response["cid"])
            response = requests.post(self.apiurl, data=data)
            response = json.loads(response.text)
            if response["ret"] < 0:
                raise RuntimeError("[云打码]解码失败, 错误代码:{0}".format(response["ret"]))
            return response["text"]
        except Exception as e:
            raise RuntimeError("[云打码]解码失败, 错误原因:{0}".format(e))


if __name__ == "__main__":
    ydm = YDMHttp(username="shuaiguo", password="5201314ouru")
    print("uid: {0}".format(ydm.login()))
    print("balance: {0}".format(ydm.balance()))
    # print(ydm.decode("captcha.jpeg"))
    # print(ydm.decode("11.jpg", codetype=2000))
    # print(ydm.decode("4.png"))
    # print(ydm.decode("fucklaji.png", codetype=2004))
    print(ydm.decode("ex.png", codetype=4006))