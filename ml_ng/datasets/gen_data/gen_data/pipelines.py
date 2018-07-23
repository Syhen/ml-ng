# -*- coding: utf-8 -*-

import pymongo


class BaseMongodbPipeline(object):
    def __init__(self, mongo_uri, mongo_db_name, mongo_auth):
        self.mongo_uri = mongo_uri
        self.mongo_db_name = mongo_db_name
        self.mongo_auth = mongo_auth
        self._client = None
        self.mongo_db = None

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.get("MONGO_URI"), settings.get("MONGO_DB_NAME"), settings.get("MONGO_AUTH"))

    def open_spider(self, spider):
        self._client = pymongo.MongoClient(self.mongo_uri)
        self.mongo_db = self._client[self.mongo_db_name]
        if self.mongo_auth:
            self.mongo_db.authenticate(**self.mongo_auth)

    def close_spider(self, spider):
        if self._client:
            self._client.close()


class IMDBIndexPipeline(BaseMongodbPipeline):
    def process_item(self, item, spider):
        if spider.name != 'imdb_index':
            return item
        self.mongo_db['movie_index'].update_one({'_id': item['mid']}, {'$setOnInsert': item}, upsert=True)
        return item


class IMDBDetailPipeline(BaseMongodbPipeline):
    def process_item(self, item, spider):
        if spider.name != 'imdb_detail':
            return item
        self.mongo_db['movie_detail'].update_one({'_id': item['mid']}, {'$set': item}, upsert=True)
        self.mongo_db['movie_index'].update_one({'_id': item['mid']}, {'$set': {'status': 1}})
        return item


class IMDBReviewPipeline(BaseMongodbPipeline):
    def process_item(self, item, spider):
        if spider.name != 'imdb_review':
            return item
        self.mongo_db['movie_review'].update_one({'_id': item['rwid']}, {'$set': item}, upsert=True)
        return item
