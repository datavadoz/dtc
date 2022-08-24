from src.common.extractor import Extractor


if __name__ == '__main__':
    with Extractor() as extractor:
        extractor.extract()
