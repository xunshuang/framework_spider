# coding:utf-8

from flask import Flask, Blueprint, request, jsonify, render_template, url_for, redirect, make_response
from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
from Server.api.encrypt import enc, dec
import json
from Server.api.getMachineListApi import *  # 获取随机推荐
from Server.api.getMediaListApi import *  # 获取信源


mysqlOBJ = MYSQL(CONFIG=MYSQL_CONFIG, db='machinedb')  # 该视图的专用mysql对象
list_bp = Blueprint('list', __name__)


@list_bp.route('/list/<machineSiteId>', methods=['GET'])
def lists(machineSiteId):
    media_list = get_media(mysqlOBJ)
    return render_template('list.html',
                           media_list=media_list,
                           machineSiteId=machineSiteId,
                           prefix='/'
                           )


@list_bp.route('/list/mediaMap', methods=['POST'])
def get_media_map():
    form = request.form
    machineSiteId = form.get('machineSiteId') or 'A001'
    media_dict = get_media_dict(mysqlOBJ, machineSiteId)
    return jsonify(media_dict)


# 选择分栏并获取第一页数据
@list_bp.route('/select_list', methods=['POST'])
def select_list():
    form = request.form
    levelClassOne = form.get('levelClassOne') or ""
    levelClassTwo = form.get('levelClassTwo') or ""
    levelClassThree = form.get('levelClassThree') or ""

    page = form.get('page') or 1
    pageSize = form.get('pagesize') or 10
    siteId = form.get('machineSiteId')
    list_result = roll_page(
        mysqlOBJ, page=page, machineSiteId=siteId,
        levelClassOne=levelClassOne,
        levelClassTwo=levelClassTwo,
        levelClassThree=levelClassThree,
        pagesize=pageSize
    )
    for res in list_result:
        res['machineImg'] = res['machineImg'].split('$$$')[0] if res['machineImg'] else ""
        res["machinePublishTime"] = res["machinePublishTime"].strftime("%Y-%m-%d")
        if not res['machineImg']:
            res['machineImg'] = '/images/imageLost.png'

    data_count = get_list_page(mysqlOBJ, levelClassOne=levelClassOne, levelClassTwo=levelClassTwo,
                               levelClassThree=levelClassThree, machineSiteId=siteId)
    max_page = int(data_count / 10) + 1 if data_count % 10 else int(data_count / 10)
    page_list = get_page_list(max_page=max_page, now_page=page)
    Response = make_response(
        render_template(
            ['list_template.html'],
            random_data1=list_result,
            data_count=data_count,
            page_list = page_list,
            now_page = page
        )
    )

    cookie_args = enc(levelClassOne) + '$$' + enc(levelClassTwo) + '$$' + enc(levelClassThree) + '$$' + enc(siteId)
    Response.set_cookie('args', cookie_args)  # 更新一下 cookie
    Response.set_cookie('max_count', str(data_count))  # 更新一下 最大条数 cookie

    return Response


# 选择分栏并获取第一页数据
@list_bp.route('/rollPage',methods=['POST'])
def rollPage():
    args = request.form

    page = int(args.get('page')) or 0
    pageSize = args.get('pagesize') or 10

    cookie_args_list = list(map(dec, request.cookies.get('args').split('$$')))

    list_result = roll_page(
        mysqlOBJ, page=page, machineSiteId=cookie_args_list[3],
        levelClassOne=cookie_args_list[0],
        levelClassTwo=cookie_args_list[1],
        levelClassThree=cookie_args_list[2],
        pagesize=pageSize
    )
    for res in list_result:
        res['machineImg'] = res['machineImg'].split('$$$')[0] if res['machineImg'] else ""
        res["machinePublishTime"] = res["machinePublishTime"].strftime("%Y-%m-%d")
        if not res['machineImg']:
            res['machineImg'] = '/images/imageLost.png'

    data_count = get_list_page(mysqlOBJ, levelClassOne=cookie_args_list[0], levelClassTwo=cookie_args_list[1],
                               levelClassThree=cookie_args_list[2], machineSiteId=cookie_args_list[3])
    max_page = int(data_count / 10) + 1 if data_count % 10 else int(data_count / 10)
    page_list = get_page_list(max_page=max_page, now_page=page)
    Response = make_response(
        render_template(
            ['list_template.html'],
            random_data1=list_result,
            data_count=data_count,
            page_list=page_list,
            now_page=page
        )
    )
    return Response
