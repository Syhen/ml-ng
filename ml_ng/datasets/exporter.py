# -*- coding: utf-8 -*-
"""
create on 2018-07-23 上午11:32

author @heyao
"""
import os

import pandas as pd

from ml_ng.default import base_path as default_base_path


class IMDBExporter(object):
    def __init__(self, mongo_db, base_path=None, gzip=None):
        self.mongo_db = mongo_db
        self.base_path = base_path or os.path.join(default_base_path, 'datasets/data')
        self.gzip = 'gzip' if gzip else None

    def _query_data(self, collection, filters=None, params=None, iterable=False, skip=0, limit=0):
        filters = filters or {}
        params = params or {}
        params.update({'_id': 0, 'created_at': 0})
        data = self.mongo_db[collection].find(filters, params).skip(skip).limit(limit)
        if iterable:
            return data
        return list(data)

    def get_filename(self, name_format):
        # dt = datetime.strftime(datetime.now(), '%Y%m%d')
        dt = ""
        return name_format % dt

    def _export_flle(self, df, filename, compression, filetype='csv'):
        if filetype == 'csv':
            if compression:
                filename += '.gz'
            return df.to_csv(filename, compression=compression)
        if filetype == 'excel':
            return df.to_excel(filename)
        return False

    def query_detail(self, filters=None, params=None, iterable=False, skip=0, limit=0):
        params = params or {'summary': 0}
        return self._query_data('movie_detail', filters, params, iterable, skip, limit)

    def export_detail(self, movie_ids=None, params=None, skip=0, limit=0, columns=None):
        filters = {'_id': {'$in': movie_ids}} if movie_ids else {}
        data = self.query_detail(filters, params, iterable=False, skip=skip, limit=limit)
        df = pd.DataFrame(data)
        for column in df.columns:
            dtype = type(df.loc[0, column])
            if 'list' not in str(dtype):
                continue
            df[column] = df[column].apply(lambda x: '|'.join(x))
        if columns:
            columns = list(set(columns) & set(df.columns))
            df = df[columns]
        filename = self.get_filename('movie_detail%s.csv')
        self._export_flle(df, os.path.join(self.base_path, filename), compression=self.gzip, filetype='csv')
        return df.to_dict('records')

    def query_review(self, filters=None, params=None, iterable=False, skip=0, limit=0):
        return self._query_data('movie_review', filters, params, iterable, skip, limit)

    def export_review(self, movie_ids=None, params=None, skip=0, limit=0, columns=None):
        filters = {'_id': {'$in': movie_ids}} if movie_ids else {}
        data = self.query_review(filters, params, iterable=False, skip=skip, limit=limit)
        df = pd.DataFrame(data)
        if columns:
            columns = list(set(columns) & set(df.columns))
            df = df[columns]
        filename = self.get_filename('movie_review%s.csv')
        self._export_flle(df, os.path.join(self.base_path, filename), compression=self.gzip, filetype='csv')
        return df.to_dict('records')


if __name__ == '__main__':
    import pymongo

    con = pymongo.MongoClient()
    db = con['coursera_ml_ng']
    imdb_exporter = IMDBExporter(db, gzip=True)
    data = imdb_exporter.export_detail()
    data = imdb_exporter.export_review()
