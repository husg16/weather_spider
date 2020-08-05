# -*- coding: utf-8 -*-
import time
import pymysql
from alarm.elastic_obj import ElasticObj

obj_alarm = ElasticObj('alarm', 'text')


class AlarmPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect('127.0.0.1', 'ltgdgy', '112100729', 'weather', 63126, charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        city_code = item.get('alarm_dict').get('EFFECT')
        province_name = item.get('alarm_dict').get('PROVINCE')
        # 如果城市code没有获取到，需要去查表重新获取
        if not city_code or len(city_code) < 9:
            city_code = self.get_city_code(province_name.strip('省'))
            item.get('alarm_dict').update({'city_code': city_code})

        cur_time = time.strftime('%Y-%m-%d', time.localtime())
        dates = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        list_data_alarm = [
            {
                'type': 'text',
                'date': cur_time,
                'source': '实况',
                'alarm':  item.get('alarm_dict'),
                'link': '',
                'keyword': dates,
                'title': '%s,%s' % (cur_time, item.get('code'))
            },
        ]
        times = time.strftime('%Y-%m-%d-%H-%M', time.localtime())
        # 保存数据到es
        if item.get('alarm_dict'):
            obj_alarm.index_data(list_data_alarm, times + '-' + item.get('code'))

    def get_city_code(self, name=''):
        """
        获取城市code
        :param name: 省名称
        :return: 返回城市code
        """
        try:
            sql = """
                            select id from city_test where city_zh=%s
                    """ % repr(name)
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            return res[0]
        except Exception as e:
            print(e)
