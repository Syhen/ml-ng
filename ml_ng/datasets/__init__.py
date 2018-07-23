# -*- coding: utf-8 -*-
"""
create on 2018-07-20 上午11:35

author @heyao
"""
import pandas as pd

from ml_ng.datasets.loader import IMDBLoader as _IMDBLoader


def load_imdb(subsets='all'):
    _loader = _IMDBLoader()
    movie_detail = pd.DataFrame()
    movie_review = pd.DataFrame()
    if subsets == 'all' or subsets == 'detail':
        movie_detail = _loader.load_detail()
    if subsets == 'all' or subsets == 'review':
        movie_review = _loader.load_review()
    return movie_detail, movie_review
