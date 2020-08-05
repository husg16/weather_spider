# -*- coding: utf-8 -*-
import pymysql
import redis
import scrapy


class HistoryRedisSpider(scrapy.Spider):
    name = 'history_redis'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        conn = pymysql.connect('127.0.0.1', 'jgh', '00000929', 'weather', 63126, charset="utf8",
                               use_unicode=True)
        cursor = conn.cursor()
        sql = """
                        select city_id from city
                """
        cursor.execute(sql)
        city_id_list = [city[0] for city in cursor.fetchall()]
        r = redis.Redis(host='127.0.0.1', port=6379, password='gf005r9', db=0)
        with r.pipeline(transaction=False) as p:
            for city_id in city_id_list:
                if len(city_id) == 9:
                    p.lpush('weather_history:start_urls',
                            'http://www.weather.com.cn/weather40dn/{}.shtml'.format(city_id))
            p.execute()