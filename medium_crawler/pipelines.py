"""Scrapy pipelines."""


class DefaultValuesPipeline(object):
    """Set default values processor."""

    def process_item(self, item, spider):
        """Initialize fields with a default value."""
        for field, value in item.fields.items():
            if 'default' in value:
                item.setdefault(field, value['default'])
        return item
