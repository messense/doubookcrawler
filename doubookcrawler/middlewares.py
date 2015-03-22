# -*- coding: utf-8 -*-
import urllib
try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse

from scrapy import log
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware as _RetryMiddleware


class RetryMiddleware(_RetryMiddleware):

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1

        if retries <= self.max_retry_times:
            log.msg(format="Retrying %(request)s (failed %(retries)d times): %(reason)s",
                    level=log.DEBUG, spider=spider, request=request, retries=retries, reason=reason)

            if request.url.startswith('http://www.douban.com/misc/sorry?original-url='):
                query = urlparse.urlsplit(request.url).query
                query_parsed = urlparse.parse_qs(query)
                url = urllib.unquote(query_parsed['original-url'][0])
            else:
                url = request.url
            retryreq = request.replace(url=url)
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust

            return retryreq
        else:
            log.msg(format="Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                    level=log.DEBUG, spider=spider, request=request, retries=retries, reason=reason)
