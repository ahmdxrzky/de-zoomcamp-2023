import os
import pandas as pd
from datetime import datetime
from pathlib import Path

df = pd.read_csv("week7_project/assets/openweatherdata-denpasar-1990-2020.csv")
df['dt'] = df['dt'] + 126230400
df['datetime'] = df['dt'].apply(lambda x: datetime.fromtimestamp(x))
df['year'] = df['datetime'].dt.year
df['month'] = df['datetime'].dt.month
df = df.drop(['dt_iso', 'timezone', 'city_name', 'lat', 'lon', 'snow_1h', 'snow_3h', 'snow_6h', 'snow_12h', 'snow_24h', 'snow_today', 'weather_main', 'weather_description', 'weather_icon'], axis=1)

for year in range(1995, 2024):
    for month in range(1, 13):
        df_new = df[(df['year'] == year) & (df['month'] == month)]
        path = Path(os.path.join("assets", "dataset", str(year), f"{year}_{month:02}.csv"))
        if not os.path.exists(path.parent):
            os.system(f"mkdir -p {path.parent}")
        df_new.to_csv(path)