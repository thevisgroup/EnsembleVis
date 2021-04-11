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

for age_group in range(8):
    print("Start the code...\n")

    input_name = 'data_D_Age' + str(age_group) + '.npy'
    data = load(input_name)
    #print(data.shape)

    if age_group == 0:
        data_stack = data
    else:
        data_stack = np.vstack((data_stack, data))

    print(data_stack.shape)
    # for i in range(160):
    #     tmp = i*np.ones((1000,1))
    #     if i == 0:
    #         y = tmp
    #     else:
    #         y = np.vstack((y,tmp))

    #random sampling for quick calculation
    #idx = np.random.randint(160000, size=10000)
    #data_sub = data[:20000,:]
    #y_sub = y[:20000,:]

#     time_start = time.time()
data_std = StandardScaler().fit_transform(data_stack)
#     print(data_std.shape)
#
pca = PCA(n_components=2)
embedding = pca.fit_transform(data_std)
print(embedding.shape)
#     #print(embedding.shape)
for age_group in range(8):

    output_name = 'PCA_D_Age' + str(age_group) + '.npy'
    pca_data = embedding[(age_group*160000):((age_group+1)*160000),:]

    save(output_name, pca_data)
# #
# df = pd.DataFrame(embedding, columns=("x", "y"))
#
#
# df_subset = pd.DataFrame()
# df_subset['tsne-2d-one'] = embedding[:,0]
# df_subset['tsne-2d-two'] = embedding[:,1]
# df_subset['y_sub']=y_sub
# plt.figure(figsize=(16,10))
# sns.scatterplot(
#     x="tsne-2d-one", y="tsne-2d-two",
#     hue="y_sub",
#     palette=sns.color_palette("hls", 20),
#     data=df_subset,
#     legend="full",
#     alpha=0.3
# )
# plt.show()