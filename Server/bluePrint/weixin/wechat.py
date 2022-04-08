# coding:utf-8
from flask import Blueprint, request
from hashlib import sha1
import xmltodict

from Server.api.pc.getNewestNews import *  # 获取新闻
from Server.api.weixin.FuncMap import Map


mysqlOBJ = MYSQL(CONFIG=MYSQL_CONFIG, db='machinedb')  # 该视图的专用mysql对象

weChat_bp = Blueprint('weChat', __name__)


# wxb28f616376c291c5
# af45f60a585ebb78ac5b7876318c9216

@weChat_bp.route('/wx', methods=['GET', 'POST'])
def weChat():
    print('##########', request.data)

    args = request.args

    signature = args.get('signature')
    nonce = args.get('nonce')
    timestamp = args.get('timestamp')
    echoStr = args.get('echostr')
    token = 'xunshu4ng202204081618'

    args_list = [
        token, timestamp, nonce
    ]

    args_list.sort()
    shaObj = sha1()

    shaObj.update(args_list[0].encode('utf-8'))
    shaObj.update(args_list[1].encode('utf-8'))
    shaObj.update(args_list[2].encode('utf-8'))

    hashcode = shaObj.hexdigest()

    if hashcode == signature:
        return """<xml><ToUserName>oKV3l6GA5S1Bnnakk_ThJvqdbbIA</ToUserName><FromUserName>gh_dcd30c3d7c29</FromUserName><CreateTime>1649427585</CreateTime><MsgType>text</MsgType><Content>你好</Content><MsgId>23614122573209947</MsgId></xml>"""
        xmlDict = xmltodict.parse(request.data.decode('utf-8'))['xml']

        FtoUserName = xmlDict['ToUserName']
        FFromUserName = xmlDict['FromUserName']
        FCreateTime = xmlDict['CreateTime']
        FMsgType = xmlDict['MsgType']

        FContent = xmlDict['Content']
        FMsgId = xmlDict['MsgId']

        if 'event' in FMsgType:
            pass
        elif "message" in FMsgType:
            pass
        returnJson = {
           "toUserName":FFromUserName,
           "FromUserName":FtoUserName,
           "CreateTime":FCreateTime,
           "MsgType":"",
           "Content":"",
           "MsgId":""
        }
        # return xmltodict.unparse(returnJson)

    else:
        return ""
