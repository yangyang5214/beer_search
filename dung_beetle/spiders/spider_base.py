# -*- coding: utf-8 -*-
import scrapy
import logging
from urllib.parse import urlparse
import copy


class SpiderBase(scrapy.Spider):
    name = ''
    allowed_domains = []
    start_urls = []
    url = ''
    prod_url = ''

    USER_AGENT = 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    HEADERS = {}

    def __init__(self, prod_url='', **kwargs):
        super(SpiderBase, self).__init__()
        self.prod_url = prod_url

    def scrapy_request(self, url, callback, **kwargs):
        self.HEADERS = {
            'user-agent': self.USER_AGENT
        }
        return scrapy.Request(url=url, callback=callback, **kwargs)

    def is_product_page(self, url):
        return True

    def start_requests(self):
        if self.prod_url:
            if self.is_product_page(self.url):
                yield self.scrapy_request(self.prod_url, callback=self.my_parse)
            elif self.is_top_category_list_page(self.url):
                yield self.scrapy_request(self.prod_url, callback=self.parse_category_page)
            else:
                yield self.scrapy_request(self.prod_url, callback=self.parse_list_page)
        else:
            for url in self.start_urls:
                yield self.scrapy_request(url, callback=self.parse_category_page)

    def is_top_category_list_page(self, url):
        if url in self.start_urls:
            return True
        return False

    def get_category_urls(self, response):
        return []

    def parse_category_page(self, response):
        category_urls = self.get_category_urls(response)
        if category_urls:
            for category_url in category_urls:
                yield self.scrapy_request(
                    category_url,
                    self.parse_list_page,
                    dont_filter=True)

    def my_parse(self, response):
        item = {
            'key': self.get_key(response),
            'url': response.url,
            'image_urls': self.get_image_urls(response)}
        return item

    def get_image_urls(self, response):
        return []

    def get_handle(self, url):
        return urlparse(url).path

    def get_full_url(self, url):
        return ''

    def parse_list_page(self, response):
        product_urls = self.get_product_urls(response)
        if product_urls:
            for url in product_urls:
                if self.is_product_page(url):
                    yield self.scrapy_request(url=url, callback=self.my_parse, dont_filter=True)
            next_page_url = self.get_next_page_url(response)
            if next_page_url:
                yield self.scrapy_request(next_page_url, self.parse_list_page, meta=copy.deepcopy(response.meta))

    def get_url_params(self, url):
        return {}

    def get_next_page_url(self, response):
        return ''

    def get_product_urls(self, response):
        return []

    def get_key(self, response):
        return ''
