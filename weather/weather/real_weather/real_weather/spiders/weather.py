import time
from pprint import pprint
import requests
import scrapy
from selenium import webdriver
import re
from pprint import pprint
from scrapy_redis.spiders import RedisCrawlSpider

from real_weather.items import RealWeatherItem
from real_weather.utils import weather_code, wind_speed_code, wind_direction_code


class WeatherSpider(RedisCrawlSpider):
    name = 'weather'
    allowed_domains = ['weather.com.cn']
    redis_key = 'real_weather:start_urls'
    # start_urls = ['http://www.weather.com.cn/weather1dn/101200101.shtml']
    # start_urls = ['http://forecast.weather.com.cn/town/weather1dn/101200101019.shtml']

    def parse(self, response):
        url = response.request.url.split('/')
        code = url[-1].split('.')[0]
        if len(code) == 9:
            try:
                li_list = response.xpath('//div[@class="todayRight"]/script/text()').get()
                li_list = li_list.split(';')[0].split('=')[1].strip('[[]]').strip('{}').split('},{')
                for i in li_list:
                    if len(i) > 80:
                        li_list.remove(i)
                        i = i.split('}],[{')
                        li_list += i

                # 每小时天气数据
                try:
                    weather1hour_list = []
                    for i, j in enumerate(li_list):
                        weather1hour_dict = {}
                        if i < 24:
                            i_list = j.split(',')
                            ja = i_list[0].split(':')
                            weather1hour_dict.update({'weather': weather_code.get(str(ja[1].strip('""')))})
                            jb = i_list[1].split(':')
                            weather1hour_dict.update({'temp': str(jb[1].strip('""')) + '℃'})
                            jc = i_list[2].split(':')
                            weather1hour_dict.update({'wind_num': wind_speed_code.get(str(jc[1].strip('""')))})
                            jd = i_list[3].split(':')
                            weather1hour_dict.update({'wind_direction': wind_direction_code.get(str(jd[1].strip('""')))})
                            je = i_list[4].split(':')
                            weather1hour_dict.update({'humidity': str(je[1].strip('""')) + '%'})
                            jf = i_list[5].split(':')
                            weather1hour_dict.update({'time': str(jf[1].strip('""'))})
                            weather1hour_list.append(weather1hour_dict)
                    print('=======================每小时天气===========================')
                    pprint(weather1hour_list)

                except Exception as e:
                    print('每小时天气获取失败')

                # 生活指数
                try:
                    li_list = response.xpath('//div[@class="weather_shzs weather_shzs_1d"]/ul/li')
                    life_index1 = []
                    for li in li_list:
                        life_index1.append(li.xpath('./h2/text()').get())
                    dl_list = response.xpath('//div[@class="lv"]/dl')
                    life_index2 = []
                    for dl in dl_list:
                        life_index2.append(dl.xpath('./dt/em/text()').get() + ',' + dl.xpath('./dd/text()').get())
                    life_index = dict(zip(life_index1, life_index2))
                    print('=======================生活指数===========================')
                    print(life_index)
                except Exception as e:
                    print('生活指数获取失败')
                # 过去24小时天气数据
                try:
                    observe24h_data = response.xpath('//div[@class="weather_zdsk"]/script/text()').get()
                    observe24h_data_list = observe24h_data.split('=')[1].strip('( ').strip(';\n').split(':[{')[1].strip(
                        '}]}}').split('},{')
                    observe24h_dict_list = []
                    for data in observe24h_data_list:
                        observe24h_dict = {}
                        data = data.split(',')
                        # print(data)
                        # print('==================================>')
                        observe24h_dict.update({'time': data[0].split(':')[1].strip('""')})
                        observe24h_dict.update({'temp': data[1].split(':')[1].strip('""')})
                        observe24h_dict.update({'wind': data[3].split(':')[1].strip('""')})
                        observe24h_dict.update({'wind_num': wind_speed_code.get(str(data[4].split(':')[1].strip('""')))})
                        observe24h_dict.update({'rain': data[5].split(':')[1].strip('""')})
                        observe24h_dict.update({'humidity': data[6].split(':')[1].strip('""')})
                        observe24h_dict.update({'air': data[7].split(':')[1].strip('""')})
                        observe24h_dict_list.append(observe24h_dict)
                    print('=======================24小时天气===========================')
                    pprint(observe24h_dict_list)
                except Exception as e:
                    print('过去24小时天气数据获取失败')
                item = RealWeatherItem()
                item['weather_24h'] = observe24h_dict_list
                item['life_index'] = life_index
                item['weather_every_time'] = weather1hour_list
                item['code'] = code
                yield item
            except Exception as e:
                url = 'http://www.weather.com.cn/weather1dn/{}.shtml'.format(code)
                yield scrapy.Request(url=url, callback=self.parse)
        # else:
        #     try:
        #         # 每小时天气
        #         weather1h_text = response.xpath('//div[@class="L_weather"]/script/text()').get().split('=')[1].split(';')[0].strip("}]')").strip("(' ' '[{").split('"},{"')
        #         weather1h_list = []
        #         for weather1h in weather1h_text:
        #             weather = weather1h.split(',')
        #             weather.pop(1)
        #             day1_dict = {}
        #             for i, w in enumerate(weather):
        #                 w = w.split(':')
        #                 day1_dict.update({w[0].strip('""'): w[1].strip('""')})
        #             weather1h_list.append(day1_dict)
        #         pprint(weather1h_list)
        #
        #         # 过去24小时天气
        #         weather24h_text = response.xpath('//div[@class="weather_zdsk"]/script/text()').get()
        #         observe24h_data_list = weather24h_text.split('=')[1].strip('( ').strip(';\n').split(':[{')[1].strip(
        #             '}]}}').split('},{')
        #         observe24h_dict_list = []
        #         for data in observe24h_data_list:
        #             data = data.strip('}]}};\r')
        #             observe24h_dict = {}
        #             data = data.split(',')
        #             observe24h_dict.update({'time': data[0].split(':')[1].strip('""')})
        #             observe24h_dict.update({'temp': data[1].split(':')[1].strip('""')})
        #             observe24h_dict.update({'wind': data[3].split(':')[1].strip('""')})
        #             observe24h_dict.update({'wind_num': wind_speed_code.get(str(data[4].split(':')[1].strip('""')))})
        #             observe24h_dict.update({'rain': data[5].split(':')[1].strip('""')})
        #             observe24h_dict.update({'humidity': data[6].split(':')[1].strip('""')})
        #             observe24h_dict.update({'air': data[7].split(':')[1].strip('""')})
        #             observe24h_dict_list.append(observe24h_dict)
        #         observe24h_dict_list.reverse()
        #         pprint(observe24h_dict_list)
        #
        #         # 生活指数
        #         index_li = response.xpath('//div[@class="weather_shzs weather_shzs_1d"]/ul/li')
        #         li_list = [li.xpath('./h2/text()').get() for li in index_li]
        #         index_dl = response.xpath('//div[@class="lv"]/dl')
        #         dl_list = [dl.xpath('./dt/em/text()').get() + '.' + dl.xpath('./dd/text()').get() for dl in index_dl]
        #         index_dict = {}
        #         for i, li in enumerate(li_list):
        #             index_dict.update({li: dl_list[i]})
        #         print(index_dict)
        #
        #         item = RealWeatherItem()
        #         item['weather_24h'] = observe24h_dict_list
        #         item['weather_every_time'] = weather1h_list
        #         item['code'] = code
        #         item['life_index'] = index_dict
        #         yield item
        #     except Exception as e:
        #         url = 'http://forecast.weather.com.cn/town/weather1dn/{}.shtml'.format(code)
        #         yield scrapy.Request(url=url, callback=self.parse)