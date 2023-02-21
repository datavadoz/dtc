{{ config(materialized='table') }}

WITH fhv_data AS (
    SELECT *, 
    FROM {{ ref('stg_fhv_tripdata') }}
), 

dim_zones AS (
    SELECT * FROM {{ ref('dim_zones') }}
    WHERE borough != 'Unknown'
)

SELECT
    fhv_data.dispatching_base_num,
    fhv_data.pickup_datetime,
    fhv_data.dropoff_datetime,
    fhv_data.pu_location_id,
    fhv_data.do_location_id,
    fhv_data.sr_flag,
    fhv_data.affiliated_base_number,
    pickup_zone.borough AS pickup_borough,
    pickup_zone.zone AS pickup_zone,
    dropoff_zone.borough AS dropoff_borough,
    dropoff_zone.zone AS dropoff_zone
FROM fhv_data
INNER JOIN dim_zones AS pickup_zone
ON fhv_data.pu_location_id = pickup_zone.locationid
INNER JOIN dim_zones AS dropoff_zone
ON fhv_data.do_location_id = dropoff_zone.locationid

