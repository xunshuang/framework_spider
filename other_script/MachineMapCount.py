# coding:utf-8
# 在每次爬虫结束后 统计Map 每个小支类的数据数量

from Config.GlobalSetting import MYSQL_CONFIG
from Db.MySQLClient.client import MYSQL
import json


class MachineMapCount():
    def __init__(self):
        self.mysqlObj = MYSQL(CONFIG=MYSQL_CONFIG, db='machinedb')
        self.mysql, self.cursor = self.mysqlObj.get_mysql()

    def init_spider_name(self, spiderSiteId):
        self.spiderSiteId = spiderSiteId

    # 读取全字典
    def read_machine_map(self):
        SQL = 'SELECT `machineJson` FROM `machineMap` WHERE `machineSiteId` = %s'
        self.cursor.execute(SQL,self.spiderSiteId)
        self.mysql.commit()

        machineMapListRaw = self.cursor.fetchone()['machineJson']
        machineMapListRaw = machineMapListRaw.replace("全部",'').replace("其他",'').replace("其它",'')
        machineMapList = json.loads(machineMapListRaw)
        levels = self.join_machine_list(machineMapList)
        for level in levels:
            levelList = level.split('$$$')
            while len(levelList) < 3:
                levelList.append("")
            self.count_map(levelList)

    # 拼接字典
    def join_machine_list(self,machineMapList):
        for lis in machineMapList:
            if lis['child']:
                gens = self.join_machine_list(machineMapList=lis['child'])
                for _ in gens:
                    yield lis["levelName"] + '$$$' + _
            else:
                yield lis["levelName"]

    # 查询字典下数据量
    def search_map_count(self,levelList):
        SQL_LIST= [
            'AND `machineLevelOne` = %s ','AND `machineLevelTwo` = %s ','AND `machineLevelThree` = %s '
        ]
        ARGS_ = len(levelList) - levelList.count('')
        print(ARGS_)
        SQL_SEARCH = 'SELECT COUNT(`id`) FROM `machineData` ' \
                     'WHERE `machineSiteId` = %s ' + "".join(SQL_LIST[0:ARGS_])

        self.cursor.execute(SQL_SEARCH, [self.spiderSiteId] + levelList[0:ARGS_])
        self.mysql.commit()
        count = self.cursor.fetchone()['COUNT(`id`)']
        return count

    def count_map(self,levelList):
        count = self.search_map_count(levelList)

        SQL_SEARCH = 'SELECT `id` FROM `machineMapCount` ' \
                     'WHERE `machineSiteId` = %s AND ' \
                     '`machineLevelOne` = %s AND ' \
                     '`machineLevelTwo` = %s AND ' \
                     '`machineLevelThree` = %s '


        self.cursor.execute(SQL_SEARCH,[self.spiderSiteId] + levelList)
        self.mysql.commit()

        if self.cursor.fetchone():
            SQL_UPDATE = 'UPDATE `machineMapCount` ' \
                         'SET `machineCount` =  %s ' \
                         'WHERE `machineSiteId` = %s AND ' \
                         '`machineLevelOne` = %s AND ' \
                         '`machineLevelTwo` = %s AND ' \
                         '`machineLevelThree` = %s '

            self.cursor.execute(SQL_UPDATE,[count,self.spiderSiteId] + levelList)
            self.mysql.commit()
        else:
            SQL_INSERT = 'INSERT INTO `machineMapCount`(' \
                         '`machineSiteId`,`machineCount`,`machineLevelOne`,`machineLevelTwo`,`machineLevelThree`) ' \
                         'VALUES (%s,%s,%s,%s,%s)'

            self.cursor.execute(SQL_INSERT, [self.spiderSiteId,count] + levelList)
            self.mysql.commit()


if __name__ == '__main__':
    x = MachineMapCount()
    x.init_spider_name('A002')
    x.read_machine_map()