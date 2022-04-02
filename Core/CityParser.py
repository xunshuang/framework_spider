# coding:utf-8
from Db.MySQLClient.client import MYSQL
from Config import GlobalSetting
import asyncio

class CityParser():
    def __init__(self):
        self.mysqlObject = MYSQL(CONFIG=GlobalSetting.MYSQL_CONFIG,db='machinedb')
        self.mysql,self.cursor = self.mysqlObject.get_mysql()



    async def parse_city_gen(self,city,cityCode=None,deep=0):
        self.mysql,self.cursor = self.mysqlObject.get_mysql()
        if not cityCode:
            SQL_SEARCH = 'SELECT `cityParentName`,`cityParentCode`,`cityName` FROM `machineCity` WHERE `cityName` LIKE "%s"' %("%" + city + "%")
        else:
            SQL_SEARCH = 'SELECT `cityParentName`,`cityParentCode`,`cityName` FROM `machineCity` WHERE `cityCode` LIKE "%s"' %("%" + cityCode + "%")

        self.cursor.execute(
            SQL_SEARCH
        )
        self.mysql.commit()
        city_searches = self.cursor.fetchall()
        if city_searches:
            for city_search in city_searches:
                if city_search["cityParentName"]:
                    yield {
                        "cityName": city_search['cityName'],
                        "deep": deep

                    }
                    async for _ in self.parse_city_gen(city=city_search["cityParentName"],cityCode=city_search["cityParentCode"],deep=deep+1):
                        try:
                            if _['cityName'] != '中华人民共和国民政部':
                                yield _
                        except:
                            pass
                else:
                    yield {
                        "cityName":city_search['cityName'],
                        "deep":deep

                    }
                yield {"cityName":"$$$","deep":deep}


    async def parse_city(self,city):
        async_gen = self.parse_city_gen(city=city)
        cityListAll = []
        cityList = []
        async for city_msg in async_gen:
            if city_msg["cityName"] == '$$$':
                cityList.sort(key=lambda x: x['deep'], reverse=True)
                cityListAll.append(cityList)
                cityList = []
            else:
                cityList.append(
                    city_msg
                )
        result = []
        for _ in cityListAll:
            if _:
                result.append(_)
        return [ _ for _ in cityListAll if _]


if __name__ == '__main__':
    x = CityParser()
    print(asyncio.run(x.parse_city(city="铜陵市")))
