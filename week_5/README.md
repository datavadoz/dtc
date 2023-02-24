# Week 5

## Overview
This week covers batch processing with Spark.

## Setup

Build customized spark-py image:
```
docker build . -t dtc-week-5
```

## Homework
### Question 1: Output of spark.version
```
$ docker container run --rm -it -p 8000:4040 --name week-5 dtc-week-5 /opt/spark/bin/pyspark
>>> import pyspark
>>> from pyspark.sql import SparkSession
>>>
>>> spark = SparkSession.builder.master("local[*]").appName("Test").getOrCreate()
>>> spark.version
'3.3.2'
```
**Answer**: 
> 3.3.2
