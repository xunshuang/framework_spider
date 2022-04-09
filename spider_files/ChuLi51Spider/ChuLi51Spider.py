# coding:utf-8
import os
import sys

sys.path.append('/workspace/framework_spider/')

from Core.spider import Spider
from spider_files.ChuLi51Spider import ChuLi51SpiderSetting
from Config.SpiderData import doc
from copy import deepcopy
import re
from hashlib import md5
from datetime import datetime
from urllib.parse import urljoin
from PIL import Image
import pytesseract
import aiohttp
import io


class ChuLi51Spider(Spider):
    spider_name = 'ChuLi51Spider'
    setting = ChuLi51SpiderSetting
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    verify = True

    async def start_requests(self):
        url_base = "https://www.51chuli.com/category/"
        yield self.request(method='GET', url=url_base, callback=self.parse)

    async def parse(self, response):
        sections = response.xpath('//div[@class="catemain"]')
        for section in sections:
            if section.xpath('./div[@class="bigt"]/h3/text()').get() == '机床':
                tableList = section.xpath('./table')
                tableNameList = section.xpath('./div[@class="groupt"]/p/text()').getall()
                for table in tableList:
                    tableName = tableNameList[tableList.index(table)]
                    tableUrl = table.xpath('.//a')
                    for _ in tableUrl:
                        url = _.xpath('./@href').get()
                        urlName = _.xpath('./text()').get()
                        meta = {
                            "page":1,
                            "url":url,
                            "levelOne":tableName,
                            "levelTwo":urlName
                        }
                        yield self.request(method='GET', url=url, callback=self.get_list, meta=meta)


    async def get_list(self, response):
        if response.meta["page"] > 1 and response.meta["page"] <= 10:
            page = response.meta['page']
            urlList = response.xpath('//div[@class="projects-dls"]/dl//h5//span/a/@href').getall()

            for url in urlList:
                yield self.request(method='GET', url=url, callback=self.get_page,meta=response.meta)

            next_page = response.xpath('//a[@class="next"]/@href').get()

            if next_page:
                next_page = urljoin(str(response.resp.url), next_page)
                yield self.request(method='GET', url=next_page, callback=self.get_list, meta={
                    "page": page + 1,
                    "url": next_page,
                    "levelOne": response.meta["levelOne"],
                    "levelTwo": response.meta["levelTwo"]
                })

        elif response.meta['page'] == 1:
            urlList = response.xpath('//div[@class="projects-dls"]/dl//h5//span/a/@href').getall()

            for url in urlList:
                yield self.request(method='GET', url=url, callback=self.get_page,meta=response.meta)

            next_page = response.xpath('//a[@class="next"]/@href').get()

            if next_page:
                next_page = urljoin(str(response.resp.url), next_page)
                yield self.request(method='GET', url=next_page, callback=self.get_list, meta={
                    "page": 2,
                    "url": next_page,
                    "levelOne": response.meta["levelOne"],
                    "levelTwo": response.meta["levelTwo"]
                })



    async def get_page(self, response):
        doc_ = deepcopy(doc)
        doc_["machineSiteId"] = "A003"
        doc_["md5hash"] = md5(str(response.resp.url).encode()).hexdigest()

        doc_["machineSource"] = "处理网"

        title = "".join(response.xpath('//div[@class="d-ltop"]/h1//text()').getall()) or ""

        if "该信息已过期" not in title:
            doc_["machineTitleHash"] = md5(title.encode()).hexdigest()
            doc_["machineTitle"] = title
            print(response.meta,title)
            doc_["machineModel"] = ""

            doc_["machinePrice"] = response.xpath('//p[@class="pricep"]/span/b/text()').get() or "面议"

            doc_["machineStatus"] = 99


            doc_["machineLevelOne"] = response.meta["levelOne"]

            doc_["machineLevelTwo"] = response.meta["levelTwo"]
            doc_["machineLevelThree"] = ""

            try:
                cityR = response.xpath('//p[@class="addressp"]/span[1]/a/text()').getall()[-1] or ""
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

            machineQuality = response.re("成色：<label>(.*?)</label>", response.respText)
            doc_["machineQuality"] = machineQuality[0] if machineQuality else ""

            doc_["machineContact"] = response.xpath('//p[@class="contactman"]/span/text()').get() or ""

            doc_["machineContactType"] = 1 if len(doc_["machineContact"]) <= 5 else 2

            try:

                telephoneImg = response.xpath('//p[@class="phonetab"]/img/@src').get()
                if telephoneImg:
                    async with aiohttp.request(method='GET', url=telephoneImg) as resp:
                        imgContent = await resp.read()
                        imgSteam = Image.open(io.BytesIO(imgContent))
                        imgSteam = imgSteam.convert('L')  # 灰度化
                        telephone = pytesseract.image_to_string(imgSteam, lang="eng", config="--psm 7").strip()  # 识别
                        if not len(telephone) == 11:
                            raise Exception("位数识别错误")

                        if not telephone.startswith('1'):
                            raise Exception("号码识别错误")
                else:
                    telephone = response.xpath('//p[@class="phonetab"]/b/text()').get() or ""
            except:
                telephone = ""

            try:
                qq = response.xpath('//p[@class="qqnum"]/a/text()').get() or ""
            except:
                qq = ""

            if telephone:
                doc_["machineContactWay"] = 1
                doc_["machineContactInfo"] = telephone

            elif qq:
                doc_["machineContactWay"] = 4
                doc_["machineContactInfo"] = qq

            else:
                doc_["machineContactWay"] = 5
                doc_["machineContactInfo"] = ""

            doc_["machineUrl"] = str(response.resp.url)

            doc_["machineImg"] = "$$$".join(response.xpath('//div[@id="img_ul2"]//li//img/@src').getall()) or ""

            pub_time = response.re('发布：<label>(20\d+-\d+-\d+ \d+:\d+)</label>', response.respText)

            doc_["machinePublishTime"] = datetime.strptime(pub_time[0], "%Y-%m-%d %H:%M").strftime(
                "%Y-%m-%d %H:%M:%S") if pub_time else ""

            machineInfo = "\n".join(response.xpath('//div[@class="containbox3"]/p//text()').getall()).strip()

            machineInfo = machineInfo.replace('\n此贴长期有效，联系我时，请说明是从处理网看到的。', '。').strip()
            doc_["machineInfo"] = machineInfo.encode() if machineInfo else "暂无详细信息".encode()
            doc_["machineInsertTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if doc_['machineContactInfo']:
                yield doc_


# 外部调用启动入口
def start():
    ChuLi51Spider.start()


if __name__ == '__main__':
    start()
