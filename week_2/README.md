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
> 447,770

### Question 2: What’s the cron schedule for "the first of every month at 5am UTC"?
**Answer**:
> 0 5 1 * *

### Question 3: Load yellow taxi data for Feb. 2019 and March 2019 from GCS into BigQuery. How many rows did your flow code process?
**Answer**:
> 14,851,920

### Question 4: Github Storage Block. How many rows of green taxi data for Nov. 2020 were processed by the script?
```
...
05:37:30.322 | INFO    | Task run 'clean-2c6af9f6-0' - rows: 88605
05:37:30.514 | INFO    | Task run 'clean-2c6af9f6-0' - Finished in state Completed()
05:37:30.541 | INFO    | Flow run 'naruto' - Created task run 'write_local-09e9d2b8-0' for task 'write_local'
05:37:30.542 | INFO    | Flow run 'naruto' - Executing 'write_local-09e9d2b8-0' immediately...
05:37:30.763 | INFO    | Task run 'write_local-09e9d2b8-0' - Finished in state Completed()
05:37:30.784 | INFO    | Flow run 'naruto' - Created task run 'write_gcs-67f8f48e-0' for task 'write_gcs'
05:37:30.785 | INFO    | Flow run 'naruto' - Executing 'write_gcs-67f8f48e-0' immediately...
05:37:30.845 | INFO    | Task run 'write_gcs-67f8f48e-0' - Getting bucket 'dtc-week-2'.
05:37:32.975 | INFO    | Task run 'write_gcs-67f8f48e-0' - Uploading from PosixPath('data/green/green_tripdata_2020-11.parquet') to the bucket 'dtc-week-2' path 'data/green/green_tripdata_2020-11.parquet'.
05:37:35.196 | INFO    | Task run 'write_gcs-67f8f48e-0' - Finished in state Completed()
05:37:35.224 | INFO    | Flow run 'naruto' - Finished in state Completed('All states completed.')
05:37:36.039 | INFO    | prefect.infrastructure.process - Process 'naruto' exited cleanly.
```
**Answer**:
> 88,605

*Note*: Create deployment with GitHub storage:

1. Create GitHub block from Orion UI.
2. Create deployment yaml file:
```
prefect deployment build week_2/worker/etl_web_to_gcs.py:etl_web_to_gcs --storage-block github/<github_block_name_from_step_1> -n <deployment_name>d
```
3. Start agent on **default** queue:
```
prefect agent start --work-queue "default"
```
4. Run workflow with required params:
