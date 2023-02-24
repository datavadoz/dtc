# Week 5

## Overview
This week covers batch processing with Spark

## Setup

Run Spark via Docker :
```
docker container run --rm -it -p 8000:4040 --name my_spark apache/spark-py:v3.3.2 bash
```


## Homework
### Question 1: Output of spark.version
```
$ docker container run --rm -it -p 8000:4040 --name my_spark apache/spark-py:v3.3.2 bash
$ export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
$ export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
$ python3
>>> import pyspark
>>> from pyspark.sql import SparkSession
>>>
>>> spark = SparkSession.builder.master("local[]")
>>> spark.version
'3.3.2'
```
**Answer**: 
> 3.3.2

