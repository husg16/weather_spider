# -*- coding: utf-8 -*-
import json
import time
from pprint import pprint
import requests
import scrapy
from scrapy_redis.spiders import RedisCrawlSpider

from weather_day40.items import WeatherDay40Item


class HistorySpider(RedisCrawlSpider):
    name = 'history'
    allowed_domains = ['weather.com.cn']
    redis_key = 'weather_history:start_urls'

    def parse(self, response):
        try:
            url = response.request.url
            code = url.split('/').pop().split('.')[0]
            today = int(time.strftime("%Y", time.localtime()))
            year_list = [today - 2, today - 1, today, today + 1]
            for x in year_list:
                for j in range(1, 13):
                    headers = {
                        'Referer': 'http://www.weather.com.cn/weather40dn/{}.shtml'.format(code),
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                        'Content-Type': 'application/json'
                    }
                    j = str(j)
                    if len(j) == 1:
                        j = '0' + j
                    url = 'http://d1.weather.com.cn/calendarFromMon/{}/{}_{}.html'.format(x, code, str(x) + j)
                    # url = 'http://d1.weather.com.cn/calendarFromMon/2021/101200101_202101.html'
                    r = requests.get(url=url, headers=headers)
                    data = r.content.decode(encoding='utf8')
                    data = json.dumps(data)
                    data = json.loads(data, encoding='utf-8')
                    data_list = data.strip('var fc40 = ').strip('[').strip('"').strip(']').split('},{')

                    weather40day_history = []
                    for i, data in enumerate(data_list):
                        datas = data.strip('{').split(',')
                        temp = []
                        for data in datas:
                            if data.startswith('"alins"') or data.startswith('"als"') or data.startswith(
                                    '"date"') or data.startswith(
                                '"hgl"') or data.startswith('"hmax"') or data.startswith('"hmin"') \
                                    or data.startswith('"nl"') or data.startswith('"nlyf"'):
                                temp.append(data)
                        temp_dict = {}
                        for w, weather in enumerate(temp):
                            temp_data = weather.split(':')
                            if w == 5:
                                temp_dict.update({'temp_l': temp_data[1].strip('""') + '℃'})
                            elif w == 2:
                                temp_dict.update({temp_data[0].strip('""'): temp_data[1].strip('""')})
                            elif w == 3:
                                temp_dict.update({'humidity': temp_data[1].strip('""')})
                            elif w == 4:
                                temp_dict.update({'temp_h': temp_data[1].strip('""') + '℃'})
                            elif w == 0:
                                temp_dict.update({temp_data[0].strip('""'): temp_data[1].strip('""')})
                            elif w == 1:
                                temp_dict.update({temp_data[0].strip('""'): temp_data[1].strip('""')})
                            elif w == 6:
                                temp_dict.update({'nl': temp_data[1].strip('""')})
                            elif w == 7:
                                temp_dict.update({'nlyf': temp_data[1].strip('""')})
                        weather40day_history.append(temp_dict)
                    weather40day_history.append(str(x) + j)
                    pprint(weather40day_history)
                    item = WeatherDay40Item()
                    item['weather_day40_history'] = weather40day_history
                    item['code'] = code
                    yield item
        except Exception as e:
            print('40天天气数据获取失败%s' % e)
            url = 'http://www.weather.com.cn/weather40dn/{}.shtml'.format(code)
            yield scrapy.Request(url=url, callback=self.parse)