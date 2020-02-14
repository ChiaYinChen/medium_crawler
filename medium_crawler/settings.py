"""Scrapy settings."""
import os
BOT_NAME = 'medium_crawler'
SPIDER_MODULES = ['medium_crawler.spiders']
NEWSPIDER_MODULE = 'medium_crawler.spiders'

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 0.3
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 5.0
AUTOTHROTTLE_DEBUG = True
RETRY_HTTP_CODES = [500, 503, 504, 400, 408]
RETRY_TIMES = 10

ITEM_PIPELINES = {
    'medium_crawler.pipelines.DefaultValuesPipeline': 100,
}

DOWNLOADER_MIDDLEWARES = {
    'medium_crawler.middlewares.ProxyMiddleware': 100,
}

PROXY_DEPTH = os.environ.get('PROXY_DEPTH', 0)
