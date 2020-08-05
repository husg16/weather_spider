from pprint import pprint
import scrapy
from scrapy_redis.spiders import RedisCrawlSpider

from weather_day15.items import WeatherDay15Item


class Weather15Spider(RedisCrawlSpider):
    name = 'weather15'
    allowed_domains = ['weather.com.cn']
    redis_key = 'weather_day15:start_urls'

    def parse(self, response):
        # 15天天气温度数据temp_h, temp_l（两个列表)
        url = response.request.url.split('.com.cn')
        if len(url[0]) == 18:
            code = url[1].split('.')[0][-9:]
            try:
                # 温度数据
                temp_script = response.xpath('//div[@class="blueFor-container sfd"]/script/text()').get().split(';\n')[2:4]
                temp_h = temp_script[0].split('=')[1].strip('[]').split(',')
                temp_l = temp_script[1].split('=')[1].strip('[]').split(',')

                li_list = response.xpath('//div[@class="blueFor-container sfd"]/ul[2]/li')
                # 日期数据
                day_list = response.xpath('//div[@class="blueFor-container sfd"]/ul[1]/li')
                day_list = [i.xpath('./p[1]/text()').get() for i in day_list]
                day15_list = []
                for i, li in enumerate(li_list):
                    if i < 8:
                        day15_dict = {}
                        weather = li.xpath('./i[1]/@title').get()
                        weather1 = li.xpath('./i[2]/@title').get()
                        wind = li.xpath('./div/i[1]/@title').get() + '&' + li.xpath('./div/i[2]/@title').get()
                        wind_num = li.xpath('./p[3]/text()').get().strip('\n')
                        pprint(wind_num)
                        day15_dict.update({'weather': weather + '转' + weather1, 'wind': wind, 'wind_num': wind_num, 'time': day_list[i],
                                           'temp': temp_l[i].strip('""') + '/' + temp_h[i].strip('""') + '℃'})
                        day15_list.append(day15_dict)
                # print('====================15天天气=====================>>>')
                pprint(day15_list)
                item = WeatherDay15Item()
                item['weather_day15'] = day15_list
                item['code'] = code
                yield item
            except Exception as e:
                print('15天天气数据获取失败 %s' % e)
                url = 'http://www.weather.com.cn/weather15dn/{}.shtml'.format(code)
                yield scrapy.Request(url=url, callback=self.parse)
        # else:
        #     try:
        #         url = response.request.url.split('.com.cn')
        #         code = url[1].split('.')[0][-12:]
        #         print(code)
        #         weather15d_list = []
        #         temp_svg_list = response.xpath('//div[@class="blueFor-container sfd"]/script/text()').get().split('=')[1:]
        #         temp_h = temp_svg_list[0].split(';')[0].strip(' []').split(',')
        #         temp_l = temp_svg_list[1].split(';')[0].strip(' []').split(',')
        #         li_list = response.xpath('//div[@class="blueFor-container sfd"]/ul[1]/li')
        #         time_list = []
        #         for li in li_list:
        #             time = li.xpath('./p[1]/text()').get()
        #             time_list.append(time)
        #
        #         li1_list = response.xpath('//div[@class="blueFor-container sfd"]/ul[2]/li')[0:8]
        #         for i, li1 in enumerate(li1_list):
        #             weather = li1.xpath('./p[1]/text()').get().strip('\r\n').strip(' ').strip('\r\n')
        #             wind1 = li1.xpath('./div/i[1]/@title').get()
        #             wind2 = li1.xpath('./div/i[2]/@title').get()
        #             wind_num = li1.xpath('./p[4]/text()').get().strip('\r\n').strip(' ').strip('\r\n')
        #             weather15d_dict = {
        #                 'weather': weather,
        #                 'wind': wind1 + '转' + wind2,
        #                 'wind_num': wind_num,
        #                 'time': time_list[i],
        #                 'temp': temp_l[i].strip('""') + '/' + temp_h[i].strip('""') + '℃'
        #             }
        #             weather15d_list.append(weather15d_dict)
        #
        #         # pprint(weather15d_list)
        #         item = WeatherDay15Item()
        #         item['weather_day15'] = weather15d_list
        #         item['code'] = code
        #         yield item
        #     except Exception as e:
        #         url = 'http://forecast.weather.com.cn/town/weather15dn/{}.shtml'.format(code)
        #         yield scrapy.Request(url=url, callback=self.parse)