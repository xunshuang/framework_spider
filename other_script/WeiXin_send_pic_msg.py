# coding:utf-8
# 定时发送-图文消息 每日机床信息 从早8点到晚上22点

import os
import sys
import time
import json
import hashlib
import jinja2

sys.path.append('/workspace/framework_spider/')
import requests
from Db.MySQLClient.client import MYSQL
from Config.GlobalSetting import MYSQL_CONFIG
from datetime import datetime

mysqlObj = MYSQL(MYSQL_CONFIG, db='machinedb')


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


# 制作草稿
def make_machine_msg_to_draft(dateNum):
    print(f"正在制作 {dateNum} 点的草稿  今日第{dateNum - 8}份")
    mysql, cursor = mysqlObj.get_mysql()
    SQL_SEARCH_MACHINE_DAY = 'SELECT * FROM `machineDay` ORDER BY `machinePublishTime` DESC LIMIT 30'
    cursor.execute(SQL_SEARCH_MACHINE_DAY)
    mysql.commit()

    _ = cursor.fetchall()[dateNum - 8]
    md5hash = _['md5hash']

    SQL_SEARCH_MACHINE = 'SELECT * FROM `machineData` WHERE `md5hash` = %s;'
    cursor.execute(SQL_SEARCH_MACHINE, md5hash)
    mysql.commit()
    machine_data = cursor.fetchone()

    imgListRaw = [_ for _ in machine_data['machineImg'].split('$$$')]
    if not imgListRaw or imgListRaw == [""]:
        imgListRaw = ['imageLost']
    imgList,imgDeleteList = get_media_id(imgListRaw)
    machineLocation = "-".join(
        [_ for _ in [machine_data["machineLocalClassOne"], machine_data["machineLocalClassTwo"],
                     machine_data["machineLocalClassThree"]] if _])
    dataDict = {
        "品牌": machine_data["machineModel"],
        "状态": {"1": "已出售", "2": "展示中", "99": "未知状态"}[str(machine_data["machineStatus"])],
        "所在地": machineLocation,
        # "出厂日期": machine_data["machineManufacture"],
        "产品质量": machine_data["machineQuality"],
        "联系人/公司": machine_data["machineContact"],
        "联系方式": {"1": "手机", "2": "电话", "3": "微信", "4": "QQ", "5": "未知联系方式"}[
                    str(machine_data["machineContactWay"])] + ' - ' +
                machine_data["machineContactInfo"],
        "数据发布时间": machine_data["machinePublishTime"].strftime("%Y-%m-%d")
    }
    machineInfo = machine_data['machineInfo'].decode('utf-8').replace('，联系我时，请说明是从处理网看到的。','。')

    html_title = f'<title>{machine_data["machineTitle"]}</title>'
    html_h1 = f'<h1 class="title-h1" style="color: white;text-align: center;font-size: 2rem;width: 80%;margin-left: 10%;border-bottom: 2px solid white;">{machine_data["machineTitle"]}</h1>'
    html_info = "".join([f"""<img src="{img}" style="max-width: 80%;height: auto;">""" for img in imgList]) +\
                '<div class="prefix"  style="margin: 3.125rem;"></div>' +\
                "".join([f"""<span style="width: 100%;"><p style="width: 100%;text-align: center;color: white;">{key}:{value}</p></span>""" for key,value in dataDict.items() if key !='联系方式' and value]) + f"""<span><b style="width: 100%;text-align: center;color: orangered;">联系方式:{dataDict['联系方式']}</b></span>"""

    html_detail = f'<p style="width: 100%;text-align=left;">{machineInfo}</p>'
    content = """
    <html>
	<head>
		"""+html_title+"""
	</head>
	<body>
		<div class="container" style="width: 100%;height: 100%;position: fixed;overflow-x: hidden;overflow-y: scroll;text-align: center;background: black;">
			<div class="content" sytle="position: relative;margin-top: 5rem;width: 80%;height: auto;margin-left: 10%;margin-bottom: 10%;background: rgba(0, 0, 0, 0.6);border: 0.0625rem solid white;border-radius: 1.25rem;">
				""" +html_h1 + """
				<div>
					<img src="http://mmbiz.qpic.cn/mmbiz_png/rISx4vUsIspTjB0u3Fial4FQqhkjrx8Piahs9OGDss8PUlRmk8ickUYAR5pq55ZpbNZvDhkBByzQ257xh380icZc6w/0" style="max-width: 80%;height: auto;"/>
					<div class="prefix" style="margin: 3.125rem;"></div>
					<div class="info" style="width: 80%;margin-left: 10%;text-align: center;padding-bottom: 2rem;">

						""" + html_info + '   <div class="prefix" style="margin: 3.125rem;"></div>' +"""



					</div>

					<div class="details" style="width: 80%;margin-left: 10%;color: white;margin-bottom: 2.5em;padding-bottom:2.5em;border-bottom: 0.125rem solid white;">
"""+ html_detail + """					</div>
					<span style="width: 100%;">
						<p class="warnings" style="text-align: center;font-size: 14px;color: red;width: 80%;margin-left: 10%;font-weight: 800;">【交易注意事项】</p>
					</span>
					<span style="width: 100%;">
						<p class="warnings" style="text-align: left;font-size: 14px;color: red;width: 80%;margin-left: 10%;font-weight: 800;">1. 未见实物，先交定金的，风险极高！！！</p>
					</span>
					<span style="width: 100%;">
						<p class="warnings" style="text-align: left;font-size: 14px;color: red;width: 80%;margin-left: 10%;font-weight: 800;">2. 动身看货前需先确认产品型号、设备是否还在、产权是否清晰等重要信息，以免白跑一趟；</p>
					</span>
					<span style="width: 100%;">
						<p class="warnings" style="text-align: left;font-size: 14px;color: red;width: 80%;margin-left: 10%;font-weight: 800;">3. 价格远低于市场价请慎重购买，要深刻理解一分钱一分货的道理；</p>
					</span>
					<span style="width: 100%;">
						<p class="warnings" style="text-align: left;font-size: 14px;color: red;width: 80%;margin-left: 10%;font-weight: 800;">4. 仔细检查设备能否正常使用</p>
					</span>
					<span style="width: 100%;">
						<p class="warnings" style="text-align: left;font-size: 14px;color: red;width: 80%;margin-left: 10%;font-weight: 800;">5. 认真核对发票、质保证书、身份证、营业执照等信息，并拍照留存；</p>
					</span>
					<span style="width: 100%;">
						<p class="warnings" style="text-align: left;font-size: 14px;color: red;width: 80%;margin-left: 10%;font-weight: 800;">6. 收货验货时请仔细核对，谨防调包；</p>
					</span>
					<span style="width: 100%;">
						<p class="warnings" style="text-align: left;font-size: 14px;color: red;width: 80%;margin-left: 10%;font-weight: 800;">7. 本公众号信息来自互联网，不核实信息的真实性、有效性、也不参与交易环节；</p>
					</span>
                    <div class="prefix" style="margin: 3.125rem;"></div>

					<!-- </div> -->
				</div>


			</div>

		</div>

	</body>
</html>
"""




    article = {
        "title": f"{datetime.now().strftime('%Y-%m-%d')} 第{dateNum - 8}份 {machine_data['machineTitle']}",  # 标题
        "author": "寻霜",
        "digest": machineInfo.replace('\n','').strip()[:50],
        "content": content,
        "content_source_url": f'http://www.mengshuai.top/single/{machine_data["md5hash"]}.html',
        "thumb_media_id": 'dwZxgP0_byDB5IVBizZ-N8iGY-K6ZIStR_MDMPbMe_1bLNfyyLlQB2jy7I0_MBkQ',
        "need_open_comment": 0,
        "only_fans_can_comment": 0
    }

    js = json.dumps({
        "articles":[
            article
        ]
    },ensure_ascii=False)
    url_upload = 'https://api.weixin.qq.com/cgi-bin/draft/add?access_token=' + get_accessToken()
    resp = requests.post(url=url_upload,data=js.encode('utf-8')).json()

    for delete in imgDeleteList:
        os.remove(delete)
    print('图片删除成功！')


    if resp.get('media_id'):
        print('草稿报存成功，media_id:',resp.get('media_id'))
        return resp.get('media_id'),machine_data["machineTitle"]
    else:
        print(resp)

