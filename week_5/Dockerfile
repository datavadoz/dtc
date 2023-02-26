FROM apache/spark-py:v3.3.2

USER 0

RUN apt-get -y update && apt-get -y install wget

RUN wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhvhv/fhvhv_tripdata_2021-06.csv.gz \
    && wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv \
    && gzip -d fhvhv_tripdata_2021-06.csv.gz

USER 185

