# coding:utf-8
# 初始化一个ding-ding机器人类
import time
import hmac
import hashlib
import base64
import urllib.parse
import asyncio
import aiohttp
import json


class DingTalk():
    def __init__(
            self,
            at: str or bool or list = None,
            text: str = "",
            json_data: dict = None
    ):
        self.at = at
        self.text = text
        self.json_data = json_data
        self.msg = {
            "at": {
                "atMobiles": [

                ],
                "isAtAll": False
            },
            "text": {
                "content": """
[ ⭐⭐SureFly机床信息爬虫平台  ⭐⭐ ]
%s





(自动消息，无需回复，有问题请联系孟帅)
        🖊-- By MachineRobot ♥
                """
            },
            "msgtype": "text"
        }


    def init_at(self, at):
        self.at = at

    def init_text(self, text):
        self.text = str(text)

    def special_json(self, json_data: dict or str):
        if not isinstance(json_data, dict):
            try:
                json_data = json.dumps(json_data, ensure_ascii=False)
            except:
                raise Exception("JSON 格式不正确!")

        self.json_data = json_data

    @property
    def init_params(self):
        timestamp = str(round(time.time() * 1000))
        secret = 'this is secret'
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp,sign

    def init_msg(self):

        if self.at == 'ALL':
            self.msg['at']['isAtAll'] = True
        elif isinstance(self.at,str):
            self.msg['at']['atMobiles'].append(
                self.at
            )

        elif isinstance(self.at,list):
            self.msg['at']['atMobiles'] = self.at


        if self.text:
            self.msg["text"]['content'] = self.msg["text"]['content'] %(self.text)


    async def send_msg(self):
        timestamp,sign = self.init_params
        async with aiohttp.request('POST',url='https://oapi.dingtalk.com/robot/send?access_token='
                                             '270f8fe53c1e428094fbbfdce20bc2a3f8fd3a0072332587991ecc47a9d75bb7' +
                                             f'&timestamp={timestamp}&sign={sign}',json=self.msg) as resp:
            t = await resp.text()
            print(t)
            if resp.status == 200:
                return True,"发送成功"
            else:
                return False,"发送失败"

    @classmethod
    def send(cls,at,text,json_data=None):
        file = cls(at,text,json_data)
        file.init_msg()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(file.send_msg())


if __name__ == '__main__':
    DingTalk.send('15566528051',"爬虫程序:AJSpider【1/19】正在运行\n采集数据:【29条】\n更新数据:【22条】")