# Week 3

## Overview
This week mainly interacts with BigQuery so no more Python code.

## Setup

Create an external table of FHV 2019:
```
CREATE OR REPLACE EXTERNAL TABLE `dtc-de-375513.dezoomcamp.external_fhv_2019`
OPTIONS (
  format = 'CSV',
  uris = ['gs://dtc-week-3/fhv_tripdata_2019-*.csv.gz']
)
```

Create a new non-partition table from the created external table:
```
CREATE OR REPLACE TABLE `dtc-de-375513.dezoomcamp.fhv_2019` AS
SELECT * FROM `dtc-de-375513.dezoomcamp.external_fhv_2019`
```

## Homework
### Question 1: What is the count for fhv vehicle records for year 2019?
```
SELECT COUNT(*)
FROM `dezoomcamp.fhv_2019`
```
**Answer**: 
> 43,244,696

### Question 2: Write a query to count the distinct number of affiliated_base_number for the entire dataset on both the tables. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
```
-- This query will process 0 B when run.
SELECT DISTINCT `Affiliated_base_number`
FROM `dtc-de-375513.dezoomcamp.external_fhv_2019`;

-- This query will process 317.94 MB when run.
SELECT DISTINCT `Affiliated_base_number`
from `dtc-de-375513.dezoomcamp.fhv_2019`;
```
**Answer**:
> 0 MB for the External Table and 317.94MB for the BQ Table

### Question 3: How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?
```
SELECT COUNT(*)
FROM `dtc-de-375513.dezoomcamp.fhv_2019`
WHERE PUlocationID IS NULL AND DOlocationID IS NULL;
```
**Answer**:
> 717,748

## Question 4: What is the best strategy to optimize the table if query always filter by pickup_datetime and order by affiliated_base_number?
**Answer**:
> Partition by pickup_datetime Cluster on affiliated_base_number

## Question 5: Implement the optimized solution you chose for question 4. Write a query to retrieve the distinct affiliated_base_number between pickup_datetime 2019/03/01 and 2019/03/31 (inclusive). Use the BQ table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values? Choose the answer which most closely matches.
```
-- Create partitioned and clustered FHV 2019 table
CREATE OR REPLACE TABLE `dtc-de-375513.dezoomcamp.partitioned_and_clustered_fhv_2019`
PARTITION BY DATE(pickup_datetime)
CLUSTER BY Affiliated_base_number AS
  SELECT * FROM `dtc-de-375513.dezoomcamp.fhv_2019`;

-- This query will process 647.87 MB when run.
SELECT DISTINCT Affiliated_base_number
FROM `dtc-de-375513.dezoomcamp.fhv_2019`
WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';

-- This query will process 23.05 MB when run.
SELECT DISTINCT Affiliated_base_number
FROM `dtc-de-375513.dezoomcamp.partitioned_and_clustered_fhv_2019`
WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';
```
**Answer**:
> 647.87 MB for non-partitioned table and 23.06 MB for the partitioned table

## Question 6: Where is the data stored in the External Table you created?
**Answer**:
> GCP Bucket

## Question 7: It is best practice in Big Query to always cluster your data:
**Answer**:
> False

