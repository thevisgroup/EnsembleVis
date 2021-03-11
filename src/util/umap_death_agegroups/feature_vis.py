from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np
from numpy import load
import time
from sklearn.manifold import TSNE
import seaborn as sns
import pandas as pd
import pathlib
import os

dirname = os.path.dirname(__file__)

for f in range(7):

    data = load(
        os.path.join(
            dirname, f'umap_D_Age{f}.npy'))

    for i in range(160):
        tmp = i*np.ones((1000, 1))
        if i == 0:
            y = tmp
        else:
            y = np.vstack((y, tmp))

    umap_sub = data[:10000, :]
    y_sub = y[:10000, :]

    df_subset = pd.DataFrame()
    df_subset['umap-2d-one'] = umap_sub[:, 0]
    df_subset['umap-2d-two'] = umap_sub[:, 1]
    df_subset['y_sub'] = y_sub

    out = os.path.join(
        dirname, f'../../../public/assets/data/output/umap/d')

    pathlib.Path(out).mkdir(parents=True, exist_ok=True)

    df_subset.to_csv(
        f'{out}/age_{f}.csv', index=False)
