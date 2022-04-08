# coding:utf-8
import requests

url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxb28f616376c291c5&secret=af45f60a585ebb78ac5b7876318c9216'

resp = requests.get(url)

print(resp.text)