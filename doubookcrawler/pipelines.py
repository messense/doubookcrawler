# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from doubookcrawler.models import Book, Rating
from doubookcrawler.items import BookItem, CommentItem


class DoubookCrawlerPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, BookItem):
            Book.upsert_book(item)
        elif isinstance(item, CommentItem):
            Rating.upsert_rating(item)
        return item
