# coding:utf-8
from Config.GlobalSetting import MYSQL_CONFIG
from Db.MySQLClient.client import create_new_mysql
import json

class MachineMap():
    def __init__(self):
        self.mysql, self.cursor = create_new_mysql(CONFIG=MYSQL_CONFIG)

    def init_spider_name(self, spiderSiteId):
        self.spiderSiteId = spiderSiteId

    def make_machine_map(self):
        SQL = 'SELECT DISTINCT ' \
              '`machineLevelOne`,`machineLevelTwo`,`machineLevelThree` ' \
              'FROM `machineData` ' \
              'WHERE `machineSiteId` = "%s";' % (self.spiderSiteId)

        self.cursor.execute(SQL)
        self.mysql.commit()

        machineMapListRaw = self.cursor.fetchall()
        machineListRaw = []
        for _ in self.split_machine_map_list(machineMapListRaw):
            machineListRaw += [_]
        machineList = json.dumps(machineListRaw,ensure_ascii=False)
        try:
            SQL2 = 'INSERT INTO `machineMap`(`machineSiteId`,`machineJson`) VALUES (%s,%s);'
            try:
                self.cursor.execute(SQL2,(self.spiderSiteId,machineList))
                self.mysql.commit()
            except:
                self.mysql.rollback()
                raise Exception("rollback")
        except:
            SQL2 = 'UPDATE `machineMap` SET `machineJson` = %s WHERE `machineSiteId` = %s'
            try:
                self.cursor.execute(SQL2,(machineList,self.spiderSiteId))
                self.mysql.commit()
            except:
                self.mysql.rollback()
    def split_machine_map_list(self, machineMapListRaw):
        for _1 in list(set([_['machineLevelOne'] for _ in machineMapListRaw])):
            one = _1 or "其他"
            doc1 = {
                "levelName":one,
                "child":[]
            }
            for _2 in machineMapListRaw:
                if _2["machineLevelOne"] == one or  _2["machineLevelOne"] == "":
                    two = _2["machineLevelTwo"] or "其他"
                    doc2 = {
                        "levelName":two,
                        "child":[]
                    }
                    for _3 in  machineMapListRaw:
                        if _3['machineLevelOne'] == one or _3['machineLevelOne'] == "":
                            if _3['machineLevelTwo'] == two or _3['machineLevelTwo'] == "":
                                three = _3['machineLevelThree'] or "其他"
                                doc3 = {
                                    "levelName": three,
                                    "child": []
                                }
                                doc2['child'].append(doc3)
                    doc1['child'].append(doc2)
            yield doc1




if __name__ == '__main__':
    a = MachineMap()
    a.init_spider_name('A003')
    a.make_machine_map()
