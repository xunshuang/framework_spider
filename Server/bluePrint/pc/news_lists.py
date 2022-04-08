# coding:utf-8

from flask import Blueprint, render_template, redirect, make_response
from Server.api.pc.getMediaListApi import *  # 获取信源
from Server.api.pc.getNewsList import * # 获取新闻列表

mysqlOBJ = MYSQL(CONFIG=MYSQL_CONFIG, db='machinedb')  # 该视图的专用mysql对象
news_list_bp = Blueprint('news_list', __name__)

@news_list_bp.route('/select_news_list')
def redirect_select_list():
    return redirect('/select_news_list/1')


# 选择分栏并获取第一页数据
@news_list_bp.route('/select_news_list/<page>')
def select_list(page):
    if not page:
        page = 1
    else:
        page = int(page)
    media_list = get_media(mysqlOBJ)

    max_count = get_news_max(mysqlOBJ) # 新闻最大条数


    max_page = int(max_count / 10) + 1 if max_count % 10 else int(max_count / 10) # 获取最大页数
    page_list = get_page_list(max_page,page) # 获取页数列表

    news_one_page_list =get_news_list(mysqlOBJ,page)
    Response = make_response(
        render_template(
            'news_list.html',
            prefix = '/',
            media_list=media_list,
            now_page=page,
            news_one_page_list=news_one_page_list,
            page_list=page_list
        )
    )

    # cookie_args = enc(levelClassOne)
    # Response.set_cookie('MachineArgs', cookie_args)  # 更新一下 cookie
    # Response.set_cookie('max_count', str(data_count))  # 更新一下 最大条数 cookie
    # print(time.time() - bt)

    return Response


