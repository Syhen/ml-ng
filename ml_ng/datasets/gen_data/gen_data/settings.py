# -*- coding: utf-8 -*-

BOT_NAME = 'gen_data'

SPIDER_MODULES = ['gen_data.spiders']
NEWSPIDER_MODULE = 'gen_data.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 32
# DOWNLOAD_DELAY = 3
# COOKIES_ENABLED = False

ITEM_PIPELINES = {
}
