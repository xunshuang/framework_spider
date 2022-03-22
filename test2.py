#python 3.8
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests

timestamp = str(round(time.time() * 1000))
secret = 'this is secret'
secret_enc = secret.encode('utf-8')
string_to_sign = '{}\n{}'.format(timestamp, secret)
string_to_sign_enc = string_to_sign.encode('utf-8')
hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))


url = 'https://oapi.dingtalk.com/robot/send?access_token=270f8fe53c1e428094fbbfdce20bc2a3f8fd3a0072332587991ecc47a9d75bb7' + f'&timestamp={timestamp}&sign={sign}'

resp= requests.post(
    url=url,json={
        "at":{
          "atMobiles":[
          ]
        },
        "text":{
            "content":"""
                此刻尽丝滑！
                我的妈呀
                        --By spider
            """
        },
        "msgtype":"text"
    }
)
print(resp.text)