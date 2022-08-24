import requests

from src.common.crawler import BaseCrawler


class AssetCrawler(BaseCrawler):

    @staticmethod
    def crawl():
        url = 'https://api.github.com/repos/{0}/{1}/releases'.format(BaseCrawler.__REPO_OWNER__,
                                                                     BaseCrawler.__REPO_NAME__)
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
