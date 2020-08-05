# -*- coding: utf-8 -*-
from pprint import pprint

import requests
import scrapy
from scrapy_redis.spiders import RedisCrawlSpider

from real_weather.utils import weather_code, wind_speed_code, wind_direction_code
from real_weather.items import RealWeatherItem

class RealSpider(RedisCrawlSpider):
    name = 'real'
    allowed_domains = ['weather.com.cn']
    redis_key = 'real:start_urls'
    # start_urls = ['http://www.weather.com.cn/weather1dn/101200101.shtml']
    # start_urls = ['http://forecast.weather.com.cn/town/weather1dn/101200101019.shtml']

    def parse(self, response):
        item = RealWeatherItem()
        url = response.request.url.split('/')
        code = url[-1].split('.')[0]
        if len(code) == 9:
            try:
                headers = {
                    'Referer': 'http://www.weather.com.cn/weather1dn/{}.shtml'.format(code),
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                    'Content-Type': 'application/json'
                }
                url = 'http://d1.weather.com.cn/sk_2d/{}.html'.format(code)  # 实况url
                r = requests.get(url=url, headers=headers)
                data_l = r.content.decode(encoding='utf8').split('=')[1].strip('}').strip('{').split(',')[1:]
                tem_list = []
                for data in data_l:
                    if data.startswith('"temp"') or data.startswith('"WD"') or data.startswith(
                            '"WS"') or data.startswith('"SD"') \
                            or data.startswith('"time"') or data.startswith('"weather"') or data.startswith('"wse"') \
                            or data.startswith('"rain"') or data.startswith('"aqi"') or data.startswith(
                        '"aqi_pm25"') or data.startswith('"date"'):
                        tem_list.append(data)
                real_weather_dict = {}
                for t, tem in enumerate(tem_list):
                    tem = tem.split(':')
                    if t == 1:
                        real_weather_dict.update({'wind': tem[1].strip('""')})
                    elif t == 2:
                        real_weather_dict.update({'wind_num': tem[1].strip('""')})
                    elif t == 3:
                        real_weather_dict.update({'wind_num1': tem[1].strip('""')})
                    elif t == 4:
                        real_weather_dict.update({'humidity': tem[1].strip('""')})
                    elif t == 5:
                        real_weather_dict.update({'update_time': tem[1].strip('""') + ':' + tem[2].strip('""')})
                    elif t == 0:
                        real_weather_dict.update({'temp': tem[1].strip('""') + '℃'})
                    else:
                        real_weather_dict.update({tem[0].strip('""'): tem[1].strip('""')})
                real_weather_dict.update({'city_code': code})
                pprint(real_weather_dict)
                item['real_weather'] = real_weather_dict
                item['code'] = code

                yield item
            except Exception as e:
                url = 'http://www.weather.com.cn/weather1dn/{}.shtml'.format(code)
                yield scrapy.Request(url=url, callback=self.parse)
        # else:
        #     try:
        #         temp = response.xpath('//div[@class="todayLeft"]/div[3]/span[1]/text()').get()
        #         temp1 = response.xpath('//div[@class="todayLeft"]/div[3]/span[2]/text()').get()
        #         weather = response.xpath('//div[@class="todayLeft"]/div[4]/text()').get()
        #         wind = response.xpath('//div[@class="todayLeft"]/p[1]/span/text()').get()
        #         humidity = response.xpath('//div[@class="todayLeft"]/p[2]/span/text()').get()
        #         update_time = response.xpath('//div[@class="todayLeft"]/div[1]/div/span/text()').get()
        #         real_weather_dict = {'update_time': update_time, 'temp': temp + temp1, 'weather': weather, 'wind': wind, 'humidity': humidity, 'city_code': code}
        #         pprint(real_weather_dict)
        #
        #         item['real_weather'] = real_weather_dict
        #         item['code'] = code
        #
        #         yield item
        #     except Exception as e:
        #         url = 'http://forecast.weather.com.cn/town/weather1dn/{}.shtml'.format(code)
        #         yield scrapy.Request(url=url, callback=self.parse)