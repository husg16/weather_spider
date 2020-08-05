import time
from pprint import pprint
import requests
import scrapy
import re
from pprint import pprint
from scrapy_redis.spiders import RedisCrawlSpider

from real_weather.items import RealWeatherItem
from real_weather.utils import weather_code, wind_speed_code, wind_direction_code


class WeatherTownSpider(RedisCrawlSpider):
    name = 'weather_town'
    allowed_domains = ['weather.com.cn']
    redis_key = 'real_weather_town:start_urls'
    # start_urls = ['http://forecast.weather.com.cn/town/weather1dn/101200101019.shtml']

    def parse(self, response):
        try:
            url = response.request.url.split('/')
            code = url[-1].split('.')[0]
            # 每小时天气
            weather1h_text = response.xpath('//div[@class="L_weather"]/script/text()').get().split('=')[1].split(';')[
                0].strip("}]')").strip("(' ' '[{").split('"},{"')
            weather1h_list = []
            for weather1h in weather1h_text:
                weather = weather1h.split(',')
                weather.pop(1)
                day1_dict = {}
                for i, w in enumerate(weather):
                    w = w.split(':')
                    day1_dict.update({w[0].strip('""'): w[1].strip('""')})
                weather1h_list.append(day1_dict)
            pprint(weather1h_list)

            # 过去24小时天气
            weather24h_text = response.xpath('//div[@class="weather_zdsk"]/script/text()').get()
            observe24h_data_list = weather24h_text.split('=')[1].strip('( ').strip(';\n').split(':[{')[1].strip(
                '}]}}').split('},{')
            observe24h_dict_list = []
            for data in observe24h_data_list:
                data = data.strip('}]}};\r')
                observe24h_dict = {}
                data = data.split(',')
                observe24h_dict.update({'time': data[0].split(':')[1].strip('""')})
                observe24h_dict.update({'temp': data[1].split(':')[1].strip('""')})
                observe24h_dict.update({'wind': data[3].split(':')[1].strip('""')})
                observe24h_dict.update({'wind_num': wind_speed_code.get(str(data[4].split(':')[1].strip('""')))})
                observe24h_dict.update({'rain': data[5].split(':')[1].strip('""')})
                observe24h_dict.update({'humidity': data[6].split(':')[1].strip('""')})
                observe24h_dict.update({'air': data[7].split(':')[1].strip('""')})
                observe24h_dict_list.append(observe24h_dict)
            observe24h_dict_list.reverse()
            pprint(observe24h_dict_list)

            # 生活指数
            index_li = response.xpath('//div[@class="weather_shzs weather_shzs_1d"]/ul/li')
            li_list = [li.xpath('./h2/text()').get() for li in index_li]
            index_dl = response.xpath('//div[@class="lv"]/dl')
            dl_list = [dl.xpath('./dt/em/text()').get() + '.' + dl.xpath('./dd/text()').get() for dl in index_dl]
            index_dict = {}
            for i, li in enumerate(li_list):
                index_dict.update({li: dl_list[i]})
            print(index_dict)

            item = RealWeatherItem()
            item['weather_24h'] = observe24h_dict_list
            item['weather_every_time'] = weather1h_list
            item['code'] = code
            item['life_index'] = index_dict
            yield item
        except Exception as e:
            url = 'http://forecast.weather.com.cn/town/weather1dn/{}.shtml'.format(code)
            yield scrapy.Request(url=url, callback=self.parse)