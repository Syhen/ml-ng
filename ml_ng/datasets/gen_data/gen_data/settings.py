# -*- coding: utf-8 -*-

BOT_NAME = 'gen_data'

SPIDER_MODULES = ['gen_data.spiders']
NEWSPIDER_MODULE = 'gen_data.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 32
# DOWNLOAD_DELAY = 3
# COOKIES_ENABLED = False

ITEM_PIPELINES = {
    'gen_data.pipelines.IMDBIndexPipeline': 300,
    'gen_data.pipelines.IMDBDetailPipeline': 310,
    'gen_data.pipelines.IMDBReviewPipeline': 320,
}

# mongodb
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'coursera_ml_ng'
MONGO_AUTH = {}
