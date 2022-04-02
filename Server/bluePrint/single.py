from flask import Flask, Blueprint, request, jsonify, render_template

from Config.GlobalSetting import MYSQL_CONFIG
from Config.GlobalSetting import MYSQL_CONFIG

from Server.api.getMachineListApi import *  # 获取随机推荐
from Server.api.getMediaListApi import *  # 获取信源
from Server.api.getMachinePage import get_page,get_relation_page

mysqlOBJ = MYSQL(CONFIG=MYSQL_CONFIG,db='machinedb')  # 该视图的专用mysql对象

single_bp = Blueprint('single', __name__)


# 首页

@single_bp.route('/single/<md5hash>')
def single(md5hash):

    machine_data = get_page(mysqlOBJ, md5hash)

    imgList = [_ for _ in machine_data['machineImg'].split('$$$')]
    if not imgList or imgList == [""]:
        imgList = ['/images/imageLost.png']
    machineLocation = "-".join([_ for _ in [machine_data["machineLocalClassOne"], machine_data["machineLocalClassTwo"],
                                machine_data["machineLocalClassThree"]] if _])
    dataDict = {
        "品牌": machine_data["machineModel"],
        "状态": {"1": "已出售", "2": "展示中", "99": "未知状态"}[str(machine_data["machineStatus"])],
        "所在地": machineLocation,
        "出厂日期": machine_data["machineManufacture"],
        "产品质量": machine_data["machineQuality"],
        "联系人/公司": machine_data["machineContact"],
        "联系方式": {"1": "手机", "2": "电话", "3": "微信", "4": "QQ", "5": "未知联系方式"}[str(machine_data["machineContactWay"])] + ' - ' +
                machine_data["machineContactInfo"],
        "数据发布时间": machine_data["machinePublishTime"]
    }
    # 过滤掉无效数据
    for k,v in dataDict.copy().items():
        if not v:
            dataDict.pop(k)

    # 获取关联信息
    relation_data = get_relation_page(mysqlOBJ,contact=str(machine_data["machineContactInfo"]))

    machineInfo = machine_data['machineInfo'].decode()

    media_list = get_media(mysqlOBJ)

    prefix = "/"
    return render_template("single.html",
                           prefix=prefix,
                           machine_data=machine_data,
                           imgList=imgList,
                           dataDict=dataDict,
                           machineInfo=machineInfo,
                           relation_data =relation_data,
                           media_list = media_list
                           )
