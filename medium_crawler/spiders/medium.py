"""Medium Crawler."""
import json
import logging
from datetime import datetime, timedelta

import dateutil.parser as dp
import scrapy

from .. import items


class MediumBase:
    """Mixin for medium spider."""

    def __init__(self, usernames=None, date=None,
                 back=None, urls=None, **kwargs):
        """Pass extra arguments.

        :params: usernames: comma-separated medium usernames.
        :params: date: crawling date (YYYYMMDD).
        :params: back: number of days to be crawled.
        :params: urls: comma-separated url list.
        """
        if date:
            self.start_date = datetime.strptime(date, '%Y%m%d')
        else:
            if back:
                self.start_date = dp.parse(
                    datetime.strftime(
                        datetime.now() - timedelta(days=int(back)), '%Y%m%d'
                    )
                )
            else:
                self.start_date = dp.parse(
                    datetime.strftime(datetime.now(), '%Y%m%d')
                )
        if usernames:
            self.usernames = usernames.strip().split(',')
        else:
            self.usernames = None
        if urls:
            self.urls = urls.strip().split(',')
        else:
            self.urls = None


class MediumPost(MediumBase, scrapy.Spider):
    """Crawl medium post."""

    name = 'medium'

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.pagination_url = (
            '{path}?limit={limit}&to={to}&'
            'source={source}&page={page}'
        )
        self.comment_pagination_url = (
            'https://medium.com{path}?'
            'limit={limit}&to={to}'
        )

    def start_requests(self):
        """Start request."""
        if self.urls:
            for url in self.urls:
                yield scrapy.Request(
                    url=f'{url}?format=json',
                    callback=self.post

                )
        elif self.usernames:
            for username in self.usernames:
                url = f'https://medium.com/@{username}?format=json'
                yield scrapy.Request(
                    url=url,
                    meta={'uid': username},
                    callback=self.parse_links
                )

    def parse_links(self, response, _next=True):
        """Extract links from medium API."""
        obj = json.loads(response.text.replace('])}while(1);</x>', '', 1))
        if response.meta.get('user_id'):
            user_id = response.meta['user_id']
        else:
            user_id = obj['payload']['user']['userId']
            response.meta['user_id'] = user_id
        posts = obj.get('payload', {}).get('references', {}).get('Post')
        if posts:
            for k, v in posts.items():
                updated_time = datetime.fromtimestamp(v['updatedAt'] / 1000)
                if updated_time.date() < self.start_date.date():
                    _next = False
                    break
                if user_id == v['creatorId']:
                    url = (
                        f"https://medium.com/{user_id}/{v['id']}?format=json"
                    )
                    yield scrapy.Request(
                        url=url,
                        meta=response.meta,
                        callback=self.post
                    )
                else:
                    logging.warning('Not this post creator!')
        else:
            logging.warning(f'Unable to find post for {response.meta["uid"]}')

        # paging
        if _next and (
            'payload' in obj and
            'paging' in obj['payload'] and
            'next' in obj['payload']['paging']
        ):
            url = self.pagination_url.format(
                path=obj['payload']['paging']['path'],
                limit=obj['payload']['paging']['next']['limit'],
                to=obj['payload']['paging']['next']['to'],
                source='latest',
                page=obj['payload']['paging']['next']['page']
            )
            yield scrapy.Request(
                url=url,
                meta=response.meta,
                callback=self.parse_links
            )

    def post(self, response):
        """Get medium posts."""
        data = response.text.replace('])}while(1);</x>', '', 1)
        obj = json.loads(data)['payload']
        link = obj['value']['mediumUrl']
        uid = [i[1] for i in obj['references']['User'].items()][0]['username']
        author = [i[1] for i in obj['references']['User'].items()][0]['name']
        author_id = [i[1] for i in obj['references']['User'].items()][0]['userId']  # noqa: E501
        title = obj['value']['title']
        content = '\n'.join([i['text'] for i in obj['value']['content']['bodyModel']['paragraphs']])  # noqa: E501
        comment_count = int(obj['value']['virtuals']['responsesCreatedCount'])
        like_count = int(obj['value']['virtuals']['totalClapCount'])
        created_time = datetime.fromtimestamp(obj['value']['createdAt'] / 1000)
        tag = ','.join([i['name'] for i in obj['value']['virtuals']['tags']])
        post_record = items.ArticleItem(
            uid=uid,
            link=link,
            author=author,
            author_id=author_id,
            poster=author,
            title=title,
            content=content,
            comment_count=comment_count,
            like_count=like_count,
            created_time=created_time,
            article_type='post',
            tag=tag,
        )
        yield post_record
        if comment_count > 0:
            post_id = obj['value']['id']
            response.meta['post_id'] = post_id
            response.meta['post_record'] = post_record
            url = (
                f'https://medium.com/_/api/posts/{post_id}/responsesStream'
            )
            yield scrapy.Request(
                url=url,
                meta=response.meta,
                callback=self.comment
            )

    def comment(self, response):
        """Get medium comments."""
        post_record = response.meta['post_record']
        data = response.text.replace('])}while(1);</x>', '', 1)
        obj = json.loads(data)
        posts = obj.get('payload', {}).get('references', {}).get('Post')
        if posts:
            for post_id, post_item in posts.items():
                if post_id != response.meta['post_id']:
                    post = posts[post_id]
                    author_id = post['creatorId']
                    content = '\n'.join([i['text'] for i in post['previewContent2']['bodyModel']['paragraphs']])  # noqa: E501
                    comment_count = int(post['virtuals']['responsesCreatedCount'])  # noqa: E501
                    like_count = int(post['virtuals']['totalClapCount'])  # noqa: E501
                    created_time = datetime.fromtimestamp(post['createdAt'] / 1000)  # noqa: E501
                    link = f'https://medium.com/{author_id}/{post_id}'
                    comment_record = items.ArticleItem(
                        uid=post_record['uid'],
                        link=link,
                        author_id=author_id,
                        poster=post_record['author'],
                        title=post_record['title'],
                        content=content,
                        comment_count=comment_count,
                        like_count=like_count,
                        created_time=created_time,
                        article_type='comment',
                    )
                    yield scrapy.Request(
                        url=f'{link}?format=json',
                        meta={
                            'comment_record': comment_record,
                            'author_id': author_id
                        },
                        callback=self.get_comment_author_name
                    )

        # paging
        if (
            'payload' in obj and
            'paging' in obj['payload'] and
            'next' in obj['payload']['paging']
        ):
            url = self.comment_pagination_url.format(
                path=obj['payload']['paging']['path'],
                limit=obj['payload']['paging']['next']['limit'],
                to=obj['payload']['paging']['next']['to'],
            )
            yield scrapy.Request(
                url=url,
                meta=response.meta,
                callback=self.comment
            )

    def get_comment_author_name(self, response):
        """Get comment author name."""
        comment_record = response.meta['comment_record']
        author_id = response.meta['author_id']
        data = response.text.replace('])}while(1);</x>', '', 1)
        obj = json.loads(data)
        comment_record['author'] = (
            obj.get('payload', {}).
            get('references', {}).
            get('User').
            get(author_id, {}).
            get('name')
        )
        yield comment_record
