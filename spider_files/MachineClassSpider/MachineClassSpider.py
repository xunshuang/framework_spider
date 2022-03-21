# coding:utf-8
import os
import sys
sys.path.append('/workspace/framework_spider/')

from Core.spider import Spider
import MachineClassSpiderSetting

class AJSpider(Spider):
    spider_name = 'MachineClassSpider'
    setting = MachineClassSpiderSetting
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://used.jc35.com/chanpin-4513.html',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    async def start_requests(self):
        start_urls = ['https://used.jc35.com/']
        for url in start_urls:
            yield self.request(method='GET',url=url,callback=self.get_class_1)

    async def get_class_1(self,response):
        classesOne = response.xpath('//div[@class="subTitle"]/h3/a')

        for classOne in classesOne:
            classOneTitle = classOne.xpath('.//text()').get()
            classOneUrl = classOne.xpath('./@href').get()

            meta = {
                "classOneTitle":classOneTitle
            }
            yield self.request(method='GET',url=classOneUrl,callback=self.get_class_2,meta=meta)

    async def get_class_2(self,response):
        meta = response.meta
        classesTwo = response.xpath('//div[@class="find"]/div[1]//ul[@class="otherexi"]/li/a')
        for classTwo in classesTwo:
            classTwoTitle = classTwo.xpath('.//text()').get()
            classTwoUrl = classTwo.xpath('./@href').get()
            yield self.request(method='GET',url=classTwoUrl,callback=self.get_class_3,meta={
                "classOneTitle":meta["classOneTitle"],
                "classTwoTitle":classTwoTitle
            })


    async def get_class_3(self,response):
        meta = response.meta.copy()
        classesThree = response.xpath('//div[@class="proLists"]/ul/li/a')
        for classThree in classesThree:
            classThreeTitle = classThree.xpath('.//text()').get()
            classThreeUrl = classThree.xpath('.//@href').get()

            print({
                "classOneTitle":meta["classOneTitle"],
                "classTwoTitle":meta['classTwoTitle'],
                "classThreeTitle":classThreeTitle
            })
            yield {
                "classOneTitle":meta["classOneTitle"],
                "classTwoTitle":meta['classTwoTitle'],
                "classThreeTitle":classThreeTitle
            }


AJSpider.start()