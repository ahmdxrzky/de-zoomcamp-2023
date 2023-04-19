{{ config(materialized='view') }}

with weather_data as 
(
  select *,
    row_number() over(partition by date(datetime)) as rn
  from {{ source('staging', 'all_weather_data') }}
)
select
    -- identifiers
    cast(index as integer) as record_id,
    
    -- timestamps
    cast(datetime as timestamp) as record_datetime,
    
    -- weather info
    cast(temp as numeric) as temperature,
    cast(pressure as numeric) as pressure,
    cast(humidity as integer) as humidity,
    cast(wind_speed as numeric) as wind_speed,
    cast(wind_deg as integer) as wind_direction_degrees,
    cast(weather_id as integer) as weather_id
from weather_data
where rn = 1
