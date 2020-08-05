# -*- coding: utf-8 -*-
import time
import pymysql
from pprint import pprint
from datetime import datetime
from weather_day40.elastic_obj import ElasticObj

obj_day40 = ElasticObj('weather_day40', 'text')
obj_history = ElasticObj('weather_history', 'text')
obj_calender = ElasticObj('calender', 'text')


class WeatherDay40Pipeline(object):
    def __init__(self):
        # self.conn = pymysql.connect('192.168.2.101', 'lty', 'lty@100729', 'weather', 63126, charset="utf8",
        #                             use_unicode=True)
        # self.cursor = self.conn.cursor()
        pass

    def process_item(self, item, spider):
        cur_time = time.strftime('%Y-%m-%d', time.localtime())
        list_data_day40 = [
            {
                'type': 'text',
                'date': cur_time,
                'source': '40天天气',
                'weather_day40': item.get('weather_day40'),
                'link': 'http://www.weather.com.cn/weather40dn/%s.shtml' % item.get('code'),
                'keyword': '40天天气',
                'title': '%s,%s' % (cur_time, item.get('code'))
            },
        ]

        day_of_week = datetime.now().isoweekday()
        num_dict = {"1": u"一", "2": u"二", "3": u"三", "4": u"四", "5": u"五", "6": u"六", "7": u"日"}
        week = '星期' + num_dict.get(str(day_of_week))
        if item.get('calendar_data'):
            item.get('calendar_data').update({'week': week})
        list_calender = [
            {
                'type': 'text',
                'date': cur_time,
                'source': 'calender',
                'calender': item.get('calendar_data'),
                'link': '',
                'keyword': '农历',
                'title': '%s' % (cur_time)
            },
        ]
        list_history = [
            {
                'type': 'text',
                'date': cur_time,
                'source': 'calender',
                'calender': item.get('weather_day40_history'),
                'link': '',
                'keyword': '农历',
                'title': '%s' % (cur_time)
            }
        ]
        times = time.strftime('%Y-%m-%d', time.localtime())
        if item.get('weather_day40') and item.get('code'):
            obj_day40.index_data(list_data_day40, times + '-' + item.get('code'))
        if item.get('calendar_data'):
            obj_calender.index_data(list_calender, times)
        if item.get('weather_day40_history') and item.get('code'):
            t = item.get('weather_day40_history').pop()
            obj_history.index_data(list_history, t + '-' + item.get('code'))


if __name__ == '__main__':
    # data = obj_calender.get_data_id('2020-07-31')
    data = obj_history.get_data_id('202107-101010100')
    pprint(data)
    # obj_history.delete_index('weather_history')
    # obj_calender.delete_index('weather_day40')
    # pprint(data)