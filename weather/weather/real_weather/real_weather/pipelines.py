# -*- coding: utf-8 -*-
from pprint import pprint
import pymysql
import time

from real_weather.elastic_obj import ElasticObj

obj_real = ElasticObj('real_weather', 'text')
obj_24h = ElasticObj('weather24h', 'text')
obj_1h = ElasticObj('weather1h', 'text')
obj_life = ElasticObj('life_index', 'text')


class RealWeatherPipeline(object):
    def __init__(self):
        # self.conn = pymysql.connect('192.168.27.101', 'ltkhjky', '00729', 'weather', 63126, charset="utf8",
        #                             use_unicode=True)
        # self.cursor = self.conn.cursor()
        pass

    def process_item(self, item, spider):
        cur_time = time.strftime('%Y-%m-%d', time.localtime())
        # # 保存天气指数到mysql
        # try:
        #     insert_sql = """
        #                                         insert into weather_index(city_code,blood_glucose,dieted,wash_car,aqi,dressing,uv,date,cold,sport)
        #                                         VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        #                                                      """
        #     if item.get('life_index'):
        #         self.cursor.execute(insert_sql,
        #                             (item.get('code'), item.get('life_index').get('·血糖'), item.get('life_index').get('减肥'),
        #                              item.get('life_index').get('洗车'),
        #                              item.get('life_index').get('空气污染扩散'), item.get('life_index').get('穿衣'),
        #                              item.get('life_index').get('紫外线'), cur_time, item.get('life_index').get('感冒'),
        #                              item.get('life_index').get('运动')
        #                              ))
        #         self.conn.commit()
        # except Exception as e:
        #     print(e)

        dates = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        list_data_real = [
            {
                'type': 'text',
                'date': cur_time,
                'source': '实况',
                'real': item.get('real_weather'),
                'link': 'http://www.weather.com.cn/weathern/{}.shtml'.format(item.get('code')),
                'keyword': dates,
                'title': '%s,%s' % (cur_time, item.get('code'))
            },
        ]
        list_data_1h = [
            {
                'type': 'text',
                'date': cur_time,
                'source': '整点天气',
                'weather_every_time': item.get('weather_every_time'),
                'link': 'http://www.weather.com.cn/weathern/101200101.shtml',
                'keyword': '整点天气',
                'title': '%s,%s' % (cur_time, item.get('code'))
            },
        ]
        list_data_24h = [
            {
                'type': 'text',
                'date': cur_time,
                'source': '24小时历史',
                'weather_24h': item.get('weather_24h'),
                'link': 'http://www.weather.com.cn/weathern/101200101.shtml',
                'keyword': '历史天气',
                'title': '%s,%s' % (cur_time, item.get('code'))
            },
        ]

        list_data_index = [{
                'type': 'text',
                'date': cur_time,
                'source': '生活指数',
                'life_index': item.get('life_index'),
                'link': 'http://www.weather.com.cn/weathern/{}.shtml'.format(item.get('code')),
                'keyword': '生活指数',
                'title': '%s,%s' % (cur_time, item.get('code'))
        }]

        times = time.strftime('%Y-%m-%d-%H-%M', time.localtime())
        # 保存数据到es
        if item.get('real_weather'):
            obj_real.index_data(list_data_real, times + '-' + item.get('code'))
        times = time.strftime('%Y-%m-%d', time.localtime())
        if item.get('weather_24h'):
            obj_24h.index_data(list_data_24h, times + '-' + item.get('code'))
        if item.get('weather_every_time'):
            obj_1h.index_data(list_data_1h, times + '-' + item.get('code'))
        if item.get('life_index'):
            obj_life.index_data(list_data_index, times + '-' + item.get('code'))


if __name__ == '__main__':
    # obj = ElasticObj('real_weather', 'ott')
    # obj.create_index()
    # obj.index_data()
    # obj.bulk_index_data()
    # obj.del_index_data('1')
    # da = obj.search_data(5)
    # obj.delete_index('weather')
    # data_real = obj_real.query_data_by_body('2020-07-31,101200101')
    # data_real = obj_real.query_data_by_body('2020-07-11,101290904005')
    # data_real = obj_real.query_data_by_bodys('101200101')
    data_real = obj_life.get_data_id('2020-07-31-20-26-101200201')
    pprint(data_real)
    # data_24h = obj_24h.query_data_by_body('2020-07-13,101200101')
    # pprint(data_24h)
    # data_1h = obj_1h.query_data_by_body('2020-07-13,101200101')
    # pprint(data_1h)

    # obj_1h.es.delete(index='weather1h', id='L0TKN3MBCqN9E5EVaK5p', doc_type='text')
    # obj.delete_index('real_weather')
