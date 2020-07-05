# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymysql

dbInfo = {
    'host' : 'localhost',
    'port' : 3306,
    'user' : 'root',
    'password' : '',
    'db' : 'scrapys'
}

class ScrapysPipeline:
    def __init__(self):
        try :
            self.conn =  pymysql.connect(
                host = dbInfo['host'],
                port = dbInfo['port'],
                user = dbInfo['user'],
                password = dbInfo['password'],
                db = dbInfo['db']
            )
        except Exception as e:
            print("----未能正常连接数据库----")
            self.conn = None

    def process_item(self, item, spider):
        time = item['time']
        name = item['name']
        type = item['type']
        output = f'{time},{name},{type}\r\n'
        with open('./maoyanmovie.csv', 'a+', encoding='utf-8') as article:
            article.write(output)
        if self.conn != None :
            self.commitmysql(self,item)

        return item

    def commitmysql(self , item ):
        try:
            sql = "INSERT INTO scrapys_maoyan (name.type,time) VALUES (%s,%s,%s)"
            self.conn.execute(sql,item)
        except Exception as e :
            creatTable = "CREATE TABLE scrapys_maoyan (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL DEFAULT '', type VARCHAR(255) NOT NULL DEFAULT '', time VARCHAR(255)  NOT NULL DEFAULT '')"
            self.conn.execute(creatTable)
            sql = "INSERT INTO scrapys_maoyan (name.type,time) VALUES (%s,%s,%s)"
            self.conn.execute(sql, item)


