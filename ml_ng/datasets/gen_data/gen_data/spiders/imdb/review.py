# -*- coding: utf-8 -*-
"""
create on 2018-07-22 下午4:02

author @heyao
"""
from datetime import datetime

import pymongo
from scrapy import Spider, Request

from gen_data.items import IMDBReviewItem


class IMDBReviewSpider(Spider):
    name = 'imdb_review'

    def __init__(self, name, **kwargs):
        super(IMDBReviewSpider, self).__init__(name, **kwargs)
        _client = pymongo.MongoClient(kwargs['mongo_uri'])
        self.mongo_db = _client[kwargs['mongo_db_name']]
        if kwargs['mongo_auth']:
            self.mongo_db.authenticate(**kwargs['mongo_auth'])

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        settings = crawler.settings
        return cls(cls.name, mongo_uri=settings.get("MONGO_URI"), mongo_db_name=settings.get("MONGO_DB_NAME"),
                   mongo_auth=settings.get("MONGO_AUTH"))

    def start_requests(self):
        param = {
            'mid': 1,
            '_id': 0
        }
        data = self.mongo_db['movie_detail'].find({}, param)
        for i in data:
            yield Request(
                'https://www.imdb.com/title/{mid}/reviews?ref_=tt_ov_rt'.format(mid=i['mid']),
                meta={'info': i},
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
        info = response.meta['info']
        reviews = response.xpath('//div[@class="lister-list"]/div')
        for review in reviews:
            item = IMDBReviewItem()
            item.update(info)
            item['rwid'] = review.xpath('./@data-review-id').extract()[0]
            rating = review.xpath('.//span[@class="rating-other-user-rating"]/span[1]/text()').extract()
            if not rating:
                continue
            item['rating'] = int(rating[0])
            item['review_title'] = review.xpath('.//div[@class="lister-item-content"]/a/text()').extract()[0].strip()
            item['review_body'] = review.xpath('.//div[@class="content"]/div/text()').extract()[0].strip()
            rw_url = response.urljoin(review.xpath('.//div[@class="lister-item-content"]/a/@href').extract()[0].strip())
            item['review_url'] = rw_url
            user_url = review.xpath('.//span[@class="display-name-link"]/a/@href').extract()[0]
            item['uid'] = user_url.split('/')[2]
            item['uname'] = review.xpath('.//span[@class="display-name-link"]/a/text()').extract()[0]
            item['is_spoilers'] = bool(review.xpath('.//span[@class="spoiler-warning"]').extract()) * 1
            released_at = review.xpath('.//span[@class="review-date"]/text()').extract()[0]
            item['released_at'] = datetime.strptime(released_at, '%d %B %Y')
            item['created_at'] = datetime.now()
            yield item
        has_move = response.xpath('//div[@class="load-more-data"]')
        if has_move.extract():
            key = has_move.xpath('./@data-key').extract()[0]
            url_base = 'https://www.imdb.com/title/{mid}/reviews/_ajax?ref_=undefined&paginationKey={key}'
            url = url_base.format(mid=info['mid'], key=key)
            yield Request(
                url,
                meta={'info': info},
                callback=self.parse,
                dont_filter=True
            )
