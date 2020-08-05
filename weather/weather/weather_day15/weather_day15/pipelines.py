# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pprint import pprint
import time

from weather_day15.elastic_obj import ElasticObj

obj_day15 = ElasticObj('weather_day15', 'text')


class WeatherDay15Pipeline(object):

    def process_item(self, item, spider):
        cur_time = time.strftime('%Y-%m-%d', time.localtime())
        list_data_day15 = [
            {
                'type': 'text',
                'date': cur_time,
                'source': '15天天气',
                'weather_day15': item.get('weather_day15'),
                'link': 'http://www.weather.com.cn/weather15dn/%s.shtml' % item.get('code'),
                'keyword': '15天天气',
                'title': '%s,%s' % (cur_time, item.get('code'))
            },
        ]
        times = time.strftime('%Y-%m-%d', time.localtime())
        if item.get('weather_day15') and item.get('code'):
            obj_day15.index_data(list_data_day15, times + '-' + item.get('code'))


if __name__ == '__main__':
    data = obj_day15.query_data_by_body('2020-07-31,101200101')
    pprint(data)
    # obj_day15.es.delete(index='weather_day15', id='OUX6RXMBCqN9E5EVHgt1', doc_type='arrays')
    # obj_day15.delete_index('weather_day15')

