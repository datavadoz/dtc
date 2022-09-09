import os

import requests
from tqdm import tqdm


class Downloader:
    __download_dir__ = '/tmp/'

    def __init__(self, download_dir=None):
        self.download_dir = download_dir if download_dir else Downloader.__download_dir__

    def get(self, url, file_name):
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            error_code = response.status_code
            error_text = response.reason
            print(f'Failed to download {file_name} due to {error_code} ({error_text})')
            return False

        block_size = 1024
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        out_file = os.path.join(self.download_dir, file_name)

        print(f'Downloading {out_file}...')
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc=file_name)
        with open(out_file, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

        progress_bar.close()
