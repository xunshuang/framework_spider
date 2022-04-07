from flask import Flask, Blueprint, request,jsonify,render_template,url_for,redirect

from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG

from Server.api.getMachineListApi import * # 获取随机推荐
from Server.api.getMediaListApi import * #获取信源


mysqlOBJ = MYSQL(CONFIG=MYSQL_CONFIG,db='machinedb')  # 该视图的专用mysql对象

mysql, cursor = mysqlOBJ.get_mysql()

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def pre_index():
    random_data = get_random_recommend(mysqlOBJ) # 随机 10条数据
    media_list = get_media(mysqlOBJ)

    return render_template("index.html",media_list=media_list,random_data1=random_data[0:5],random_data2=random_data[5::])


# 首页
@index_bp.route('/index')
def index():

    random_data = get_random_recommend(mysqlOBJ) # 随机 10条数据
    media_list = get_media(mysqlOBJ)

    return render_template("index.html",media_list=media_list,random_data1=random_data[0:5],random_data2=random_data[5::])

