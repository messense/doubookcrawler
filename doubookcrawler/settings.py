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

DEBUG = False

CONCURRENT_ITEMS = 300
CONCURRENT_REQUESTS = 5

ITEM_PIPELINES = {
    'doubookcrawler.pipelines.DoubookCrawlerPipeline': 300,
}

# Retry many times since proxies often fail
RETRY_TIMES = 10
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 90,
    'doubookcrawler.randomproxy.RandomProxy': 100,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
}

# Proxy list containing entries like
# http://host1:port
# http://username:password@host2:port
# http://host3:port
# ...
PROXY_LIST = '/Users/messense/Projects/doubookcrawler/proxy.txt'

db_conn = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='',
    db='doubook',
    charset='utf8',
)
