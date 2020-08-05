from pprint import pprint
import scrapy
from scrapy_redis.spiders import RedisCrawlSpider

from real_weather.items import RealWeatherItem


class RealTownSpider(RedisCrawlSpider):
    name = 'real_town'
    allowed_domains = ['weather.com.cn']
    redis_key = 'real_town:start_urls'
    # start_urls = ['http://forecast.weather.com.cn/town/weather1dn/101200101019.shtml']

    def parse(self, response):
        item = RealWeatherItem()
        url = response.request.url.split('/')
        code = url[-1].split('.')[0]
        try:
            temp = response.xpath('//div[@class="todayLeft"]/div[3]/span[1]/text()').get()
            temp1 = response.xpath('//div[@class="todayLeft"]/div[3]/span[2]/text()').get()
            weather = response.xpath('//div[@class="todayLeft"]/div[4]/text()').get()
            wind = response.xpath('//div[@class="todayLeft"]/p[1]/span/text()').get()
            humidity = response.xpath('//div[@class="todayLeft"]/p[2]/span/text()').get()
            update_time = response.xpath('//div[@class="todayLeft"]/div[1]/div/span/text()').get()
            real_weather_dict = {'update_time': update_time, 'temp': temp + temp1, 'weather': weather, 'wind': wind,
                                 'humidity': humidity, 'city_code': code}
            pprint(real_weather_dict)

            item['real_weather'] = real_weather_dict
            item['code'] = code

            yield item
        except Exception as e:
            url = 'http://forecast.weather.com.cn/town/weather1dn/{}.shtml'.format(code)
            yield scrapy.Request(url=url, callback=self.parse)