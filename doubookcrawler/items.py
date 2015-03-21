# -*- coding: utf-8 -*-
import scrapy


class BookItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    rating = scrapy.Field()


class CommentItem(scrapy.Item):
    book_id = scrapy.Field()
    user = scrapy.Field()
    rating = scrapy.Field()
    vote = scrapy.Field()
