{{ config(materialized='table') }}

SELECT
    locationid,
    borough,
    zone,
    REPLACE(service_zone, 'Boro', 'with Green') AS service_zone
FROM {{ ref('taxi_zone_lookup') }}
