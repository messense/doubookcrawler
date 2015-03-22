# -*- coding: utf-8 -*-

# Scrapy settings for doubookcrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import MySQLdb

BOT_NAME = 'doubookcrawler'

SPIDER_MODULES = ['doubookcrawler.spiders']
NEWSPIDER_MODULE = 'doubookcrawler.spiders'

USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/40.0.2214.94 Safari/537.36')

DEBUG = True

CONCURRENT_ITEMS = 300
CONCURRENT_REQUESTS = 2

db_conn = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='',
    db='doubook',
    charset='utf8',
)
