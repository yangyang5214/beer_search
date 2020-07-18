# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.utils.python import to_bytes
import hashlib


class DungBeetlePipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        image_urls = item['image_urls']
        if image_urls:
            for url in image_urls:
                yield Request(url, meta={'item': item})
