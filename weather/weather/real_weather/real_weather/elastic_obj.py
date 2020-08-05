import os
import time
from os import walk
from datetime import datetime
from pprint import pprint

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class ElasticObj:
    def __init__(self, index_name, index_type, ip=('192.168.25.101',)):
        """
        :param index_name: 索引名称
        :param index_type: 索引类型
        :param ip:
        """
        self.index_name = index_name
        self.index_type = index_type
        # self.es = Elasticsearch(list(ip), http_auth=('es', 'lty@100729'), port=9200)
        self.es = Elasticsearch(list(ip), http_auth=('es', '107670729'), port=9200)

    def create_index(self, index_name="lty", index_type="lty_crawl"):
        _index_mappings = {
            "settings": {
                "number_of_shards": 3,
                "number_of_replicas": 0,
                "analysis": {
                    "analyzer": {
                        "ik": {
                            "tokenizer": "ik_max_word"
                        }
                    }
                }
            },
            "mappings": {
                self.index_type: {
                    "properties": {
                        "id": {
                            "type": "keyword",
                            "index": True
                        },
                        "title": {
                            "type": "text",
                            "index": True,
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "keyword": {
                            "type": "text",
                            "index": True
                        },
                        "link": {
                            "type": "keyword",
                            "index": True
                        },
                        "datetime": {
                            "type": "keyword",
                            "index": True
                        },
                        "copyfrom": {
                            "type": "keyword",
                            "index": False
                        }
                    }
                }

            }
        }
        if self.es.indices.exists(index=self.index_name) is not True:
            res = self.es.indices.create(index=self.index_name, body=_index_mappings)
            return res

    def index_data(self, list_data, id):
        """保存数据到es"""
        # list_data = [
        #     {
        #         'date': '2019-03-28',
        #         'source': '蓝泰源',
        #         'link': 'http://www.lantaiyun.com',
        #         'keyword': '智能公交管理系统',
        #         'title': '蓝泰源 公交 智能公交 管理系统 公交系统',
        #     },
        #     {
        #         'date': '2019-03-28',
        #         'source': '慧行云',
        #         'link': 'http://www.huixingyun.com',
        #         'keyword': 'saas公交管理平台',
        #         'title': '蓝泰源 saas 公交 管理平台 公交平台',
        #     }
        # ]
        for item in list_data:
            # res = self.es.index(index=self.index_name, doc_type=self.index_type, body=item)
            type = item.pop('type')
            res = self.es.index(index=self.index_name, doc_type=type, body=item, id=id)
            print(res)

    def bulk_index_data(self):
        """用bulk批量保存数据到es"""
        list_data = [
            {
                'date': '2019-03-28',
                'source': '蓝泰源',
                'link': 'http://www.lantaiyun.com',
                'keyword': '智能公交管理系统',
                'title': '蓝泰源 公交 智能公交 管理系统 公交系统',
            },
            {
                'date': '2019-03-28',
                'source': '慧行云',
                'link': 'http://www.huixingyun.com',
                'keyword': 'saas公交管理平台',
                'title': '蓝泰源 saas 公交 管理平台 公交平台',
            },
            {
                'date': '2019-03-28',
                'source': '坐公交',
                'link': 'http://www.huixingyun.com',
                'keyword': '坐公交app',
                'title': '蓝泰源 坐公交 app',
            },
            {
                'date': '2019-03-28',
                'source': '云终端管理平台',
                'link': 'http://www.huixingyun.com',
                'keyword': 'TMP云终端管理平台',
                'title': '蓝泰源 TMP 公交 管理平台 云终端',
            }
        ]

        ACTIONS = [self._get_one_data(line) for line in list_data]
        # print(ACTIONS)
        success, _ = bulk(self.es, ACTIONS, index=self.index_name, raise_on_error=True)

    def del_index_data(self, id):
        """删除索引中的一条数据"""
        res = self.es.delete(index=self.index_name, doc_type=self.index_type, id=id)
        print(res)

    def get_data_id(self, id):
        """根据id获取一条数据"""
        try:
            res = self.es.get(index=self.index_name, doc_type=self.index_type, id=id)
            return res
        except Exception as e:
            print(e)

    def search_data(self, size):
        """获取多条数据"""
        res = self.es.search(index=self.index_name, doc_type=self.index_type, size=size)

        # 输出查询到的结果
        # for r in res['hits']['hits']:
        #     print(r.get('_source'))
        print(res)

    def query_data_by_body(self, keyword):
        """查询关键字"""
        doc = {
            "query": {
                "match": {
                    "title": keyword,
                }
            }
        }
        _searched = self.es.search(index=self.index_name, doc_type=self.index_type, body=doc)

        # 输出查询到的结果
        # print(_searched)
        return _searched
        # for hit in _searched['hits']['hits']:
        #     print(hit['_source']['data'], hit['_source']['source'],
        #           hit['_source']['link'], hit['_source']['keyword'], hit['_source']['title'])


    def query_data_by_bodys(self, keyword):
        """查询关键字"""
        doc = {
            "query": {
                "match": {
                    "keyword": keyword,
                }
            }
        }
        _searched = self.es.search(index=self.index_name, doc_type=self.index_type, body=doc)

        # 输出查询到的结果
        # print(_searched)
        return _searched

    def _get_one_data(self, data):
        """获取一条数据"""
        id_num = 0
        action = {
            '_index': self.index_name,
            '_type': self.index_type,
            # '_id': id_num,  # 也可以默认生成，不赋值
            '_source': {
                'date': data.get('date'),
                "source": data.get('source'),
                "link": data.get('link'),
                "keyword": data.get('keyword'),
                "title": data.get('title')
            }
        }
        id_num += 1
        return action


    def delete_index(self, index_name):
        """删除索引"""
        res = self.es.indices.delete(index_name)
        print(res)


if __name__ == '__main__':
    # obj = ElasticObj('ott', 'ott_type', ip=('192.168.2.188', '192.168.2.190', '192.168.2.191'))
    obj = ElasticObj('real_weather', 'text')
    # obj.create_index()
    # obj.index_data()
    # obj.bulk_index_data()
    # obj.del_index_data('1')
    # da = obj.search_data(5)
    # obj.delete_index('weather')
    # da = obj.query_data_by_body('指数')
    # da = obj._get_one_data(
    #     {
    #         'date': '2020-07-07',
    #         "source": '实况',
    #         "link": '',
    #         "keyword": '实况',
    #         "title": '实况, 2020-07-07, 101200101'
    #     }
    # )
    # pprint(data)
    # pprint(da)
    # obj.es.delete(index='weather', id='MTrWJ3MBCqN9E5EV4yWA', doc_type='weather_day7')
    # obj.es.delete(index='ott', id='mzgjJ3MBCqN9E5EVGudS', doc_type='ott_type')
    # obj.es.delete(index='ott', id='jDgwJ3MBCqN9E5EVIP6U', doc_type='ott_type')
    # obj.es.delete(index='ott', id='djglJ3MBCqN9E5EV1uz8', doc_type='ott_type')
    # obj.es.delete(index='ott', id='iDgwJ3MBCqN9E5EVHv6Q', doc_type='ott_type')
    # obj.delete_index('real_weather')