# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql


class SafetyinformationPipeline:
    def process_item(self, item, spider):
        return item


class MysqlPipeline:
    def __init__(self, host, port, user, password, database, table):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.table = table

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            port=crawler.settings.get('MYSQL_PORT'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            table=crawler.settings.get('MYSQL_TABLE'),
        )

    def open_spider(self, spider):
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password, charset='utf8')
        cur = conn.cursor()
        cur.execute('create database if not exists {} charset UTF8MB4'.format(self.database))
        cur.close()
        conn.close()
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(["%s"] * len(data))
        sql_insert = 'insert into %s (%s) values (%s)' % (self.table, keys, values)
        sql_query = "select * from {} where title = '{}'".format(
            self.table,
            pymysql.escape_string(item['title']),
        )
        sql_create_table = """create table if not exists {} ({}, {}, {}, {}, {}, {}, {}, {})""".format(
            self.table,
            'id int(11) AUTO_INCREMENT primary key',
            'author varchar(50)',
            'type varchar(50)',
            'title varchar(255)',
            'date varchar(100)',
            'source varchar(255)',
            'link varchar(255)',
            'intro text',
        )
        try:
            if self.cursor.execute(sql_create_table):
                self.db.commit()
        except Exception as e:
            print(f'table exist: {e}')
        try:
            self.cursor.execute(sql_query)
            result = self.cursor.fetchall()
        except Exception as e:
            print(f'sql query error: {e}')
            result = ""
        if not result:
            self.cursor.execute(sql_insert, tuple(data.values()))
            self.db.commit()
        return item

    def close_spider(self, spider):
        self.db.close()
