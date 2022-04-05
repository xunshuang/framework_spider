from flask import Flask, Blueprint, request, jsonify, render_template,make_response

from Config.GlobalSetting import MYSQL_CONFIG
from Config.GlobalSetting import MYSQL_CONFIG

from Server.api.getMachineListApi import *  # 获取随机推荐
from Server.api.getMediaListApi import *  # 获取信源
from Server.api.getMachinePage import get_page,get_relation_page
from Server.api.getNewestNews import * # 获取新闻
from Server.api.getNewsPage import * # 获取详情新闻
mysqlOBJ = MYSQL(CONFIG=MYSQL_CONFIG,db='machinedb')  # 该视图的专用mysql对象

news_single_bp = Blueprint('news_single', __name__)


@news_single_bp.route('/news_single/<md5hash>')
def news_single(md5hash):
    # 信源列表
    media_list = get_media(mysqlOBJ)


    #获取详情页新闻
    news_page = get_news_page(mysqlOBJ,md5hash)

    # 获取新闻列表
    news_list = get_newest(mysqlOBJ)
    for _ in news_list:
        if not _['machineImg']:
            _['machineImg'] = '/images/imageLost.png'

    prefix = "/"

    Response = make_response(
        render_template(
            'news_single.html',
            media_list=media_list,
            news_page=news_page,
            news_list=news_list,
            prefix=prefix

        )
    )
    return Response
