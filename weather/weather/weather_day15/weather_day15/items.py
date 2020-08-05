# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeatherDay15Item(scrapy.Item):
    # define the fields for your item here like:
    weather_day15 = scrapy.Field()
    code = scrapy.Field()