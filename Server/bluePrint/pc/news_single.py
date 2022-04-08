from flask import Blueprint, render_template,make_response

from Server.api.pc.getMediaListApi import *  # 获取信源
from Server.api.pc.getNewestNews import * # 获取新闻
from Server.api.pc.getNewsPage import * # 获取详情新闻
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
