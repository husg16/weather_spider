# -*- coding: utf-8 -*-
from pprint import pprint
import scrapy
from scrapy_redis.spiders import RedisCrawlSpider

from weather_day15.items import WeatherDay15Item


class Weather15townSpider(RedisCrawlSpider):
    name = 'weather15town'
    allowed_domains = ['weather.com.cn']
    # start_urls = ['http://forecast.weather.com.cn/town/weather15dn/101200101019.shtml']
    redis_key = 'weather_day15town:start_urls'

    def parse(self, response):
        try:
            url = response.request.url
            code = url.split('/').pop().split('.')[0]
            print(code)
            weather15d_list = []
            temp_svg_list = response.xpath('//div[@class="blueFor-container sfd"]/script/text()').get().split('=')[1:]
            temp_h = temp_svg_list[0].split(';')[0].strip(' []').split(',')
            temp_l = temp_svg_list[1].split(';')[0].strip(' []').split(',')
            li_list = response.xpath('//div[@class="blueFor-container sfd"]/ul[1]/li')
            time_list = []
            for li in li_list:
                time = li.xpath('./p[1]/text()').get()
                time_list.append(time)

            li1_list = response.xpath('//div[@class="blueFor-container sfd"]/ul[2]/li')[0:8]
            for i, li1 in enumerate(li1_list):
                weather = li1.xpath('./p[1]/text()').get().strip('\r\n').strip(' ').strip('\r\n')
                wind1 = li1.xpath('./div/i[1]/@title').get()
                wind2 = li1.xpath('./div/i[2]/@title').get()
                wind_num = li1.xpath('./p[4]/text()').get().strip('\r\n').strip(' ').strip('\r\n')
                weather15d_dict = {
                    'weather': weather,
                    'wind': wind1 + '转' + wind2,
                    'wind_num': wind_num,
                    'time': time_list[i],
                    'temp': temp_l[i].strip('""') + '/' + temp_h[i].strip('""') + '℃'
                }
                weather15d_list.append(weather15d_dict)

            pprint(weather15d_list)
            item = WeatherDay15Item()
            item['weather_day15'] = weather15d_list
            item['code'] = code
            yield item
        except Exception as e:
            url = 'http://forecast.weather.com.cn/town/weather15dn/{}.shtml'.format(code)
            yield scrapy.Request(url=url, callback=self.parse)