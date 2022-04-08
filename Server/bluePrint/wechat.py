# coding:utf-8
from flask import Flask, Blueprint, request, jsonify, render_template
from hashlib import sha1
from Config.GlobalSetting import MYSQL_CONFIG
from Server.api.getMachineListApi import *  # 获取随机推荐
from Server.api.getMediaListApi import *  # 获取信源
from Server.api.getMachinePage import get_page, get_relation_page
from Server.api.getNewestNews import *  # 获取新闻
import re

mysqlOBJ = MYSQL(CONFIG=MYSQL_CONFIG, db='machinedb')  # 该视图的专用mysql对象

weChat_bp = Blueprint('weChat', __name__)


@weChat_bp.route('/wx')
def weChat():
    args = request.args

    signature = args.get('signature')

    nonce = args.get('nonce')

    timestamp = args.get('timestamp')

    echoStr = args.get('echoStr')
    token = 'xun123'

    args_list = [
        token, timestamp, nonce
    ]
    args_list.sort()
    shaObj = sha1()


    shaObj.update(args_list[0].encode('utf-8'))
    shaObj.update(args_list[1].encode('utf-8'))
    shaObj.update(args_list[2].encode('utf-8'))

    hashcode = shaObj.hexdigest()
    with open('ok.txt', 'w') as f:
        f.write(
            signature + '\n' + nonce + '\n' + timestamp + '\n' + echoStr + '\n' + token + '\n' + str(
                args_list) + '\n' + hashcode

        )
    if hashcode == signature:
        return echoStr
    else:
        return ""
