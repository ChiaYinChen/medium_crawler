"""Test for medium."""
import json
import logging
from datetime import date, datetime

import pytest
from scrapy.http import HtmlResponse, Request

from medium_crawler.spiders.medium import MediumPost


logger = logging.getLogger(__name__)


@pytest.mark.usefixtures('betamax_session')
class TestMediumSpider:
    """Test case for MediumPost spider."""

    medium_spider = MediumPost(date='20200301', usernames='chiayinchen')

    def mock_scrapy_response(
        self, betamax_session: object, url: str
    ) -> HtmlResponse:
        """Mock scrapy response by betamax.

        Args:
            betamax_session (object): betamax_session object
            url (str): request's url

        Returns:
            HtmlResponse: scrapy html response
        """
        response = betamax_session.get(url)
        request = Request(url)
        return HtmlResponse(
            url=url,
            body=response.content,
            request=request
        )

    def test_parse_links(self, betamax_session):
        """Test parse links."""
        response = self.mock_scrapy_response(
            betamax_session=betamax_session,
            url='https://medium.com/@chiayinchen?format=json'
        )
        obj = json.loads(response.text.replace('])}while(1);</x>', '', 1))
        user_id = obj['payload']['user']['userId']
        posts = obj.get('payload', {}).get('references', {}).get('Post')
        stop_next_or_request = self.medium_spider.parse_links_logic(
            response=response,
            posts=posts,
            user_id=user_id
        )
        self._test_parse_links_logic(stop_next_or_request)
        self._test_parse_links_paging(obj)

    def _test_parse_links_logic(self, stop_next_or_request):
        """Test parse_links_logic."""
        item_links = []
        _next = True
        for item in stop_next_or_request:
            if isinstance(item, Request):
                item_links.append(item)
            else:
                _next = item
        logger.debug(f'links: {[i.url for i in item_links]}')
        logger.debug(f'Total get {len(item_links)} links in this page.')
        assert len(item_links) > 0
        assert isinstance(_next, bool)
        assert _next is False

    def _test_parse_links_paging(self, obj):
        """Test parse_links pagination url."""
        pagination_url = self.convert_to_pagination_url(obj)
        logger.debug(f"User post's pagination url: {pagination_url}")
        assert isinstance(pagination_url, str)
        assert pagination_url[:4] == 'http'

    def convert_to_pagination_url(self, obj):
        """Convert to pagination url."""
        url = self.medium_spider.pagination_url.format(
            path=obj['payload']['paging']['path'],
            limit=obj['payload']['paging']['next']['limit'],
            to=obj['payload']['paging']['next']['to'],
            source='latest',
            page=obj['payload']['paging']['next']['page']
        )
        return url

    def test_parse_post_item(self, betamax_session):
        """Test parse post item."""
        response = self.mock_scrapy_response(
            betamax_session=betamax_session,
            url='https://medium.com/8045c82962e2/625a07c75000?format=json'
        )
        data = response.text.replace('])}while(1);</x>', '', 1)
        obj = json.loads(data)['payload']
        item = self.medium_spider.parse_post_item(post=obj)
        logger.debug(item)
        assert isinstance(item['title'], str)
        assert len(item['title']) > 0, 'Article title is empty string.'
        assert isinstance(item['created_time'], (datetime, date))
        assert isinstance(item['author'], str)
        assert len(item['author']) > 0, 'Article author is empty string.'
        assert isinstance(item['author_id'], str)
        assert item['author_id'] == '8045c82962e2'
        assert isinstance(item['content'], str)
        assert len(item['content']) > 0, 'Article content is empty string.'
        assert isinstance(item['comment_count'], int)
        assert item['comment_count'] > 0
        assert isinstance(item['like_count'], int)
        assert item['like_count'] > 0
        assert item['link'][:4] == 'http'
        assert isinstance(item['tag'], str)
        assert len(item['tag']) > 0, 'Article tag is empty string.'
