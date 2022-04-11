# coding:utf-8
from flask import Blueprint, request
from hashlib import sha1
import xmltodict

from Server.api.pc.getNewestNews import *  # 获取新闻
from Server.api.weixin.FuncMap import Map

mysqlOBJ = MYSQL(CONFIG=MYSQL_CONFIG, db='machinedb')  # 该视图的专用mysql对象

weChat_bp = Blueprint('weChat', __name__)


# 正式号码
# wxb28f616376c291c5
# af45f60a585ebb78ac5b7876318c9216

# 测试号码
# wxc90805c8f9e1aaae
# 127c9bf502b937e3d3a5a2db503cfb21

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

        FToUserName = xmlDict['ToUserName']  # 发给谁
        FFromUserName = xmlDict['FromUserName']  # 从哪来
        FCreateTime = xmlDict['CreateTime']  # 创建时间
        FMsgType = xmlDict['MsgType']  # 消息类型

        if 'event' in FMsgType:
            EVENT = xmlDict['Event']  # 事件类型
            TContent = Map['event'][EVENT](mysqlOBJ=mysqlOBJ, xmlDict=xmlDict)
            returnJson = {
                "ToUserName": FFromUserName,
                "FromUserName": FToUserName,
                "CreateTime": FCreateTime,
                "MsgType": "text",
                "Content": TContent,
            }
            return xmltodict.unparse({"xml": returnJson})  # 菜单事件监听


        elif "text" in FMsgType:

            TContent = Map['message'](mysqlOBJ=mysqlOBJ, xmlDict=xmlDict)

            returnJson = {
                "ToUserName": FFromUserName,
                "FromUserName": FToUserName,
                "CreateTime": FCreateTime,
                "MsgType": "text",
                "Content": TContent,
            }
            returnXML = xmltodict.unparse({"xml": returnJson})

            return returnXML  # 指令模式



    else:
        return ""
