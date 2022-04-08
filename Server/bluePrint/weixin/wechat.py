# coding:utf-8
from flask import Blueprint, request
from hashlib import sha1
from xml.etree import ElementTree

from Server.api.pc.getNewestNews import *  # 获取新闻

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

        # if request.data:
        #     XMLData = request.data.decode('utf-8')
        #     ElementTree.parse(XMLData)

        return """
        <xml>
          <ToUserName><![CDATA[oKV3l6GA5S1Bnnakk_ThJvqdbbIA]]></ToUserName>
          <FromUserName><![CDATA[gh_dcd30c3d7c29]]></FromUserName>
          <CreateTime>12345678</CreateTime>
          <MsgType><![CDATA[text]]></MsgType>
          <Content><![CDATA[你好]]></Content>
        </xml>
        """
    else:
        return ""
