"""Scrapy items."""
from datetime import datetime

import scrapy


class ArticleItem(scrapy.Item):
    """Item for article."""

    uid = scrapy.Field()
    link = scrapy.Field()
    author = scrapy.Field(default=None)
    author_id = scrapy.Field(default=None)
    poster = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field(default=None)
    comment_count = scrapy.Field(default=0)
    like_count = scrapy.Field(default=0)
    created_time = scrapy.Field()
    fetched_time = scrapy.Field(default=datetime.now())
    article_type = scrapy.Field()
    tag = scrapy.Field(default=None)
