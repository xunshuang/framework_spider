# coding:utf-8

from flask import Flask, Blueprint, request,jsonify,render_template,url_for,redirect

from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
import json
from Server.api.getMachineListApi import * # 获取随机推荐
from Server.api.getMediaListApi import * #获取信源


mysqlOBJ = MYSQL(CONFIG=MYSQL_CONFIG,db='machinedb')  # 该视图的专用mysql对象

list_bp = Blueprint('list', __name__)



@list_bp.route('/list/<machineSiteId>/<page>',methods=['GET'])
def lists(machineSiteId,page):
    media_list = get_media(mysqlOBJ)
    return render_template('list.html',
                           media_list=media_list,
                           machineSiteId=machineSiteId,
                           prefix = '/'
                           )


@list_bp.route('/list/mediaMap',methods=['POST'])
def get_media_map():
    form = request.form
    machineSiteId = form.get('machineSiteId')
    media_dict = get_media_dict(mysqlOBJ,machineSiteId)
    return jsonify(media_dict)


# 选择分栏
@list_bp.route('/select_list',methods=['POST'])
def select_list():
    form = request.form
    levelClassOne = form.get('levelClassOne') or ""
    levelClassTwo = form.get('levelClassTwo') or ""
    levelClassThree = form.get('levelClassThree') or ""


    page = form.get('page') or 0
    pageSize = form.get('pagesize') or 20
    siteId = form.get('machineSiteId')

    list_result = roll_page(
        mysqlOBJ,page=page,machineSiteId=siteId,
        levelClassOne = levelClassOne,
        levelClassTwo = levelClassTwo,
        levelClassThree = levelClassThree,
        pagesize=pageSize
    )
    for res in list_result:
        res['machineImg'] = res['machineImg'].split('$$$')[0] if res['machineImg'] else ""
        res["machinePublishTime"] = res["machinePublishTime"].strftime("%Y-%m-%d")
        if not res['machineImg']:
            res['machineImg'] = '/images/imageLost.png'

    return render_template('list_template.html',random_data1=list_result)

