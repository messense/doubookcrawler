# -*- coding: utf-8 -*-
import scrapy


class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["book.douban.com"]
    start_urls = (
        'http://book.douban.com/tag/',
    )

    def parse(self, response):
        pass
