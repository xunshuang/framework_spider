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
def make_machine_msg_to_draft():
    imgList, imgDeleteList = get_media_id(
        ['http://www.mengshuai.top/images/profile.jpg', 'http://www.mengshuai.top/images/profile2.jpg'])
    I = []
    for img in imgList:
        _ = f'<img src="{img}" style="height: 80%;width: 80%;margin: 10%;border-radius: 10px;-webkit-border-radius: 10px;-moz-border-radius: 10px;" />'
        I.append(_)
    content = """
<html>
	<head>
		<title>联系我们</title>
	</head>
	<body>
		<div class="container" style="width: 100%;height: 100%;position: fixed;overflow-x: hidden;overflow-y: scroll;text-align: center;background: rgba(0,0,0,0.8)">
			<div class="content" sytle="position: relative;margin-top: 5rem;width: 80%;height: auto;margin-left: 10%;margin-bottom: 10%;background: rgba(0, 0, 0, 0.6);border: 0.0625rem solid white;border-radius: 1.25rem;">
				<h1 class="title-h1" style="color: white;text-align: center;font-size: 2rem;width: 80%;margin-left: 10%;border-bottom: 2px solid white;">联系我们</h1>
				<div>
					<img src="http://mmbiz.qpic.cn/mmbiz_png/rISx4vUsIspTjB0u3Fial4FQqhkjrx8Piahs9OGDss8PUlRmk8ickUYAR5pq55ZpbNZvDhkBByzQ257xh380icZc6w/0"
					 style="max-width: 80%;height: auto;" />
					<div class="prefix" style="margin: 3.125rem;"></div>
					<div style="width: 80%;margin-left: 10%;background: whitesmoke;height: 31.25rem;">
						<div style="display: flex;">
							<div class="profile" style="width: 30%;height: 40%;">
"""+I[0]+"""
							</div>
							<div class="name" style="width: 70%;background: white;height: 40%;">
								<h3 style="width: 80%;border-bottom: 0.0625rem solid rgba(0,0,0,0.3);margin-left: 10%;text-align: center;margin-bottom: 0.625rem;padding-bottom: 0.625rem;">二手设备回收</h4>
									<p style="width: 80%;margin-left: 10%;text-align: left;margin-bottom: 0.625rem;font-weight: 600;">📞 昵称：购销设备15162448857</p>
									<p style="width: 80%;margin-left: 10%;text-align: left;margin-bottom: 0.625rem;font-weight: 600;">🗣 微信号：a8561258</p>
									<p style="width: 80%;margin-left: 10%;text-align: left;margin-bottom: 0.625rem;font-weight: 600;">🏠 地区：天津 西青</p>
							</div>

						</div>
						<div>
							<div class="details">
								<p style="text-align: left;font-weight: 800;font-size: 1.875rem;margin-bottom: 2rem;">“</p>
								<p style="font-weight: 600;font-size: 1.5rem;width: 80%;margin-left: 10%;">专业回收二手机床设备，整厂回收，数控机床，普通机床，诚信第一。</p>
								<p style="text-align: right;font-weight: 800;font-size: 1.875rem;margin-top: 2rem;">”</p>
							</div>
						</div>

					</div>


					<div class="prefix" style="margin: 3.125rem;"></div>
					<div style="width: 80%;margin-left: 10%;background: whitesmoke;height: 31.25rem;">
						<div style="display: flex;">
							<div class="profile" style="width: 30%;height: 40%;">
"""+I[1]+"""							</div>
							<div class="name" style="width: 70%;background: white;height: 40%;">
								<h3 style="width: 80%;border-bottom: 0.0625rem solid rgba(0,0,0,0.3);margin-left: 10%;text-align: center;margin-bottom: 0.625rem;padding-bottom: 0.625rem;">二手机床信息发布</h4>
									<p style="width: 80%;margin-left: 10%;text-align: left;margin-bottom: 0.625rem;font-weight: 600;">📞 昵称：三次握手四次挥手</p>
									<p style="width: 80%;margin-left: 10%;text-align: left;margin-bottom: 0.625rem;font-weight: 600;">🗣 微信号：MxyH62</p>
									<p style="width: 80%;margin-left: 10%;text-align: left;margin-bottom: 0.625rem;font-weight: 600;">🏠 地区：河北 廊坊</p>
							</div>

						</div>
						<div>
							<div class="details">
								<p style="text-align: left;font-weight: 800;font-size: 1.875rem;margin-bottom: 2rem;">“</p>
								<p style="font-weight: 600;font-size: 1.5rem;width: 80%;margin-left: 10%;">明人不说暗话，接广告！</p>
								<p style="text-align: right;font-weight: 800;font-size: 1.875rem;margin-top: 2rem;">”</p>
							</div>
						</div>

					</div>

					<div style="width: 80%;margin-left: 10%;">
						<span style="width: 100%;">
							<p class="warnings" style="text-align: center;font-size: 14px;color: red;width: 80%;margin-left: 10%;font-weight: 800;">【交易注意事项】</p>
						</span>
						<span style="width: 100%;">
							<p class="warnings" style="text-align: left;font-size: 14px;color: red;width: 80%;margin-left: 10%;font-weight: 800;">1.
								未见实物，先交定金的，风险极高！！！</p>
						</span>
						<span style="width: 100%;">
							<p class="warnings" style="text-align: left;font-size: 14px;color: red;width: 80%;margin-left: 10%;font-weight: 800;">2.
								动身看货前需先确认产品型号、设备是否还在、产权是否清晰等重要信息，以免白跑一趟；</p>
						</span>
						<span style="width: 100%;">
							<p class="warnings" style="text-align: left;font-size: 14px;color: red;width: 80%;margin-left: 10%;font-weight: 800;">3.
								价格远低于市场价请慎重购买，要深刻理解一分钱一分货的道理；</p>
						</span>
						<span style="width: 100%;">
							<p class="warnings" style="text-align: left;font-size: 14px;color: red;width: 80%;margin-left: 10%;font-weight: 800;">4.
								仔细检查设备能否正常使用</p>
						</span>
						<span style="width: 100%;">
							<p class="warnings" style="text-align: left;font-size: 14px;color: red;width: 80%;margin-left: 10%;font-weight: 800;">5.
								认真核对发票、质保证书、身份证、营业执照等信息，并拍照留存；</p>
						</span>
						<span style="width: 100%;">
							<p class="warnings" style="text-align: left;font-size: 14px;color: red;width: 80%;margin-left: 10%;font-weight: 800;">6.
								收货验货时请仔细核对，谨防调包；</p>
						</span>
						<span style="width: 100%;">
							<p class="warnings" style="text-align: left;font-size: 14px;color: red;width: 80%;margin-left: 10%;font-weight: 800;">7.
								本公众号信息来自互联网，不核实信息的真实性、有效性、也不参与交易环节；</p>
						</span>
						<div class="prefix" style="margin: 3.125rem;"></div>
					</div>

					<!-- </div> -->
				</div>
			</div>
		</div>
	</body>
</html>
  
"""

    article = {
        "title": f"商业合作",  # 标题
        "author": "寻霜",
        "digest": "诚寻商业合作，机床回收，机床信息发布，详情页内。",
        "content": content,
        "content_source_url": f'http://www.mengshuai.top/',
        "thumb_media_id": 'dwZxgP0_byDB5IVBizZ-NzpprYGGPJBHf9w4wWndB7WQa6xgF2eVFH2MBJgNqh2H',
        "need_open_comment": 0,
        "only_fans_can_comment": 0
    }

    js = json.dumps({
        "articles": [
            article
        ]
    }, ensure_ascii=False)
    url_upload = 'https://api.weixin.qq.com/cgi-bin/draft/add?access_token=' + get_accessToken()
    resp = requests.post(url=url_upload, data=js.encode('utf-8')).json()

    for delete in imgDeleteList:
        os.remove(delete)
    print('图片删除成功！')

    if resp.get('media_id'):
        print('草稿报存成功，media_id:', resp.get('media_id'))
        return resp.get('media_id')
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

    return imgList, imgDeleteList


# 发送消息
def send_msg():

        media_id  = make_machine_msg_to_draft()
        send_url = 'https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=' + get_accessToken()
        send_json = {
            "media_id": media_id
        }
        send_resp = requests.post(url=send_url, json=send_json).json()
        if send_resp['errmsg'] == 'ok':
            print("文章发送成功！")


#


if __name__ == '__main__':
    # url = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=' + get_accessToken()
    # data = {
    # "type":"image",
    # "offset":0,
    # "count":20
    # }
    # resp = requests.post(url=url,json=data).json()
    # print(resp)
    send_msg()