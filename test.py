# coding:utf-8
import requests
from xml.etree import ElementTree
import xmltodict
xml = """<xml><ToUserName><![CDATA[gh_dcd30c3d7c29]]></ToUserName>\n<FromUserName><![CDATA[oKV3l6GA5S1Bnnakk_ThJvqdbbIA]]></FromUserName>\n<CreateTime>1649427585</CreateTime>\n<MsgType><![CDATA[text]]></MsgType>\n<Content><![CDATA[你好]]></Content>\n<MsgId>23614122573209947</MsgId>\n</xml>"""
xmlDict = xmltodict.parse(xml)['xml']

FtoUserName = xmlDict['ToUserName']
FFromUserName = xmlDict['FromUserName']
FCreateTime = xmlDict['CreateTime']
FMsgType = xmlDict['MsgType']

FContent = xmlDict['Content']
FMsgId = xmlDict['MsgId']


dic = {"xml":{
    "ToUserName":FFromUserName,
    "FromUserName":FtoUserName,
    "CreateTime":FCreateTime,
    "MsgType":FMsgType,
    "Content":FContent,
    "MsgId":FMsgId
}}

x = xmltodict.unparse(dic)

print(x)