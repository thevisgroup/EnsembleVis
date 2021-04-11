import numpy as np
from numpy import load
import time
from sklearn.manifold import TSNE
import seaborn as sns
import pandas as pd
from numpy import save
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import pathlib
import os

dirname = os.path.dirname(__file__)

output_res = np.empty((160, 2))

for age_group in range(8):
    print(f'Start age group: {age_group} \n')

    input_name = os.path.join(dirname, f'PCA_D_Age{age_group}.npy')
    output_name = os.path.join(dirname, f'PCA_D_Age{age_group}_mean.npy')

    pca_data = load(input_name)

    output_data = []
    for sim_config in range(160):
        sub_data = pca_data[(sim_config*1000):(sim_config+1)*1000, :]
        config_mean = np.mean(sub_data, axis=0)

        if sim_config == 0:
            output_data = config_mean
        else:
            output_data = np.vstack((output_data, config_mean))

    out = os.path.join(
        dirname, f'../../../public/assets/data/output/pca/d')

    pathlib.Path(out).mkdir(parents=True, exist_ok=True)

    # for age_mean
    output_res = output_res+output_data

    # for individual age_group
    df = pd.DataFrame(output_data, columns=['x', 'y']).to_csv(
        f'{out}/age_{age_group}.csv', index_label=["simu"])

    # for aggregated age_group
    output_data = np.hstack(
        (output_data, np.full((160, 1), fill_value=age_group, dtype=int)))

    df = pd.DataFrame(output_data, columns=['x', 'y', 'age_group'])
    df["age_group"] = df["age_group"].astype(int)

    df.to_csv(f'{out}/age.csv', index_label=["simu"],
              mode='a', header=not os.path.exists(f'{out}/age.csv'))

    # for age_mean
    df = pd.DataFrame(output_res/8, columns=['x', 'y']).to_csv(
        f'{out}/age_mean.csv', index_label=["simu"])
