import pandas as pd
import pathlib
import os

dirname = os.path.dirname(__file__)

col_list = ['iter', ' day', ' age_group', ' S', ' E', ' H', ' R', ' D']
header = [' S', ' E', ' H', ' R', ' D']


for i in range(0, 139):
  dir = f'/Volumes/Travis/UQVis/output_row_{i}'

  files = os.listdir(dir)
  for file in files:
    if "full" in file:
      csv_file = f'{dir}/{file}'
      df = pd.read_csv(csv_file, usecols=col_list).fillna(0)

      for j in range(0, 8):
        a = df[df[' age_group'] == j].groupby([' day'])[header].agg('mean')
        out = os.path.join(
            dirname, f'../../public/assets/data/output/simu_{i}')
        print(out)
        pathlib.Path(out).mkdir(parents=True, exist_ok=True)
        a.to_csv(f'{out}/age_{j}.csv', columns=header)
