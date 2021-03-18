import pandas as pd
from pathlib import Path
import os
import csv

dirname = os.path.dirname(__file__)

csvheader = ["age_group"]
header = ["day", "S_mean", "S_min", "S_max", "E_mean", "E_min", "E_max", "H_mean", "H_min", "H_max",
          "R_mean", "R_min", "R_max", "D_mean", "D_min", "D_max", "I_mean", "I_min", "I_max", "IS_mean", "IS_min", "IS_max"]

for i in range(160):
    dir = os.path.join(
        dirname, f'../../public/assets/data/output/simu_{i}')

    dir = Path(dir).resolve()

    filename = f'{dir}/avgPolyline.csv'

    if os.path.exists(filename):
        os.remove(filename)

    result = []
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(g for g in (csvheader+header))

        for f in range(8):

            # read file
            df = pd.read_csv(f'{dir}/age_{f}.csv', usecols=header,
                             skipinitialspace=True)
            # calculate mean
            res = df.mean(axis=0).to_frame(f).transpose()
            res = res.values.flatten().tolist()
            # insert age_group
            res.insert(0, f)
            # write file
            writer.writerow(res)
