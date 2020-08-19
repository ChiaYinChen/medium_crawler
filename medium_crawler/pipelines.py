"""Scrapy pipelines."""
from datetime import datetime


class DefaultValuesPipeline:
    """Set default values processor."""

    def process_item(self, item, spider):
        """Initialize fields with a default value."""
        for field, value in item.fields.items():
            if 'default' in value:
                item.setdefault(field, value['default'])
        return item


class AutoFetchTime:
    """Generate fetched time."""

    def process_item(self, item, spider):
        item['fetched_time'] = datetime.now()
        return item
