# -*- coding: utf-8 -*-
try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse

import scrapy
from scrapy import Request
from scrapy import log

from doubookcrawler.items import BookItem, CommentItem


class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["book.douban.com"]
    start_urls = (
        'http://book.douban.com/tag/',
    )

    def parse(self, response):
        tags = response.xpath('//table[@class="tagCol"]/tbody/tr/td/a/@href')
        for tag in tags.extract():
            url = urlparse.urljoin(self.start_urls[0], tag)
            yield Request(url, callback=self.parse_tag)
            if self.settings['DEBUG']:
                break

    def parse_tag(self, response):
        books = response.xpath('//ul/li[@class="subject-item"]/div[@class="info"]')
        for book in books:
            url = book.xpath('h2/a/@href').extract()
            title = book.xpath('h2/a/text()').extract()
            pub = book.xpath('div[@class="pub"]/text()').extract()
            rating = book.xpath('div/span[@class="rating_nums"]/text()').extract()
            if not (url and title and pub and rating):
                self.log('Bad data for book, ignore', log.WARNING)
                continue

            url_path = urlparse.urlsplit(url[0].strip()).path
            if url_path.endswith('/'):
                url_path = url_path[:-1]
            book_id = url_path.split('/')[-1]
            book_pub = pub[0].strip().split('/')

            book_item = BookItem()
            book_item['id'] = int(book_id)
            book_item['title'] = title[0].strip()
            book_item['author'] = book_pub[0].strip()
            book_item['rating'] = float(rating[0])
            yield book_item

            comments_url = urlparse.urljoin(url[0], 'comments/')
            yield Request(comments_url, callback=self.parse_comments)

            if self.settings['DEBUG']:
                break

        pager = response.xpath('//div[@class="paginator"]')
        if not pager:
            self.log('No more pages, return', log.INFO)
            return
        next_page = pager.xpath('span[@class="next"]/a/@href').extract()[0]
        next_url = urlparse.urljoin('http://book.douban.com', next_page)
        if not self.settings['DEBUG']:
            yield Request(next_url, callback=self.parse_tag)

    def parse_comments(self, response):
        rating_classes = {
            'allstar50': 5,
            'allstar40': 4,
            'allstar30': 3,
            'allstar20': 2,
            'allstar10': 1,
        }
        url_path = urlparse.urlsplit(response.url).path
        book_id = url_path.split('/')[2]
        comments = response.xpath('//ul/li[@class="comment-item"]/h3')
        for comment in comments:
            vote = comment.xpath('span[@class="comment-vote"]/span/text()').extract()
            info = comment.xpath('span[@class="comment-info"]')
            user = info.xpath('a/text()').extract()
            rating = info.xpath('span[1]/@class').extract()
            if not (vote and user and rating):
                self.log('Bad data for comment, ignore', log.WARNING)
                continue

            vote = int(vote[0])
            user = user[0].strip()
            rating = rating[0].replace('user-stars', '').replace('rating', '')
            rating = rating.strip()
            rating_num = rating_classes.get(rating, 0)
            if rating_num == 0:
                self.log('Bad rating 0 for comment, ignore', log.INFO)
                continue

            comment_item = CommentItem()
            comment_item['book_id'] = int(book_id)
            comment_item['user'] = user
            comment_item['rating'] = rating_num
            comment_item['vote'] = vote
            yield comment_item

            if self.settings['DEBUG']:
                break

        pager = response.xpath('//ul[@class="comment-paginator"]/li[3]/a/@href')
        if not pager:
            return
        next_page = pager.extract()[0]
        next_url = urlparse.urljoin(response.url, next_page)
        if not self.settings['DEBUG']:
            yield Request(next_url, callback=self.parse_comments)
