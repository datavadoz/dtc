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

### Question 2: Repartition fhvhv_tripdata_2021-06.csv to 12 partitions and save it to parquet. What is the average size of the Parquet (ending with .parquet extension) files that were created (in MB)?
```
>>> import pyspark
>>> from pyspark.sql import SparkSession
>>>
>>> spark = SparkSession.builder.master("local[*]").appName("Test").getOrCreate()
>>> df = spark.read.option('header', 'true').option('InferSchema', 'true').csv('fhvhv_tripdata_2021-06.csv')
>>> df = df.repartition(12)
>>> df.write.parquet('fhvhv/2021/06')

$ ls -lh fhvhv/2021/06/
total 270M
-rw-r--r-- 1 185 root   0 Feb 24 07:17 _SUCCESS
-rw-r--r-- 1 185 root 23M Feb 24 07:17 part-00000-12be8903-4da9-4aba-80a9-5b0ac1fc5d5d-c000.snappy.parquet
-rw-r--r-- 1 185 root 23M Feb 24 07:17 part-00001-12be8903-4da9-4aba-80a9-5b0ac1fc5d5d-c000.snappy.parquet
-rw-r--r-- 1 185 root 23M Feb 24 07:17 part-00002-12be8903-4da9-4aba-80a9-5b0ac1fc5d5d-c000.snappy.parquet
-rw-r--r-- 1 185 root 23M Feb 24 07:17 part-00003-12be8903-4da9-4aba-80a9-5b0ac1fc5d5d-c000.snappy.parquet
-rw-r--r-- 1 185 root 23M Feb 24 07:17 part-00004-12be8903-4da9-4aba-80a9-5b0ac1fc5d5d-c000.snappy.parquet
-rw-r--r-- 1 185 root 23M Feb 24 07:17 part-00005-12be8903-4da9-4aba-80a9-5b0ac1fc5d5d-c000.snappy.parquet
-rw-r--r-- 1 185 root 23M Feb 24 07:17 part-00006-12be8903-4da9-4aba-80a9-5b0ac1fc5d5d-c000.snappy.parquet
-rw-r--r-- 1 185 root 23M Feb 24 07:17 part-00007-12be8903-4da9-4aba-80a9-5b0ac1fc5d5d-c000.snappy.parquet
-rw-r--r-- 1 185 root 23M Feb 24 07:17 part-00008-12be8903-4da9-4aba-80a9-5b0ac1fc5d5d-c000.snappy.parquet
-rw-r--r-- 1 185 root 23M Feb 24 07:17 part-00009-12be8903-4da9-4aba-80a9-5b0ac1fc5d5d-c000.snappy.parquet
-rw-r--r-- 1 185 root 23M Feb 24 07:17 part-00010-12be8903-4da9-4aba-80a9-5b0ac1fc5d5d-c000.snappy.parquet
-rw-r--r-- 1 185 root 23M Feb 24 07:17 part-00011-12be8903-4da9-4aba-80a9-5b0ac1fc5d5d-c000.snappy.parquet
```
**Answer**:
> 24MB

### Question 3: How many taxi trips were there on June 15?

```
...
>>> df = spark.read.parquet('fhvhv/2021/06')
>>> from pyspark.sql import functions as F
>>> df = df.withColumn('pickup_date', F.to_date(df.pickup_datetime))
>>> df.filter(df.pickup_date == '2021-06-15').count()
452470
```
**Answer**:
> 452,470

