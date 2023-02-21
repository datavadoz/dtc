{{ config(materialized='view') }}

SELECT 
    dispatching_base_num,
    CAST(pickup_datetime AS TIMESTAMP) AS pickup_datetime,
    CAST(dropOff_datetime AS TIMESTAMP) AS dropoff_datetime,
    CAST(PUlocationID AS INTEGER) AS pu_location_id,
    CAST(DOlocationID AS INTEGER) AS do_location_id,
    SR_Flag AS sr_flag,
    Affiliated_base_number AS affiliated_base_number
FROM {{ source('staging', 'fhv_tripdata_2019') }}
{% if var('is_test_run', default=true) %}
    LIMIT 100
{% endif %}

