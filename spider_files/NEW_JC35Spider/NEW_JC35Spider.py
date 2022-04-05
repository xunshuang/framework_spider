# coding:utf-8
import os
import sys

sys.path.append('/workspace/framework_spider/')


from Core.spider import Spider
from spider_files.NEW_JC35Spider import NEW_JC35SpiderSetting
from Config.SpiderNews import doc
from copy import deepcopy
import re
from hashlib import md5
from datetime import datetime
from urllib.parse import urljoin
class NEW_JC35Spider(Spider):
    spider_name = 'NEW_JC35Spider'
    setting = NEW_JC35SpiderSetting
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
        'Accept': 'text/templates,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://used.jc35.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    async def start_requests(self):
        start_urls = [
            'https://www.jc35.com/news/t3972/list.html', # 名企在线
            'https://www.jc35.com/news/t3923/list.html', # 市场分析
            'https://www.jc35.com/news/t9/list.html', # 国内新闻
            'https://www.jc35.com/news/t3983/list.html', # 地区风采
            'https://www.jc35.com/news/t4077/list.html', # 机床会议
            'https://www.jc35.com/news/t3984/list.html', # 展会快报
            'https://www.jc35.com/news/t13/list.html', # 科技动态
        ]
        for url in start_urls:
            yield self.request(method='GET', url=url, callback=self.parse)

    async def parse(self, response):
        all_url = response.xpath('//div[@class="mainLeftList"]//a/@href').getall()
        for _ in all_url:
            url = urljoin(str(response.resp.url),_)
            yield self.request(method='GET', url=url, callback=self.get_pages)



    async def get_pages(self, response):
        doc_ = deepcopy(doc)

        try:
            doc_["machineSiteId"] = 'A004'
            doc_["md5hash"] = md5(str(response.resp.url).encode()).hexdigest()
            doc_["machineSource"] = "JC35二手机床网"
            doc_["machineTitle"] = response.xpath('//div[@class="newsShow"]/h1/text()').get()
            doc_["machineTitleHash"] = md5(doc_["machineTitle"].encode()).hexdigest()
            print(f"详情页 {doc_['machineTitle'] },url:{response.resp.url}")

            doc_["machineAuthor"] = '站点小工(机器人)'
            doc_["machineImg"] = response.xpath('//meta[@property="og:image"]/@content').get() or ""
            doc_["machineKeywords"] = response.xpath('//meta[@name="Keywords"]/@content').get() or ""

            doc_["machineDescription"] = response.xpath('//meta[@property="og:description"]/@content').get() or ""

            ContentSections = response.xpath('//div[@class="newsContent"]/div')

            for section in ContentSections:
                doc_["machineContent"] += "".join(section.xpath('.//text()').getall()).replace('\xa0','').replace('\u3000',' ') + '\n'

            doc_["machineContent"] = doc_["machineContent"].strip().encode()

            machinePublishTime = response.xpath('//meta[@property="og:release_date"]/@content').get() or ""
            doc_["machinePublishTime"] = datetime.strptime(
                machinePublishTime,'%Y/%m/%d %H:%M:%S'
            ).strftime("%Y-%m-%d %H:%M:%S") if machinePublishTime else ""

            doc_["machineInsertTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            yield doc_
        except:
            print("错误！")
            yield doc_

# 外部调用启动入口
def start():
    NEW_JC35Spider.start()


if __name__ == '__main__':
    start()