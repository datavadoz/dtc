# Week 2

## Overview
Only worker container plays an orchestration role to:
- Route taxi data in CSV format from GitHub to GCS in parquet format.
- Route taxi data in parquet format from GCS to Google BigQuery.

## Prerequisite
Docker with compose plugin (current testing version: 20.10.17).

## Instruction
Build and bring system up:
```
docker compose build
docker compose up -d
```

Browse orion webpage: [localhost:4200](localhost:4200/)


## Homework
### Question 1: How many rows does that dataset (green taxi in January 2020) have?
```
...
07:21:45.895 | INFO    | Task run 'clean-b9fd7e03-0' - rows: 447770
07:21:45.915 | INFO    | Task run 'clean-b9fd7e03-0' - Finished in state Completed()
07:21:45.939 | INFO    | Flow run 'quaint-manatee' - Created task run 'write_local-f322d1be-0' for task 'write_local'
07:21:45.940 | INFO    | Flow run 'quaint-manatee' - Executing 'write_local-f322d1be-0' immediately...
07:21:46.810 | INFO    | Task run 'write_local-f322d1be-0' - Finished in state Completed()
07:21:46.832 | INFO    | Flow run 'quaint-manatee' - Created task run 'write_gcs-1145c921-0' for task 'write_gcs'
07:21:46.832 | INFO    | Flow run 'quaint-manatee' - Executing 'write_gcs-1145c921-0' immediately...
07:21:46.897 | INFO    | Task run 'write_gcs-1145c921-0' - Getting bucket 'dtc-week-2'.
07:21:48.721 | INFO    | Task run 'write_gcs-1145c921-0' - Uploading from PosixPath('data/green/green_tripdata_2020-01.parquet') to the bucket 'dtc-week-2' path 'data/green/green_tripdata_2020-01.parquet'.
07:22:10.588 | INFO    | Task run 'write_gcs-1145c921-0' - Finished in state Completed()
07:22:10.612 | INFO    | Flow run 'quaint-manatee' - Finished in state Completed('All states completed.')
```
**Answer**:
> 447770

