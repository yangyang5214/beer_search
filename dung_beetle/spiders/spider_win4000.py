# -*- coding: utf-8 -*-
from spider_base import SpiderBase


class SpiderWin4000(SpiderBase):
    name = 'win4000'
    allowed_domains = ['http://www.win4000.com']
    start_urls = ['http://www.win4000.com/meinvtag4_1.html']

    id_prefix = 'win4000_'

    def is_product_page(self, url):
        if 'tag' in url:
            return False
        return True

    def start_requests(self):
        for url in self.start_urls:
            yield self.scrapy_request(url, callback=self.parse_list_page)

    def get_product_urls(self, response):
        return response.xpath("//div[@class='Left_bar']//ul[@class='clearfix']//li/a/@href").extract()

    def get_key(self, response):
        handle = self.get_handle(response.url)
        return self.id_prefix + handle[handle.index('/')+1:handle.index('.')]

    def get_image_urls(self, response):
        return [
            url[:url.index('_')] + '.jpg'
            for url in response.xpath('//ul[contains(@id,"scroll")]//a/img/@data-original').extract()
        ]
