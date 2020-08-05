# -*- coding: utf-8 -*-
import scrapy
import pymysql
import redis


class RedisSpider(scrapy.Spider):
    name = 'redis'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        conn = pymysql.connect('192.168.2.101', 'lty', 'lty@100729', 'weather', 63126, charset="utf8",
                               use_unicode=True)
        cursor = conn.cursor()
        sql = """
                select city_id from city
        """
        cursor.execute(sql)
        city_id_list = [city[0] for city in cursor.fetchall()]
        # print(city_id_list)

        r = redis.Redis(host='192.168.2.101', port=6379, password='lty@100729', db=0)
        with r.pipeline(transaction=False) as p:
            for city_id in city_id_list:
                if len(city_id) == 9:
                    p.lpush('real_weather:start_urls', 'http://www.weather.com.cn/weather1dn/{}.shtml'.format(city_id))
                    p.lpush('weather_day7:start_urls', 'http://www.weather.com.cn/weathern/{}.shtml'.format(city_id))
                    p.lpush('weather_day15:start_urls', 'http://www.weather.com.cn/weather15dn/{}.shtml'.format(city_id))
                    p.lpush('weather_day40:start_urls', 'http://www.weather.com.cn/weather40dn/{}.shtml'.format(city_id))
                else:
                    p.lpush('real_weather_town:start_urls', 'http://forecast.weather.com.cn/town/weather1dn/{}.shtml'.format(city_id))
                    p.lpush('weather_day7town:start_urls', 'http://forecast.weather.com.cn/town/weathern/{}.shtml'.format(city_id))
                    p.lpush('weather_day15town:start_urls', 'http://forecast.weather.com.cn/town/weather15dn/{}.shtml'.format(city_id))
            p.execute()
