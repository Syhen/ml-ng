# -*- coding: utf-8 -*-
"""
create on 2018-07-23 下午6:52

author @heyao
"""
import os

import pandas as pd

from ml_ng.default import base_path as default_base_path


class IMDBLoader(object):
    def __init__(self, base_path=None):
        self.base_path = base_path or os.path.join(default_base_path, 'datasets/data')

    def load_detail(self):
        data = pd.read_csv(os.path.join(self.base_path, 'movie_detail.csv.gz'))
        return data

    def load_review(self):
        data = pd.read_csv(os.path.join(self.base_path, 'movie_review.csv.gz'))
        return data
