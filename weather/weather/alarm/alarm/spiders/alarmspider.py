# -*- coding: utf-8 -*-
import time
from pprint import pprint
import requests
import scrapy
import uuid
from scrapy_redis.spiders import RedisCrawlSpider

from alarm.items import AlarmItem
from alarm.pipelines import AlarmPipeline
from alarm.settings import DEFAULT_REQUEST_HEADERS


class AlarmspiderSpider(scrapy.Spider):
    name = 'alarmspider'
    allowed_domains = ['weather.com.cn']
    start_urls = ['http://www.weather.com.cn']

    def parse(self, response):
        try:
            # 获取预警信息url
            header = DEFAULT_REQUEST_HEADERS
            res = requests.get('http://product.weather.com.cn/alarm/grepalarm_cn.php', headers=header)
            alarm_list = res.content.decode().split('"data":')[1].strip('};').strip('[').strip(']').split('],[')
            # 预警信息url列表
            alarm_link_list = []
            uuid_str = uuid.uuid1()
            for alarm_link in alarm_list:
                alarm_link_url = alarm_link.split(',')[1].strip('""').strip("''")
                print(alarm_link_url)
                cur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                # 保存url到数据库去重
                self.save_alarm_url(alarm_link_url, str(uuid_str), cur_time)
                # alarm_link_list.append(alarm_link_url)

            # 取出预警url
            alarm_link_list = self.get_alarm_url(str(uuid_str))
            # 获取预警信息的具体内容
            for url in alarm_link_list:
                time.sleep(0.5)
                res = requests.get(
                    'http://product.weather.com.cn/alarm/webdata/%s?_=%s' % (url, str(time.time() * 100).split('.')[0]), headers=header)
                alarm_data = res.content.decode().split('=')[1].strip('{}').split(',')
                # 预警信息的具体内容字典
                alarm_dict = {}
                for data in alarm_data:
                    alarm = data.split('":"')
                    if len(alarm) >= 2:
                        alarm_dict.update({alarm[0].strip('"'): alarm[1].strip('"')})
                        # alarm_list.append(alarm_dict)

                # 预警信息存数据库
                pprint(alarm_dict)
                item = AlarmItem()
                item['alarm_dict'] = alarm_dict
                yield item
        except Exception as e:
            print(e)

    def save_alarm_url(self, url, uuid, time):
        """
        把获取的预警url存入数据库，如果url重复就不会存入
        :param url: 预警信息url
        :param uuid: 每次存储url的唯一标示，用于查询最新的预警信息
        :param time: 存储时间
        """
        conn = AlarmPipeline().conn
        cursor = conn.cursor()
        insert_sql = """
                        insert into alarm_url_set(url,uuid,time)
                        VALUES(%s, %s, %s)
                                                                             """
        try:
            cursor.execute(insert_sql,
                           (url, uuid, time
                            ))
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def get_alarm_url(self, uuid):
        """
        获取最新的预警url
        :param uuid: uuid
        :return: 返回最新的url列表
        """
        conn = AlarmPipeline().conn
        cursor = conn.cursor()
        sql = """
                    select url from alarm_url_set where uuid=%s
        """ % repr(uuid)
        cursor.execute(sql)
        res = cursor.fetchall()
        alarm_link_list = []
        for url in res:
            alarm_link_list.append(url[0])
        conn.close()
        return alarm_link_list

