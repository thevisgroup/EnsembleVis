import pandas as pd
from pathlib import Path
import os
import csv

dirname = os.path.dirname(__file__)

header = ["p_inf", "p_hcw", "c_hcw", "d", "q", "p_s", "lambda",
          "T_lat", "juvp_s", "T_inf", "T_rec", "T_sym", "T_hos", "inf_asym"]

dir = os.path.join(
    dirname, f'../../public/assets')

dir = Path(dir).resolve()

filename = f'{dir}/posterior_parameters_meta.csv'

if os.path.exists(filename):
    os.remove(filename)

df = pd.read_csv(f'{dir}/posterior_parameters.csv', usecols=header,
                 skipinitialspace=True)

res = df.agg(['mean', 'min', 'max'])

res.to_csv(filename)
