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

### Question 4: How long was the longest trip in Hours?
```
...
>>> from pyspark.sql import functions as F
>>> df = spark.read.parquet('fhvhv/2021/06')
>>> df = df.withColumn('duration', F.unix_timestamp(df.dropoff_datetime) - F.unix_timestamp(df.pickup_datetime))
>>> df.agg(F.max(df.duration)).take(1)[0][0] / 3600
66.8788888888889
```

**Answer**:
> 66.87 Hours

### Question 5: Spark’s User Interface which shows application's dashboard runs on which local port?
```
$ docker ps
CONTAINER ID   IMAGE        COMMAND                  CREATED       STATUS       PORTS                                       NAMES
b26dbbd3cba1   dtc-week-5   "/opt/entrypoint.sh …"   2 hours ago   Up 2 hours   0.0.0.0:8000->4040/tcp, :::8000->4040/tcp   week-5
```

**Answer**:
> 4040

### Question 6: Using the zone lookup data and the fhvhv June 2021 data, what is the name of the most frequent pickup location zone?

```
>>> from spark.sql.functions import desc
>>> fhvhv = spark.read.option('header', 'true').option('InferSchema', 'true').csv('fhvhv_tripdata_2021-06.csv')
>>> zone = spark.read.option('header', 'true').option('InferSchema', 'true').csv('taxi_zone_lookup.csv')
>>> fhvhv.groupby('PULocationID').count().join(zone, fhvhv['PULocationID'] == zone['LocationID'], 'inner').sort(desc('count')).select('Zone', 'count').show()
+--------------------+------+
|                Zone| count|
+--------------------+------+
| Crown Heights North|231279|
|        East Village|221244|
|         JFK Airport|188867|
|      Bushwick South|187929|
|       East New York|186780|
|TriBeCa/Civic Center|164344|
|   LaGuardia Airport|161596|
|            Union Sq|158937|
|        West Village|154698|
|             Astoria|152493|
|     Lower East Side|151020|
|        East Chelsea|147673|
|Central Harlem North|146402|
|Williamsburg (Nor...|143683|
|          Park Slope|143594|
|  Stuyvesant Heights|141427|
|        Clinton East|139611|
|West Chelsea/Huds...|139431|
|             Bedford|138428|
|         Murray Hill|137879|
+--------------------+------+
```

**Answer**:
> Crown Heights North

