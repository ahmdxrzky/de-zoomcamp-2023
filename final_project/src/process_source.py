import os
import pandas as pd
from datetime import datetime
from pathlib import Path

final_project_dir = Path(__file__).absolute().parent.parent
df = pd.read_csv(os.path.join(final_project_dir, "assets", "openweatherdata-denpasar-1990-2020.csv"))
df['dt'] = df['dt'] + 126230400
date_time = pd.Series(df['dt'].apply(lambda x: datetime.fromtimestamp(x)))
df.insert(1, "datetime", date_time)
df['year'] = df['datetime'].dt.year
df['month'] = df['datetime'].dt.month
df = df.drop(['dt_iso', 'weather_main', 'weather_description', 'weather_icon'], axis=1)

for year in range(1995, 2024):
    for month in range(1, 13):
        df_new = df[(df['year'] == year) & (df['month'] == month)]
        path = Path(os.path.join(final_project_dir, "assets", "dataset", str(year), f"{year}_{month:02}.csv"))
        if not os.path.exists(path.parent):
            os.system(f"mkdir -p {path.parent}")
        df_new = df_new.drop(['year', 'month'], axis=1)
        df_new.to_csv(path)
        df_new = pd.read_csv(path, index_col=0)
        df_new.reset_index(inplace=True)
        df_new.to_csv(path, index=False)