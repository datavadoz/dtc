import os
import datetime
import shutil

from src.common.downloader import Downloader


class NycTaxiDataExtractor:
    __download_dir__ = '/tmp'
    __end_point__ = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    __src_files__ = [
        'yellow_tripdata_2019-01.csv.gz',
        'yellow_tripdata_2019-02.csv.gz',
        'yellow_tripdata_2019-03.csv.gz',
        'yellow_tripdata_2019-04.csv.gz',
        'yellow_tripdata_2019-05.csv.gz',
        'yellow_tripdata_2019-06.csv.gz',
    ]

    def __init__(self, download_dir=None):
        self.tmp_dir = None
        self.download_dir = download_dir if download_dir else NycTaxiDataExtractor.__download_dir__

    def __enter__(self):
        self._gen_tmp_dir()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._remove_tmp_dir()

    def _gen_tmp_dir(self):
        if not self.tmp_dir:
            date_str = datetime.datetime.utcnow().strftime('dtc_%Y%m%d%H%M%S')
            self.tmp_dir = os.path.join(self.download_dir, date_str)
            os.mkdir(self.tmp_dir)

    def _remove_tmp_dir(self):
        if self.tmp_dir:
            shutil.rmtree(self.tmp_dir)
            self.tmp_dir = None

    def _gen_download_url(self, file_name):
        return self.__end_point__ + file_name

    def _download_raw_data(self):
        downloader = Downloader(download_dir=self.tmp_dir)
        for file_name in NycTaxiDataExtractor.__src_files__:
            url = self._gen_download_url(file_name)
            downloader.get(url, file_name)

    def extract(self):
        self._gen_tmp_dir()
        self._download_raw_data()
        self._remove_tmp_dir()
