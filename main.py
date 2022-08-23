from src.common.extractor import NycTaxiDataExtractor


if __name__ == '__main__':
    with NycTaxiDataExtractor() as extractor:
        extractor.extract()
