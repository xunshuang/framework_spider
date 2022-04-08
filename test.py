# coding:utf-8
import requests
from xml.etree import ElementTree
import xmltodict
xml = """
<xml>
    <ToUserName><![CDATA[gh_dcd30c3d7c29]]></ToUserName>
    <FromUserName><![CDATA[oKV3l6GA5S1Bnnakk_ThJvqdbbIA]]></FromUserName>
    <CreateTime>1649425111</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[hi]]></Content>
    <MsgId>23614090191492520</MsgId>
</xml>
"""

xmlDict = xmltodict.parse(xml)['xml']

FtoUserName = xmlDict['ToUserName']
FFromUserName = xmlDict['FromUserName']
FCreateTime = xmlDict['CreateTime']
FMsgType = xmlDict['MsgType']

FContent = xmlDict['Content']
FMsgId = xmlDict['MsgId']


print(FtoUserName)