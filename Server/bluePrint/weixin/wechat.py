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
        xmlDict = xmltodict.parse(request.data.decode('utf-8'))['xml']

        FToUserName = xmlDict['ToUserName']
        FFromUserName = xmlDict['FromUserName']
        FCreateTime = xmlDict['CreateTime']
        FMsgType = xmlDict['MsgType']

        FMsgId = xmlDict.get('MsgId')

        if 'event' in FMsgType:
            TContent = Map['event'][FMsgType]()
            returnJson = {
                "ToUserName": FFromUserName,
                "FromUserName": FToUserName,
                "CreateTime": FCreateTime,
                "MsgType": "text",
                "Content": TContent,
            }
            return xmltodict.unparse({"xml":returnJson}) # 事件监听

        elif "text" in FMsgType:
            try:
                FContent = xmlDict['Content']
                TContent = Map['message'][FMsgType](FContent)

                returnJson = {
                    "ToUserName": FFromUserName,
                    "FromUserName": FToUserName,
                    "CreateTime": FCreateTime,
                    "MsgType": "text",
                    "Content": TContent,
                }
                returnXML = xmltodict.unparse({"xml":returnJson})

                return  returnXML # 复读机模式

            except:
                FContent = xmlDict['Content'] # 不清楚指令就复读呗
                TContent = Map['message']['repeat'](FContent)

                returnJson = {
                    "ToUserName": FFromUserName,
                    "FromUserName": FToUserName,
                    "CreateTime": FCreateTime,
                    "MsgType": "text",
                    "Content": TContent,
                }
                returnXML = xmltodict.unparse({"xml": returnJson})

                return returnXML  # 复读机模式
        else:

            returnJson = {
               "ToUserName":FFromUserName,
               "FromUserName":FToUserName,
               "CreateTime":FCreateTime,
               "MsgType":"text",
               "Content":"你说的这个我看不懂，输入 !help 获取全部指令！",
               "MsgId":FMsgId
            }
            return xmltodict.unparse({"xml":returnJson})

    else:
        return ""