def get_openid(openId=None):
    mysql, cursor = mysqlObj.get_mysql()
    SQL_SEARCH = 'SELECT `machineOpenId` FROM `machineWXUser` WHERE `machineSubMachine` = "1";'
    cursor.execute(SQL_SEARCH)
    mysql.commit()
    for openId in cursor.fetchall():
        yield openId['machineOpenId']


def get_media_id(imgListRaw):
    imgList = []
    imgDeleteList = []
    print('图片上传任务长度:', len(imgListRaw))
    for rawImg in imgListRaw:
        if 'http' in rawImg:
            print(f'正在上传第{imgListRaw.index(rawImg) + 1}个图片')
            headers_download = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'cross-site',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
            }

            imgContent = requests.get(url=rawImg, headers=headers_download).content
            imgName = 'MachineImg_' + hashlib.md5(rawImg.encode('utf-8')).hexdigest() + '.jpg'
            # imgName = 'DONT_DELETE_Banner_1.png'
            with open(imgName, 'wb') as f:
                f.write(imgContent)

            headers_upload = {
                "Content-Type": "multipart/form-data"
            }
            params = {
                "access_token": get_accessToken()
            }
            pic = open(imgName, 'rb')
            files = {
                "image": pic
            }

            upload_resp = requests.post(url='https://api.weixin.qq.com/cgi-bin/media/uploadimg', headers=headers_upload,
                                        params=params, files=files).json()
            imgList.append(upload_resp["url"])
            imgDeleteList.append(imgName)

    url_count = 'https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token=' + get_accessToken()
    count_json = requests.get(url=url_count).json()
    print("空间使用情况:", count_json)


    return imgList,imgDeleteList



# 发送消息
def send_msg(dateNum):
    dateNum = int(dateNum)
    # 在此时间段内发送图文消息！！
    if dateNum>=8 and dateNum <= 24:
        media_id,title = make_machine_msg_to_draft(dateNum)
        send_url = 'https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=' +get_accessToken()
        send_json = {
            "media_id":media_id
        }
        send_resp = requests.post(url=send_url,json=send_json).json()
        if send_resp['errmsg'] == 'ok':
            print("文章发送成功！")


#


if __name__ == '__main__':
    hours = int(datetime.now().strftime('%H'))
    send_msg(hours)
