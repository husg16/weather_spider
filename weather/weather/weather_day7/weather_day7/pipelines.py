# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pprint import pprint
import time
from weather_day7.elastic_obj import ElasticObj

obj_day7 = ElasticObj('weather_day7', 'text')


class WeatherDay7Pipeline(object):
    def process_item(self, item, spider):
        cur_time = time.strftime('%Y-%m-%d', time.localtime())
        list_data_day7 = [
            {
                'type': 'text',
                'date': cur_time,
                'source': '7天天气',
                'weather_day7': item.get('weather_day7'),
                'link': 'http://www.weather.com.cn/weathern/%s.shtml' % item.get('code'),
                'keyword': '7天天气',
                'title': '%s,%s' % (cur_time, item.get('code'))
            },
        ]
        times = time.strftime('%Y-%m-%d', time.localtime())
        if item.get('weather_day7'):
            obj_day7.index_data(list_data_day7, times + '-' + item.get('code'))


if __name__ == '__main__':
    data = obj_day7.query_data_by_body('2020-07-13,101200501')
    pprint(data)
    # obj_day7.es.delete(index='weather_day7', id='6UQyOHMBCqN9E5EVnbBg', doc_type='text')

