# -*- coding: utf-8 -*-
import scrapy
import pymysql
import redis


class RealRedisSpider(scrapy.Spider):
    name = 'real_redis'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        conn = pymysql.connect('127.0.0.1', 'lty', '00729', 'weather', 63126, charset="utf8",
                               use_unicode=True)
        cursor = conn.cursor()
        sql = """
                        select city_id from city
                """
        cursor.execute(sql)
        city_id_list = [city[0] for city in cursor.fetchall()]
        # print(city_id_list)

        r = redis.Redis(host='127.0.0.1', port=6379, password='lhf0729', db=0)
        with r.pipeline(transaction=False) as p:
            for city_id in city_id_list:
                if len(city_id) == 9:
                    p.lpush('real:start_urls', 'http://www.weather.com.cn/weather1dn/{}.shtml'.format(city_id))

                else:
                    p.lpush('real_town:start_urls',
                            'http://forecast.weather.com.cn/town/weather1dn/{}.shtml'.format(city_id))
            p.execute()
