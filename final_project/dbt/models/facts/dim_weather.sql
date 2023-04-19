{{ config(materialized='table') }}

select 
    id as weather_id, 
    main as weather_category, 
    description as weather_description
from {{ ref('weather_lookup') }}