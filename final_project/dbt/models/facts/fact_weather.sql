{{ config(materialized='table') }}

with weather_data as (
    select * 
    from {{ ref('stg_weather_data') }}
),
dim_weather as (
    select * from {{ ref('dim_weather') }}
)
select 
    weather_data.record_id,
    weather_data.record_datetime,
    extract(year from weather_data.record_datetime) as record_year, 
    extract(month from weather_data.record_datetime) as record_month,
    weather_data.temperature,
    weather_data.pressure,
    weather_data.humidity,
    weather_data.wind_speed,
    weather_data.wind_direction_degrees,
    weather_data.weather_id,
    dim_weather.weather_category,
    dim_weather.weather_description
from weather_data
inner join dim_weather
on weather_data.weather_id = dim_weather.weather_id
