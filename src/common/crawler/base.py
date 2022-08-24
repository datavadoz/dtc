class BaseCrawler:
    __REPO_OWNER__ = 'DataTalksClub'
    __REPO_NAME__ = 'nyc-tlc-data'

    @staticmethod
    def crawl():
        raise NotImplementedError
