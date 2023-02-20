# Week 4

## Overview
This big week discovers DBT.

## Setup

Install DBT :
```
pip install dbt-bigquery
```

Ingest yellow, green and fhv taxi data for both 2019 and 2022 into GCS, BQ:
`web -> GCS -> BigQuery`


## Homework
### Question 1: What is the count of records in the model fact_trips after running all models with the test run variable disabled and filtering for 2019 and 2020 data only (pickup datetime)?
```
SELECT COUNT(*)
FROM `trips_data_all.fact_trips`
```
**Answer**: 
> 61,604,284 (closest with 61,635,329)

