# -*- coding: utf-8 -*-
"""
create on 2018-07-20 下午5:09

author @heyao
"""
from datetime import datetime

import pymongo
from scrapy import Spider, Request

from gen_data.items import IMDBDetailItem


class IMDBDetailSpider(Spider):
    name = 'imdb_detail'

    def __init__(self, name, **kwargs):
        super(IMDBDetailSpider, self).__init__(name, **kwargs)
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
            '_id': 0,
            'status': 0,
            'created_at': 0
        }
        data = self.mongo_db['movie_index'].find({'status': 0}, param)
        for i in data:
            yield Request(
                i['url'],
                meta={'info': i},
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
        def extract_h4_key_text(key, is_a=True, index=None):
            if is_a:
                data = response.xpath('//div[contains(./h4/., "' + key + '")]/a/text()').extract()
                if data:
                    if index is not None:
                        return data[index].strip()
                    return [p.strip() for p in data]
                return ""
            if index is not None:
                data = response.xpath('//div[contains(./h4/., "' + key + '")]//text()').extract()
                if data:
                    return data[index].strip()
                return ""
            data = response.xpath('//div[contains(./h4/., "' + key + '")]/text()').extract()
            if data:
                return [p.strip() for p in data]
            return ""

        info = response.meta['info']
        item = IMDBDetailItem()
        item.update(info)
        item['released_at'] = response.xpath('//div[@class="subtext"]/a[last()]/meta/@content').extract()[0]
        item['year'] = item['released_at'].split('-')[0]
        item['runtime'] = response.xpath('//div[@class="subtext"]/time/@datetime').extract()[0][2:]
        genres_data = response.xpath('//div[@class="subtext"]/a')[:-1]
        item['genres'] = [genres.xpath('./span/text()').extract()[0] for genres in genres_data]
        item['plot_keywords'] = response.xpath('//div[contains(., "Plot Keywords:")]/a/span/text()').extract()
        summaries = response.xpath('//span[@itemprop="description"]/text()').extract()
        item['plot_summary'] = ''.join(p.strip() for p in summaries)
        picture_rating = response.xpath('//div[contains(./h4/., "Motion Picture Rating")]/span[1]/text()')
        item['motion_picture_rating'] = picture_rating.extract_first('')
        item['rating'] = float(response.xpath('//span[@itemprop="ratingValue"]/text()').extract()[0])
        rating_users = response.xpath('//span[@itemprop="ratingCount"]/text()').extract()[0].replace(',', '')
        item['rating_users'] = int(rating_users)
        item['folder'] = response.xpath('//div[@class="poster"]/a/img/@src').extract()[0]
        item['video_url'] = response.xpath('//div[@class="slate"]/a/img/@src').extract_first('')
        item['director'] = response.xpath('//span[@itemprop="director"]/a/span/text()').extract()
        item['writer'] = response.xpath('//span[@itemprop="creator"]/a/span/text()').extract()
        item['stars'] = response.xpath('//span[@itemprop="actors"]/a/span/text()').extract()
        item['language'] = extract_h4_key_text("Language:", index=0)
        item['country'] = extract_h4_key_text("Country:", index=0)
        item['filming_locations'] = extract_h4_key_text('Filming Locations:', index=0)
        item['budget'] = extract_h4_key_text("Budget:", is_a=False, index=2)
        item['worldwide_gross'] = extract_h4_key_text("Cumulative Worldwide Gross:", is_a=False, index=2)
        item['sound_mix'] = extract_h4_key_text("Sound Mix:")
        item['color'] = extract_h4_key_text("Color:")
        item['aspect_ratio'] = extract_h4_key_text("Aspect Ratio:", is_a=False, index=2)
        item['created_at'] = datetime.now()
        yield item
