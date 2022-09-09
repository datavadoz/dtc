class BaseFetcher:
    __REPO_OWNER__ = 'DataTalksClub'
    __REPO_NAME__ = 'nyc-tlc-data'

    @staticmethod
    def fetch():
        raise NotImplementedError
