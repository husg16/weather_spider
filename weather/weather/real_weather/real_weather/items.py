# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RealWeatherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    real_weather = scrapy.Field()
    weather_every_time = scrapy.Field()
    weather_24h = scrapy.Field()
    life_index = scrapy.Field()
    code = scrapy.Field()