# -*- coding: utf-8 -*-

import scrapy


class IMDBIndexItem(scrapy.Item):
    # url: https://www.imdb.com/chart/top?ref_=nv_mv_250
    # every list
    mid = scrapy.Field()  # item的id
    title = scrapy.Field()  # 不含括号的标题
    full_title = scrapy.Field()  # 整个标题
    url = scrapy.Field()  # item链接
    rank = scrapy.Field()  # 列表排名
    source = scrapy.Field()  # 列表来源
    status = scrapy.Field()
    created_at = scrapy.Field()  # 创建该条数据时间


class IMDBDetailItem(scrapy.Item):
    # url: https://www.imdb.com/title/tt0109830/?pf_rd_m=A2FGELUUNOQJNL&
    # pf_rd_p=e31d89dd-322d-4646-8962-327b42fe94b1&pf_rd_r=MTH5T2P1YQ4YF62JT0A6&
    # pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_12
    # from index
    rank = scrapy.Field()
    source = scrapy.Field()
    mid = scrapy.Field()
    title = scrapy.Field()
    full_title = scrapy.Field()
    year = scrapy.Field()
    url = scrapy.Field()
    runtime = scrapy.Field()
    genres = scrapy.Field()  # 流派
    plot_keywords = scrapy.Field()
    plot_summary = scrapy.Field()
    motion_picture_rating = scrapy.Field()  # 动态影像评级
    released_at = scrapy.Field()
    rating = scrapy.Field()
    rating_users = scrapy.Field()
    folder = scrapy.Field()
    video_url = scrapy.Field()
    director = scrapy.Field()
    writer = scrapy.Field()
    stars = scrapy.Field()
    language = scrapy.Field()
    country = scrapy.Field()
    filming_locations = scrapy.Field()
    budget = scrapy.Field()
    worldwide_gross = scrapy.Field()
    sound_mix = scrapy.Field()
    color = scrapy.Field()
    aspect_ratio = scrapy.Field()  # 宽高比
    created_at = scrapy.Field()


class IMDBReviewItem(scrapy.Item):
    # url: https://www.imdb.com/title/tt0109830/reviews/_ajax?ref_=undefined&paginationKey={key}
    # key from Load More element
    rwid = scrapy.Field()  # 评论id
    uid = scrapy.Field()
    mid = scrapy.Field()
    uname = scrapy.Field()
    is_spoilers = scrapy.Field()
    review_title = scrapy.Field()
    review_body = scrapy.Field()
    review_url = scrapy.Field()
    rating = scrapy.Field()
    released_at = scrapy.Field()  # 评论发布时间
    created_at = scrapy.Field()  # item创建时间
