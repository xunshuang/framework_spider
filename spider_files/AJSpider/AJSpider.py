# coding:utf-8
from Core.spider import Spider
import AJSpiderSetting

class AJSpider(Spider):
    spider_name = 'AJSpider'
    start_urls = ['http://www.baidu.com']
    setting = AJSpiderSetting

    async def start_requests(self):
        start_urls = ['http://www.baidu.com']
        for url in start_urls:
            yield self.request(method='GET',url=url,callback=self.parse,meta={"test":123})

    async def parse(self,response):
        text = response.respText
        resp = response.resp
        yield [{"md5hash": 3,"data":"3"},]





AJSpider.start()