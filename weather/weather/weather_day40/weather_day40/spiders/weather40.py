# -*- coding: utf-8 -*-
import json
import time
from pprint import pprint
import requests
import scrapy
from scrapy_redis.spiders import RedisCrawlSpider

from weather_day40.items import WeatherDay40Item


class Weather40Spider(RedisCrawlSpider):
    name = 'weather40'
    allowed_domains = ['weather.com.cn']
    redis_key = 'weather_day40:start_urls'

    def parse(self, response):
        url = response.request.url.split('.com.cn')
        code = url[1].split('.')[0][-9:]
        city_name = response.xpath('//div[@class="weather_location"]/div[3]/a/text()').get()
        try:
            today = time.strftime("%Y%m", time.localtime())
            headers = {
                'Referer': 'http://www.weather.com.cn/weather40dn/{}.shtml'.format(code),
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                'Content-Type': 'application/json'
            }
            url = 'http://d1.weather.com.cn/calendarFromMon/2020/{}_{}.html'.format(code, today)
            r = requests.get(url=url, headers=headers)
            data = r.content.decode(encoding='utf8')
            data = json.dumps(data)
            data = json.loads(data, encoding='utf-8')
            data_list = data.strip('var fc40 = ').strip('[').strip('"').strip(']').split('},{')

            # 获取当天日期所以列表位置
            dates = []
            today = time.strftime("%Y%m%d", time.localtime())
            for i, data in enumerate(data_list):
                date = data.strip('{').split(',')
                for d in date:
                    if d.startswith('"date"'):
                        d = d.split(':')[1].strip('""')
                        dates.append(d)
            for da_i, da in enumerate(dates):
                if today == da:
                    j = da_i  # 当天日期所以列表位置

            weather40day = []
            for i, data in enumerate(data_list):
                datas = data.strip('{').split(',')
                temp_list = []
                for data in datas:
                    if data.startswith('"alins"') or data.startswith('"als"') or data.startswith(
                            '"date"') or data.startswith(
                            '"hgl"') or data.startswith('"hmax"') or data.startswith('"hmin"') or data.startswith(
                        '"maxobs"') or data.startswith('"minobs"') or data.startswith('"w1"') or data.startswith(
                        '"wd1"') or data.startswith('"rainobs"') or data.startswith('"max"') or data.startswith(
                        '"min"') or data.startswith('"nl"') or data.startswith('"nlyf"'):
                        temp_list.append(data)
                if i <= j - 6:
                    temp_dict = {}
                    for w, weather in enumerate(temp_list):
                        temp_data = weather.split(':')
                        if w == 5:
                            temp_dict.update({'temp_l': temp_data[1].strip('""') + '℃'})
                        elif w == 2:
                            temp_dict.update({temp_data[0].strip('""'): temp_data[1].strip('""')})
                        elif w == 3:
                            temp_dict.update({'humidity': temp_data[1].strip('""')})
                        elif w == 4:
                            temp_dict.update({'temp_h': temp_data[1].strip('""') + '℃'})
                        elif w == 13:
                            temp_dict.update({'rain': temp_data[1].strip('""') + 'mm'})
                        elif w == 0:
                            temp_dict.update({temp_data[0].strip('""'): temp_data[1].strip('""')})
                        elif w == 1:
                            temp_dict.update({temp_data[0].strip('""'): temp_data[1].strip('""')})
                        elif w == 10:
                            temp_dict.update({'nl': temp_data[1].strip('""')})
                        elif w == 11:
                            temp_dict.update({'nlyf': temp_data[1].strip('""')})
                    weather40day.append(temp_dict)
                    # print(temp_dict)
                elif j - 5 <= i <= j - 1:
                    temp_dict = {}
                    for w, weather in enumerate(temp_list):
                        temp_data = weather.split(':')
                        # print(temp_data)
                        if w == 9:
                            temp_dict.update({'temp_l': temp_data[1].strip('""') + '℃'})
                        elif w == 2:
                            temp_dict.update({temp_data[0].strip('""'): temp_data[1].strip('""')})
                        elif w == 3:
                            temp_dict.update({'humidity': temp_data[1].strip('""')})
                        elif w == 7:
                            temp_dict.update({'temp_h': temp_data[1].strip('""') + '℃'})
                        elif w == 12:
                            temp_dict.update({'rain': temp_data[1].strip('""') + 'mm'})
                        elif w == 0:
                            temp_dict.update({temp_data[0].strip('""'): temp_data[1].strip('""')})
                        elif w == 1:
                            temp_dict.update({temp_data[0].strip('""'): temp_data[1].strip('""')})
                        elif w == 10:
                            temp_dict.update({'nl': temp_data[1].strip('""')})
                        elif w == 11:
                            temp_dict.update({'nlyf': temp_data[1].strip('""')})
                    # print(temp_dict)
                    weather40day.append(temp_dict)
                elif i >= j:
                    temp_dict = {}
                    for w, weather in enumerate(temp_list):
                        temp_data = weather.split(':')
                        if w == 8:
                            temp_dict.update({'temp_l': temp_data[1].strip('""') + '℃'})
                        elif w == 2:
                            temp_dict.update({temp_data[0].strip('""'): temp_data[1].strip('""')})
                        elif w == 3:
                            temp_dict.update({'humidity': temp_data[1].strip('""')})
                        elif w == 6:
                            temp_dict.update({'temp_h': temp_data[1].strip('""') + '℃'})
                        elif w == 12:
                            temp_dict.update({'rain': temp_data[1].strip('""') + 'mm'})
                        elif w == 0:
                            temp_dict.update({temp_data[0].strip('""'): temp_data[1].strip('""')})
                        elif w == 1:
                            temp_dict.update({temp_data[0].strip('""'): temp_data[1].strip('""')})
                        elif w == 13:
                            temp_dict.update({'weather': temp_data[1].strip('""')})
                        elif w == 14:
                            temp_dict.update({'wind': temp_data[1].strip('""')})
                        elif w == 10:
                            temp_dict.update({'nl': temp_data[1].strip('""')})
                        elif w == 11:
                            temp_dict.update({'nlyf': temp_data[1].strip('""')})
                    weather40day.append(temp_dict)
                    # print(temp_dict)
            pprint(weather40day)
            calender_data = {
                'alins': weather40day[j].get('alins'),
                'als': weather40day[j].get('als'),
                'calender': weather40day[j].get('nlyf') + weather40day[j].get('nl'),
            }
            # print(calender_data)
            item = WeatherDay40Item()
            item['weather_day40'] = weather40day
            item['code'] = code
            item['calendar_data'] =calender_data
            item['city_name'] = city_name

            yield item
        except Exception as e:
            print('40天天气数据获取失败%s' % e)
            url = 'http://www.weather.com.cn/weather40dn/{}.shtml'.format(code)
            yield scrapy.Request(url=url, callback=self.parse)