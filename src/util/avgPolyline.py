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
    with open(filename, "a", newline="") as w:
        writer = csv.writer(w)
        writer.writerow(g for g in (csvheader+header+["type"]))

        # calculate mean for average polylines
        for f in range(8):
            # read file
            df = pd.read_csv(f'{dir}/age_{f}.csv', usecols=header,
                             skipinitialspace=True)
            # calculate mean
            res = df.mean(axis=0).to_frame(
                f).transpose().values.flatten().tolist()
            # insert age_group
            res.insert(0, f)
            # append type
            res.append("average")
            # write file
            writer.writerow(res)

        w.close()

    with open(filename, "a", newline="") as w:
        writer = csv.writer(w)
        df = pd.read_csv(filename, usecols=header[1:],
                         skipinitialspace=True)

        # calculate average of averages
        aoa = df.mean(axis=0).to_frame(
            f).transpose().values.flatten().tolist()

        # insert day 0
        aoa.insert(0, "")
        # insert age_group
        aoa.insert(0, "")
        # append type
        aoa.append("aoa")
        # write file
        writer.writerow(aoa)

        # calculate standard deviation
        std = df.std(axis=0).to_frame(
            f).transpose().values.flatten().tolist()

        # insert day 0
        std.insert(0, "")
        # insert age_group
        std.insert(0, "")
        # append type
        std.append("std")
        # write file
        writer.writerow(std)
