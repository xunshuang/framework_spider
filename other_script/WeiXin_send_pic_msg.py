# coding:utf-8
# 定时发送-图文消息 每日机床信息

import os
import sys
import time
import json
sys.path.append('/workspace/framework_spider/')
import requests
from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime

mysqlObj = MYSQL(MYSQL_CONFIG, db='machinedb')

# dateNum = int(sys.argv[-1])

# 获取 accessToken
def get_accessToken():
    mysql, cursor = mysqlObj.get_mysql()
    sql = 'SELECT `machineAccessToken` FROM `machineToken`;'
    cursor.execute(sql)
    mysql.commit()
    _ = cursor.fetchone()
    if _['machineAccessToken']:
        return _['machineAccessToken']
    else:
        time.sleep(1)
        return get_accessToken()

# 获取分组情况
def get_group_id():
    url = "https://api.weixin.qq.com/cgi-bin/groups/get"
    payload_id = {
        'access_token': get_accessToken()
    }
    resp = requests.get(url=url, params=payload_id)
    result = resp.json()
    for group in result['groups']:
        if group['count'] != 0:
            yield group['id']

def get_machine_msg(dateNum):
    if dateNum >= 8:
        mysql, cursor = mysqlObj.get_mysql()
        SQL_SEARCH_MACHINE_DAY = 'SELECT * FROM `machineDay` ORDER BY `machinePublishTime` DESC LIMIT 14'
        cursor.execute(SQL_SEARCH_MACHINE_DAY)
        mysql.commit()

        md5hash = cursor.fetchall()[dateNum - 8]['md5hash']

        SQL_SEARCH_MACHINE = 'SELECT * FROM `machineData` WHERE `md5hash` = %s;'
        cursor.execute(SQL_SEARCH_MACHINE,md5hash)
        mysql.commit()
        machine_data = cursor.fetchall()[dateNum - 8]

        imgListRaw = [_ for _ in machine_data['machineImg'].split('$$$')]
        if not imgListRaw or imgListRaw == [""]:
            imgListRaw = ['http://www.mengshuai.top/images/imageLost.png']

        machineLocation = "-".join(
            [_ for _ in [machine_data["machineLocalClassOne"], machine_data["machineLocalClassTwo"],
                         machine_data["machineLocalClassThree"]] if _])
        dataDict = {
            "品牌": machine_data["machineModel"],
            "状态": {"1": "已出售", "2": "展示中", "99": "未知状态"}[str(machine_data["machineStatus"])],
            "所在地": machineLocation,
            "出厂日期": machine_data["machineManufacture"],
            "产品质量": machine_data["machineQuality"],
            "联系人/公司": machine_data["machineContact"],
            "联系方式": {"1": "手机", "2": "电话", "3": "微信", "4": "QQ", "5": "未知联系方式"}[
                        str(machine_data["machineContactWay"])] + ' - ' +
                    machine_data["machineContactInfo"],
            "数据发布时间": machine_data["machinePublishTime"]
        }
        machineInfo = machine_data['machineInfo'].decode()

        String = ""
        for k,v in dataDict.items():
            String += k + ':' + v + '\n'

        String += '详情:' + machineInfo

        groups = get_group_id()

        for groupId in groups:
            doc = {
                "filter":{
                    "is_to_all":True,
                    "group_id":""
                },
                "text":{
                    "content":String
                },
                "msgtype":'text'
            }

            msgUrl = 'https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token=' + get_accessToken()

            r = requests.post(url=msgUrl,data = json.dumps(doc,ensure_ascii=False,indent=2))
            result = r.json()
            print(result)

def get_openid(openId=None):
    mysql, cursor = mysqlObj.get_mysql()
    SQL_SEARCH = 'SELECT `machineOpenId` FROM `machineWXUser` WHERE `machineSubMachine` = "1";'
    cursor.execute(SQL_SEARCH)
    mysql.commit()
    for openId in cursor.fetchall():
        yield openId['machineOpenId']


def get_media_id(imgListRaw):
    pass


# 发送消息
def send_msg():
    doc = {

    }


if __name__ == '__main__':
    get_machine_msg(8)
