import pandas as pd
import pathlib
import os

dirname = os.path.dirname(__file__)

asymptomatic = ['I1', 'I2', 'I3', 'I4']
symptomatic = ['I_s1', 'I_s2', 'I_s3', 'I_s4']

header = ['S', 'E', 'H', 'R', 'D']
col_list = ['iter', 'day', 'age_group'] + header + symptomatic + asymptomatic
header = header + ['I', 'IS']

for i in range(160):
    dir = f'/Volumes/Travis/UQVis/output_row_{i}'

    files = os.listdir(dir)
    for file in files:
        if "full" in file:
            # read file
            df = pd.read_csv(f'{dir}/{file}', usecols=col_list,
                             skipinitialspace=True).fillna(0)

            # sum symptomatic and asymptomatic cases
            df['IS'] = df[symptomatic].sum(axis=1)
            df['I'] = df[asymptomatic].sum(axis=1)

            print(f'writing simu_{i}')
            for j in range(8):
                # calculate mean, min, max
                result = df[df['age_group'] == j].groupby(
                    ['day'])[header].agg(['mean', 'min', 'max'])

                # rename columns
                result.columns = ["_".join(x) for x in result.columns.values]

                # write file
                out = os.path.join(
                    dirname, f'../../public/assets/data/output/simu_{i}')
                pathlib.Path(out).mkdir(parents=True, exist_ok=True)
                result.to_csv(f'{out}/age_{j}.csv')
