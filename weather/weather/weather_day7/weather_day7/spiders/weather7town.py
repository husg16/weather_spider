# -*- coding: utf-8 -*-
from pprint import pprint
import scrapy
from scrapy_redis.spiders import RedisCrawlSpider

from weather_day7.items import WeatherDay7Item


class Weather7townSpider(RedisCrawlSpider):
    name = 'weather7town'
    allowed_domains = ['weather.com.cn']
    # start_urls = ['http://forecast.weather.com.cn/town/weathern/101200101019.shtml']
    redis_key = 'weather_day7town:start_urls'

    def parse(self, response):
        try:
            url = response.request.url
            code = url.split('/').pop().split('.')[0]
            print(code)
            weather7d_list = []
            temp_svg_list = response.xpath('//div[@class="blueFor-container"]/script/text()').get().split('=')[2:]
            temp_h = temp_svg_list[0].split(';')[0].strip(' []').split(',')
            temp_l = temp_svg_list[1].split(';')[0].strip(' []').split(',')

            li_list = response.xpath('//div[@class="blueFor-container"]/ul[1]/li')
            time_list = []
            for li in li_list:
                time = li.xpath('./p[1]/text()').get()
                time_list.append(time)

            li1_list = response.xpath('//div[@class="blueFor-container"]/ul[2]/li')[0:8]
            for i, li1 in enumerate(li1_list):
                weather = li1.xpath('./p[1]/@title').get()
                wind1 = li1.xpath('./div/i[1]/@title').get()
                wind2 = li1.xpath('./div/i[2]/@title').get()
                wind_num = li1.xpath('./p[4]/text()').get().strip('\r\n').strip(' ').strip('\r\n')
                weather7d_dict = {
                    'weather': weather,
                    'wind': wind1 + '转' + wind2,
                    'wind_num': wind_num,
                    'time': time_list[i],
                    'temp': temp_l[i].strip('""') + '/' + temp_h[i].strip('""') + '℃'
                }
                weather7d_list.append(weather7d_dict)
            # pprint(weather7d_list)
            item = WeatherDay7Item()
            item['weather_day7'] = weather7d_list
            item['code'] = code
            yield item
        except Exception as e:
            url = 'http://forecast.weather.com.cn/town/weathern/{}.shtml'.format(code)
            yield scrapy.Request(url=url, callback=self.parse)