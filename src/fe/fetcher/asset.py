import requests

from src.fe.fetcher import BaseFetcher


class AssetFetcher(BaseFetcher):

    @staticmethod
    def fetch():
        url = 'https://api.github.com/repos/{0}/{1}/releases'.format(BaseFetcher.__REPO_OWNER__,
                                                                     BaseFetcher.__REPO_NAME__)
        response = requests.get(url)
        assets_urls = {
            item['tag_name']: item['assets_url']
            for item in response.json()
        }

        download_info = {}
        for tag_name, url in assets_urls.items():
            response = requests.get(url)
            browser_download_urls = {
                item['name']: item['browser_download_url']
                for item in response.json()
            }
            download_info.update({tag_name: browser_download_urls})

        return download_info
