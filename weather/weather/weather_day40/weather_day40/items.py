# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeatherDay40Item(scrapy.Item):
    # define the fields for your item here like:
    weather_day40 = scrapy.Field()
    weather_day40_history = scrapy.Field()
    code = scrapy.Field()
    calendar_data = scrapy.Field()
    city_name = scrapy.Field()
