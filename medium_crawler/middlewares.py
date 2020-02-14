"""Scrapy middlewares."""
import logging
import os
import random
from distutils.util import strtobool


# configurable environment variables
PROXY = os.environ.get('PROXY', 'http://127.0.0.1:8787')
PROXY_ENABLED = strtobool(os.environ.get('PROXY_ENABLED', 'FALSE'))


class ProxyMiddleware(object):
    """HTTP proxy middleware."""

    def __init__(self, proxy_depth=None):
        """Set proxy depth."""
        self.proxy_depth = proxy_depth

    @classmethod
    def from_crawler(cls, crawler):
        """Scrapy's `from_crawler` method."""
        return cls(
            proxy_depth=crawler.settings.getint('PROXY_DEPTH')
        )

    def process_request(self, request, spider):
        """Scrapy's `process_request` method."""
        if self.use_proxy(request):
            logging.debug('using proxy.')
            request.meta['proxy'] = PROXY

    def use_proxy(self, request):
        """Make HTTP request without proxy when depth >= 3."""
        # if environ variable "PROXY_ENABLED" set to False, disable proxy
        if PROXY_ENABLED == 0:
            return False
        if 'depth' in request.meta and int(request.meta['depth']) == 0:
            return False
        elif 'depth' in request.meta:
            self.proxy_depth = request.meta['depth']
        if self.proxy_depth:
            i = self.proxy_depth
        else:
            i = random.randint(1, 10)
        return i >= 3  # make default value configurable
