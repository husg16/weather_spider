# -*- coding: utf-8 -*-
from pprint import pprint
import scrapy
from scrapy_redis.spiders import RedisCrawlSpider

from weather_day7.items import WeatherDay7Item


class Weather7Spider(RedisCrawlSpider):
    name = 'weather7'
    allowed_domains = ['weather.com.cn']
    redis_key = 'weather_day7:start_urls'

    def parse(self, response):
        url = response.request.url.split('.com.cn')
        if len(url[0]) == 18:
            code = url[1].split('.')[0][-9:]
            try:
                # 7天天气温度数据temp_h, temp_l（两个列表）
                # driver = drivers('weathern/{}'.format(code))
                # res = re.findall(r'-?[\d]+[.]?[\d]*°C', driver.page_source)[0:16]
                # temp_h, temp_l = res[0:8], res[8:]
                # driver.close()
                # print(temp_h, temp_l)
                temp_script = response.xpath('//div[@class="blueFor-container"]/script/text()').get().split(';\n')[0:2]
                temp_h = temp_script[0].split('=')[1].strip('[]').split(',')
                temp_l = temp_script[1].split('=')[1].strip('[]').split(',')

                li_list = response.xpath('//ul[@class="blue-container sky"]/li')
                # 日期数据
                day_list = response.xpath('//ul[@class="date-container"]/li')
                day_list = [i.xpath('./p[1]/text()').get() for i in day_list]
                day7_list = []
                for i, li in enumerate(li_list):
                    if i < 8:
                        day7_dict = {}
                        weather = li.xpath('./i[1]/@title').get()
                        weather1 = li.xpath('./i[2]/@title').get()
                        # weather = li.xpath('./p[1]/text()').get()
                        wind = li.xpath('./div/i[1]/@title').get() + '&' + li.xpath('./div/i[2]/@title').get()
                        wind_num = li.xpath('./p[3]/text()').get()
                        day7_dict.update({'weather': weather + '转' + weather1, 'wind': wind, 'wind_num': wind_num, 'time': day_list[i],
                                          'temp': temp_l[i].strip('""') + '/' + temp_h[i].strip('""') + '℃'})
                        day7_list.append(day7_dict)
                print('===================7天天气======================>>>')
                pprint(day7_list)
                item = WeatherDay7Item()
                item['weather_day7'] = day7_list
                item['code'] = code
                yield item
            except Exception as e:
                print('7天天气数据获取失败%s' % e)
                url = 'http://www.weather.com.cn/weathern/{}.shtml'.format(code)
                yield scrapy.Request(url=url, callback=self.parse)
        # else:
        #     try:
        #         url = response.request.url.split('.com.cn')
        #         code = url[1].split('.')[0][-12:]
        #         weather7d_list = []
        #         temp_svg_list = response.xpath('//div[@class="blueFor-container"]/script/text()').get().split('=')[2:]
        #         temp_h = temp_svg_list[0].split(';')[0].strip(' []').split(',')
        #         temp_l = temp_svg_list[1].split(';')[0].strip(' []').split(',')
        #
        #         li_list = response.xpath('//div[@class="blueFor-container"]/ul[1]/li')
        #         time_list = []
        #         for li in li_list:
        #             time = li.xpath('./p[1]/text()').get()
        #             time_list.append(time)
        #
        #         li1_list = response.xpath('//div[@class="blueFor-container"]/ul[2]/li')[0:8]
        #         for i, li1 in enumerate(li1_list):
        #             weather = li1.xpath('./p[1]/@title').get()
        #             wind1 = li1.xpath('./div/i[1]/@title').get()
        #             wind2 = li1.xpath('./div/i[2]/@title').get()
        #             wind_num = li1.xpath('./p[4]/text()').get().strip('\r\n').strip(' ').strip('\r\n')
        #             weather7d_dict = {
        #                 'weather': weather,
        #                 'wind': wind1 + '转' + wind2,
        #                 'wind_num': wind_num,
        #                 'time': time_list[i],
        #                 'temp': temp_l[i].strip('""') + '/' + temp_h[i].strip('""') + '℃'
        #             }
        #             weather7d_list.append(weather7d_dict)
        #         # pprint(weather7d_list)
        #         item = WeatherDay7Item()
        #         item['weather_day7'] = weather7d_list
        #         item['code'] = code
        #         yield item
        #     except Exception as e:
        #         url = 'http://forecast.weather.com.cn/town/weathern/{}.shtml'.format(code)
        #         yield scrapy.Request(url=url, callback=self.parse)