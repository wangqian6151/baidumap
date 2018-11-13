# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Request
from urllib.request import quote, unquote

from baidumap.items import ConvenientStoreItem, JewelryStoreItem


class BaiduPoiSpider(scrapy.Spider):
    name = 'baidu_poi'
    allowed_domains = ['api.map.baidu.com']
    base_url = 'http://api.map.baidu.com/place/v2/search?query={query}&scope=2&page_size=20&page_num={page_num}&bounds={bounds}&output=json&ak={ak}'

    # def get_bounds(self, lat_lb, lng_lb, lat_rt, lng_rt, las):
    #     # lat_lb = 22.243608
    #     # lng_lb = 113.684206
    #     # lat_rt = 22.862324
    #     # lng_rt = 114.658294  # 坐标范围
    #     # las = 0.03125  # 给las一个值
    #     lat_count = int((lat_rt - lat_lb) / las + 1)
    #     lon_count = int((lng_rt - lng_lb) / las + 1)
    #     self.logger.debug('lat_count: {} lon_count: {}'.format(lat_count, lon_count))
    #     print('lat_count: {} lon_count: {}'.format(lat_count, lon_count))
    #     for lat_c in range(0, lat_count):
    #         lat_b1 = round(lat_lb + las * lat_c, 6)
    #         for lon_c in range(0, lon_count):
    #             lon_b1 = round(lng_lb + las * lon_c, 6)
    #             loc_to_use = str(lat_b1) + ',' + str(lon_b1) + ',' + str(round(lat_b1 + las, 6)) + ',' + str(
    #                 round(lon_b1 + las, 6))
    #             self.bounds_list.append(loc_to_use)
    #     return

    def start_requests(self):
        ak = "1XjLLEhZhQNUzd93EjU5nOGQ"  # 这里填入你的百度API的ak
        # query = '便利店$超市$商店'
        # query = '便利店$超市'
        # query = '便利店'
        # query = '珠宝店'
        # query = '珠宝$首饰$黄金$银$金$钻石'
        # query = '珠宝$首饰'
        query = '珠宝首饰'
        lat_lb = 22.243608
        lng_lb = 113.684206
        lat_rt = 22.862324
        lng_rt = 114.658294  # 深圳市坐标范围
        # lat_lb = 22.416237
        # lng_lb = 113.684206
        # lat_rt = 22.862324
        # lng_rt = 113.987034  # 罗湖区坐标范围 113.684206,22.416237;113.987034,22.862324
        # las = 0.025  # 给las一个值
        # las = 0.007812  # 给las一个值
        # las = 0.003906  # 给las一个值
        las = 0.001953  # 给las一个值
        lat_count = int((lat_rt - lat_lb) / las + 1)
        lon_count = int((lng_rt - lng_lb) / las + 1)
        self.logger.debug('lat_count: {} lon_count: {}'.format(lat_count, lon_count))
        print('lat_count: {} lon_count: {}'.format(lat_count, lon_count))
        for lat_c in range(0, lat_count):
            lat_b1 = round(lat_lb + las * lat_c, 6)
            for lon_c in range(0, lon_count):
                lon_b1 = round(lng_lb + las * lon_c, 6)
                bounds = str(lat_b1) + ',' + str(lon_b1) + ',' + str(round(lat_b1 + las, 6)) + ',' + str(
                    round(lon_b1 + las, 6))
                url = self.base_url.format(query=query, page_num=0, bounds=bounds, ak=ak)
                url = quote(url, safe=";/?:@&=+$,", encoding="utf-8")
                self.logger.debug('start url: {}'.format(url))
                print('start url: {}'.format(url))
                yield Request(url, callback=self.parse_poi,
                              meta={'query': query, 'page_num': 0, 'bounds': bounds, 'ak': ak})

    def parse_poi(self, response):
        query = response.meta.get('query')
        page_num = response.meta.get('page_num')
        bounds = response.meta.get('bounds')
        ak = response.meta.get('ak')
        data = json.loads(response.text)
        print('data: {}'.format(data))
        self.logger.debug('data: {}'.format(data))
        if 'results' in data and data.get('results'):
            print("data.get('total'): {}".format(data.get('total')))
            self.logger.debug("data.get('total'): {}".format(data.get('total')))
            if data.get('total') == 400:
                print('parse_poi total = 400 url: {}'.format(response.url))
                self.logger.debug('parse_poi total = 400 url: {}'.format(response.url))
            for item in data.get('results'):
                if '便利店' in query:
                    convenient_store_item = ConvenientStoreItem()
                    convenient_store_item['query'] = query
                    convenient_store_item['name'] = item.get('name')
                    if item.get('location'):
                        convenient_store_item['lat'] = item.get("location").get("lat")
                        convenient_store_item['lng'] = item.get("location").get("lng")
                    convenient_store_item['address'] = item.get('address')
                    convenient_store_item['province'] = item.get('province')
                    convenient_store_item['city'] = item.get('city')
                    convenient_store_item['area'] = item.get('area')
                    convenient_store_item['street_id'] = item.get('street_id')
                    convenient_store_item['telephone'] = item.get('telephone')
                    convenient_store_item['detail'] = item.get('detail')
                    convenient_store_item['id'] = item.get('uid')
                    if item.get("detail_info"):
                        convenient_store_item['tag'] = item.get('detail_info').get('tag')
                        convenient_store_item['type'] = item.get('detail_info').get('type')
                        convenient_store_item['detail_url'] = item.get('detail_info').get('detail_url')
                        convenient_store_item['overall_rating'] = item.get('detail_info').get('overall_rating')
                        convenient_store_item['comment_num'] = item.get('detail_info').get('comment_num')
                        if item.get("detail_info").get("navi_location"):
                            convenient_store_item['navi_lng'] = item.get("detail_info").get("navi_location").get('lng')
                            convenient_store_item['navi_lat'] = item.get("detail_info").get("navi_location").get('lat')
                    yield convenient_store_item
                elif '珠宝' in query:
                    jewelry_store_item = JewelryStoreItem()
                    jewelry_store_item['query'] = query
                    jewelry_store_item['name'] = item.get('name')
                    if item.get('location'):
                        jewelry_store_item['lat'] = item.get("location").get("lat")
                        jewelry_store_item['lng'] = item.get("location").get("lng")
                    jewelry_store_item['address'] = item.get('address')
                    jewelry_store_item['province'] = item.get('province')
                    jewelry_store_item['city'] = item.get('city')
                    jewelry_store_item['area'] = item.get('area')
                    jewelry_store_item['street_id'] = item.get('street_id')
                    jewelry_store_item['telephone'] = item.get('telephone')
                    jewelry_store_item['detail'] = item.get('detail')
                    jewelry_store_item['id'] = item.get('uid')
                    if item.get("detail_info"):
                        jewelry_store_item['tag'] = item.get('detail_info').get('tag')
                        jewelry_store_item['indoor_floor'] = item.get('detail_info').get('indoor_floor')
                        jewelry_store_item['type'] = item.get('detail_info').get('type')
                        jewelry_store_item['detail_url'] = item.get('detail_info').get('detail_url')
                        jewelry_store_item['price'] = item.get('detail_info').get('price')
                        jewelry_store_item['overall_rating'] = item.get('detail_info').get('overall_rating')
                        jewelry_store_item['comment_num'] = item.get('detail_info').get('comment_num')
                        if item.get("detail_info").get("navi_location"):
                            jewelry_store_item['navi_lng'] = item.get("detail_info").get("navi_location").get('lng')
                            jewelry_store_item['navi_lat'] = item.get("detail_info").get("navi_location").get('lat')
                    yield jewelry_store_item

            page_num += 1
            self.logger.debug('parse_poi page_num: {}'.format(page_num))
            print('parse_poi page_num: {}'.format(page_num))
            url = self.base_url.format(query=query, page_num=page_num, bounds=bounds, ak=ak)
            url = quote(url, safe=";/?:@&=+$,", encoding="utf-8")
            self.logger.debug('parse_poi url: {}'.format(url))
            print('parse_poi url: {}'.format(url))
            yield Request(url, callback=self.parse_poi,
                          meta={'query': query, 'page_num': page_num, 'bounds': bounds, 'ak': ak})






