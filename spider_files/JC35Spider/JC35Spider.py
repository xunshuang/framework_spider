# coding:utf-8
import os
import sys

sys.path.append('/workspace/framework_spider/')


from Core.spider import Spider
from spider_files.JC35Spider import JC35SpiderSetting
from Config.SpiderData import doc
from copy import deepcopy
import re
from hashlib import md5
from datetime import datetime
from urllib.parse import urljoin
class JC35Spider(Spider):
    spider_name = 'JC35Spider'
    setting = JC35SpiderSetting
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://used.jc35.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    async def start_requests(self):
        start_urls = ['https://used.jc35.com/chanpin-0.html']
        for url in start_urls:
            yield self.request(method='GET', url=url, callback=self.parse)

    async def parse(self, response):
        all_class = response.xpath('//div[@class="proLists"]//li//a')
        for _class in all_class:
            url = _class.xpath('.//@href').get()

            yield self.request(method='GET', url=url, callback=self.parse2)

    async def parse2(self, response):
        all_class = response.xpath('//div[@class="proLists"]//li//a')
        for _class in all_class:
            url = _class.xpath('.//@href').get()

            yield self.request(method='GET', url=url, callback=self.parse3)

    async def parse3(self, response):
        all_class = response.xpath('//div[@class="proLists"]//li//a')
        for _class in all_class:
            url = _class.xpath('.//@href').get()
            yield self.request(method='GET', url=url, callback=self.get_list)
            yield self.request(method='GET', url=url, callback=self.fetch_page_one)

    async def fetch_page_one(self, response):
        url_base = response.resp.url
        try:
            max_page = int(response.re('共(\d+)页\d+条记录')[0])
        except:
            max_page = 0

        if max_page >= 2:
            for page in range(2, int(max_page) + 1):
                url = re.sub('\.html', f'_p{page}.html', str(url_base))
                yield self.request(method='GET', url=url, callback=self.get_list)

    async def get_list(self, response):
        all_data = response.xpath('//div[@class="listMain"]//li')
        print(f"列表页 url:{response.resp.url}")

        for _ in all_data:
            url = _.xpath('./p/a[@title]/@href').get()
            meta = {
                "machinePublishTime":_.xpath('./div[@class="yprice"]/text()').get().strip()
            }
            yield self.request(method='GET', url=url, callback=self.get_pages,meta=meta)

    async def get_pages(self, response):
        doc_ = deepcopy(doc)

        try:
            print(f"详情页 url:{response.resp.url}")
            doc_["machineSiteId"] = 'A001'
            doc_["md5hash"] = md5(str(response.resp.url).encode()).hexdigest()
            doc_["machineSource"] = "JC35二手机床网"
            doc_["machineTitle"] = response.xpath('//h2[@id="txtTypeName"]/text()').get()
            doc_["machineTitleHash"] = md5(doc_["machineTitle"].encode()).hexdigest()
            machineModel= re.findall('品牌：<span>(.*?)</span>', response.respText, flags=re.S) #

            doc_["machineModel"] = machineModel[0] if  machineModel else ""


            machineStatus = re.findall('状态：<span>(.*?)</span>', response.respText, flags=re.S)
            if machineStatus:
                doc_["machineStatus"] = {
                    "展示中":2,
                    "已出售":1,
                    "":99
                }[machineStatus[0]]
            else:
                doc_["machineStatus"] = 99

            doc_["machineLevelOne"] = response.xpath('//div[@class="location"]/a[2]/text()').get() #
            doc_["machineLevelTwo"] = response.xpath('//div[@class="location"]/a[3]/text()').get() #
            doc_["machineLevelThree"] = response.xpath('//div[@class="location"]/a[4]/text()').get()#

            Location = re.findall('所在地：<span>(.*?)</span>', response.respText, flags=re.S)

            if Location and Location[0] != "国外":
                LocationList = await self.CityParser.parse_city(city=Location[0])

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
            else:
                doc_["machineLocalClassOne"] = "国外"
                doc_["machineLocalClassTwo"] = ""
                doc_["machineLocalClassThree"] = ""
            machineManufacture = re.findall('出厂年份：<span>(.*?)</span>', response.respText, flags=re.S)
            doc_["machineManufacture"] = machineManufacture[0] +'-01-01 00:00:00' if machineManufacture else None

            machineQuality = re.findall('产品成色：<span>(.*?)</span>', response.respText, flags=re.S)
            doc_["machineQuality"] = machineQuality[0] if machineQuality else ""

            machineContact = re.findall('联系人：(.*?)<span>', response.xpath('//div[@class="contact"]/p//text()').get(), flags=re.S)
            doc_["machineContact"] = machineContact[0] if machineContact else ""

            if doc_["machineContact"]:
                doc_["machineContactType"] = 1 if len(doc_["machineContact"]) <=5 else 2
            else:
                doc_["machineContactType"] = 3

            machineContactInfo = re.findall('联系.*?：(.*)', "".join(response.xpath('//div[@class="contact"]/p//text()').getall()), flags=re.S)

            doc_["machineContactInfo"] = machineContactInfo[0] if machineContactInfo else ""

            doc_["machineContactWay"] = 5
            doc_["machineUrl"] = str(response.resp.url)


            doc_["machineImg"] = "$$$".join([ urljoin(str(response.resp.url),_) for _ in response.xpath('//ul[@id="bigPig"]/li/a/@href').getall()])

            doc_["machinePublishTime"] = datetime.strptime(response.meta["machinePublishTime"],"%Y.%m.%d").strftime("%Y-%m-%d %H:%M:%S")

            doc_["machineInfo"] = "\n".join(response.xpath('//div[@class="infoBot"]/p//text() | //div[@class="infoBot"]//text()').getall()).strip()
            doc_["machineInsertTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(doc_["machineTitle"])
            yield doc_
        except:
            print("错误！")
            yield doc_

# 外部调用启动入口
def start():
    JC35Spider.start()


if __name__ == '__main__':
    start()