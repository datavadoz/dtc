import datetime
import os
import shutil

from src.fe.downloader import Downloader
from src.fe.fetcher import AssetFetcher


class Extractor:
    __download_dir__ = '/tmp'

    def __init__(self, download_dir=None):
        self.root_dir = None
        self.download_dir = download_dir if download_dir else Extractor.__download_dir__

    def __enter__(self):
        self._gen_root_dir()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._remove_root_dir()

    def _gen_root_dir(self):
        if not self.root_dir:
            date_str = datetime.datetime.utcnow().strftime('dtc_%Y%m%d%H%M%S')
            self.root_dir = os.path.join(self.download_dir, date_str)
            os.mkdir(self.root_dir)

    def _remove_root_dir(self):
        if self.root_dir:
            shutil.rmtree(self.root_dir)
            self.root_dir = None

    def _gen_tag_dir(self, tag_name):
        if self.root_dir:
            tag_dir = os.path.join(self.root_dir, tag_name)
            os.mkdir(tag_dir)
            return tag_dir

    def _download_raw_data(self):
        print('Getting GitHub download raw data link...')
        download_info = AssetFetcher.fetch()
        for tag_name, download_file_info in download_info.items():
            tag_dir = self._gen_tag_dir(tag_name)
            downloader = Downloader(download_dir=tag_dir)
            for file_name, download_url in download_file_info.items():
                downloader.get(download_url, file_name)

    def extract(self):
        self._gen_root_dir()
        self._download_raw_data()
        self._remove_root_dir()
