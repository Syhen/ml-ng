# -*- coding: utf-8 -*-
"""
create on 2018-07-20 下午2:19

author @heyao
"""
from datetime import datetime

from scrapy import Spider

from gen_data.items import IMDBIndexItem


class IMDBNvMv250IndexSpider(Spider):
    name = 'imdb_index'

    start_urls = ['https://www.imdb.com/chart/top?ref_=nv_mv_250']

    def parse(self, response):
        movie_list = response.xpath('//tbody[@class="lister-list"]/tr')
        for i, movie in enumerate(movie_list, 1):
            item = IMDBIndexItem()
            item['url'] = response.urljoin(movie.xpath('./td[2]/a/@href').extract()[0])
            item['mid'] = item['url'].split('/')[-2]
            item['title'] = movie.xpath('./td[2]/a/text()').extract()[0]
            item['full_title'] = item['title'] + ' ' + movie.xpath('./td[2]/span/text()').extract()[0]
            item['rank'] = i
            item['source'] = 'nv_mv_250'
            item['status'] = 0
            item['created_at'] = datetime.now()
            yield item
