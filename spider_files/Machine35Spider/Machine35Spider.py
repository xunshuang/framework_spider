# coding:utf-8
import os
import sys

sys.path.append('/workspace/framework_spider/')


from Core.spider import Spider
from spider_files.Machine35Spider import Machine35SpiderSetting
from Config.SpiderData import doc
from copy import deepcopy
import re
from hashlib import md5
from datetime import datetime
from urllib.parse import urljoin

class Machine35Spider(Spider):
    spider_name = 'Machine35Spider'
    setting = Machine35SpiderSetting
    headers = {
        'Proxy-Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
        'Accept': 'text/templates,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://search.machine35.com/product.do?sortid=&typeid=&keywords=%B6%FE%CA%D6&province=&city=&show=&page=2',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    async def start_requests(self):
        for page in range(1,123):
            url_base = f"http://search.machine35.com/product.do?sortid=&typeid=&keywords=%B6%FE%CA%D6&province=&city=&show=&page={page}"
            yield self.request(method='GET', url=url_base, callback=self.parse)



    async def parse(self,response):
        div_nodes = response.xpath('//div[@id="content_li"]/div')
        for div in div_nodes:
            page_url = div.xpath('.//div[@class="entry"]/a/@href').get()
            yield self.request(method='GET',url=page_url,callback=self.get_page)


    async def get_page(self,response):
        doc_ = deepcopy(doc)
        doc_["machineSiteId"] = "A002"
        doc_["md5hash"] = md5(str(response.resp.url).encode()).hexdigest()

        doc_["machineSource"] = "傲立机床网"

        title = response.xpath('//div[@class="leftm"]/b[@class="title"]/text()').get() or ""
        doc_["machineTitleHash"] =  md5(title.encode()).hexdigest()
        doc_["machineTitle"] = title

        doc_["machineModel"] = response.xpath('//meta[@property="og:product:brand"]/@content').get() or ""

        doc_["machinePrice"] = response.xpath('//meta[@property="og:product:price"]/@content').get() or "面议"

        doc_["machineStatus"] = 99

        levelListRaw = [_ for _ in response.xpath('//li[@class="jc-left jc-gray"]/a/text()').getall()
                        if _ not in ["中国机床网","机床产品","二手机床"]]
        try:
            doc_["machineLevelOne"] = ("二手" + levelListRaw[0]) if "二手" not in levelListRaw[0] else levelListRaw[0]
        except:
            doc_["machineLevelOne"] = ""

        try:
            doc_["machineLevelTwo"] = ("二手" + levelListRaw[1]) if "二手" not in levelListRaw[1] else levelListRaw[1]
        except:
            doc_["machineLevelTwo"] = ""

        try:
            doc_["machineLevelThree"] = ("二手" + levelListRaw[2]) if "二手" not in levelListRaw[2] else levelListRaw[2]
        except:
            doc_["machineLevelThree"] = ""
        try:
            cityR = response.re('所 在 地：(.*?)</li>')[0].split(" ")[-1].strip()
        except:
            cityR = ""

        if cityR:
            LocationList = await self.CityParser.parse_city(city=cityR)

            if LocationList:
                for _ in LocationList[:1]:
                    try:
                        doc_["machineLocalClassOne"] = _[0]["cityName"]
                    except:
                        doc_["machineLocalClassOne"] = ""
                    try:
                        doc_["machineLocalClassTwo"] = _[1]["cityName"]
                    except:
                        doc_["machineLocalClassTwo"] = ""

                    try:
                        doc_["machineLocalClassThree"] = _[2]["cityName"]
                    except:
                        doc_["machineLocalClassThree"] = ""


        doc_["machineManufacture"] = None
        doc_["machineQuality"] = ""

        doc_["machineContact"] = response.xpath('//div[@class="content"]/div[@class="name"]/span/text()').get() or ""

        doc_["machineContactType"] = 1 if len(doc_["machineContact"]) <=5 else 2

        try:
            telephone = re.findall('<li class="left"> 移动电话：</li><li class="right">(\d+)&nbsp;</li>',response.respText,flags=re.S)[0]
        except:
            telephone = ""

        try:
            phone =  re.findall('<li class="left"> 电　　话：</li><li class="right">(.*?);</li>',response.respText,flags=re.S)[0]
            phone = phone.replace('&nbsp;',' ').replace('&nbsp','').strip()
        except:
            phone = ""

        if telephone:
            doc_["machineContactWay"] =  1
            doc_["machineContactInfo"] = telephone

        elif phone:
            doc_["machineContactWay"] = 2
            doc_["machineContactInfo"] = phone

        else:
            doc_["machineContactWay"] = 5
            doc_["machineContactInfo"] = ""


        doc_["machineUrl"] = str(response.resp.url)

        doc_["machineImg"] = response.xpath('//meta[@property="og:image"]/@content').get() or ""

        pub_time = response.re('<li> 有 效 期：(\d{4}年\d{2}月\d{2}日)-.*?</li>',response.respText)

        doc_["machinePublishTime"] = datetime.strptime(pub_time[0],"%Y年%m月%d日").strftime("%Y-%m-%d %H:%M:%S") if pub_time else ""

        machineInfo = "".join(response.xpath('//div[@class="detail"]//div[@class="content"]//text()').getall()).strip()

        machineInfo = machineInfo.replace('联系我时，请说是在“傲立机床网”上看到的，谢谢！','').replace("注：",'').strip()
        doc_["machineInfo"] = machineInfo.encode() if machineInfo else "暂无详细信息".encode()
        doc_["machineInsertTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield doc_

# 外部调用启动入口
def start():
    Machine35Spider.start()


if __name__ == '__main__':
    start()