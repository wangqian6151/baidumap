# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field


class ConvenientStoreItem(Item):
    collection = table = 'ConvenientStore'

    query = Field()
    name = Field()
    lat = Field()
    lng = Field()
    address = Field()
    province = Field()
    city = Field()
    area = Field()
    street_id = Field()
    telephone = Field()
    detail = Field()
    id = Field()
    tag = Field()
    type = Field()
    detail_url = Field()
    overall_rating = Field()
    comment_num = Field()
    navi_lng = Field()
    navi_lat = Field()


class JewelryStoreItem(Item):
    collection = table = 'JewelryStore'

    query = Field()
    name = Field()
    lat = Field()
    lng = Field()
    address = Field()
    province = Field()
    city = Field()
    area = Field()
    street_id = Field()
    telephone = Field()
    detail = Field()
    id = Field()
    tag = Field()
    indoor_floor = Field()
    type = Field()
    detail_url = Field()
    price = Field()
    overall_rating = Field()
    comment_num = Field()
    navi_lng = Field()
    navi_lat = Field()

