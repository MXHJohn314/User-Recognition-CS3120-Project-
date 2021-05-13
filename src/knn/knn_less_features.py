import pandas as pd
from bunch import bunchify
from sklearn.neighbors import KNeighborsClassifier

print(__doc__)
cmap = ['white', 'white', 'green', 'purple', 'black', 'white', 'white', 
'black', 'blue',     'purple', 'yellow', 'green', 'white', 
'blue', 'blue', 'green', 'green', 'red', 'black', 'yellow', 
'white', 'blue', 'orange', 'green', 'blue', 'green', 'white', 
'red', 'yellow', 'red', 'green', 'white', 'red', 'white', 
'yellow', 'orange', 'red', 'black', 'green', 'orange', 'purple', 
'blue', 'red', 'red', 'blue', 'purple', 'yellow', 'yellow', 'red', 
'yellow']
names = open
def get_cmap(n, name='hsv'):
    return plt.cm.get_cmap(name, n)

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
names = ['backspaces', 'holds', 'rollover', 'roll_rate', 'speed']
combos = set()

for i in range(len(names)):
    for j in range(len(names)):
        s = ''.join(sorted([names[i], names[j]]))
        if names[i] != names[j] and s.startswith(names[i]):
            combos.add((names[i], names[j]))

for i, (name1, name2) in enumerate(combos):
    df = pd.read_csv('neighbor_train.csv')
    kmeans = KMeans(n_clusters=33, random_state=0)
    df['cluster'] = kmeans.fit_predict(df[[name1, name2]])
    
    # get centroids
    centroids = kmeans.cluster_centers_
    cen_x = [i[0] for i in centroids]
    cen_y = [i[1] for i in centroids]
    ## add to df
    df['cen_x'] = df.cluster.map({0:cen_x[0], 1:cen_x[1], 2:cen_x[2]})
    df['cen_y'] = df.cluster.map({0:cen_y[0], 1:cen_y[1], 2:cen_y[2]})# define and map colors
    df['c'] = df.cluster.map({i: cmap[i] for i in range(33)}, )
    plt.scatter(df[name1], df[name2], c=df.c, alpha = 0.6, s=10)
    plt.xlabel(name1)
    plt.ylabel(name2)
    plt.show()



# # Parameters
# n_classes = 3
# n_estimators = 30
# cmap = plt.cm.RdYlBu
# plot_step = 0.02  # fine step width for decision surface contours
# plot_step_coarser = 0.5  # step widths for coarse classifier guesses
# RANDOM_SEED = 13  # fix the seed on each iteration
# 
# train = pd.read_csv('neighbor_train.csv')
# y_train = np.array(list(train.index.values))
# train = pd.read_csv('neighbor_train.csv')
# train.drop(index=0, axis=0)
# X_train = train.to_numpy()
# names = np.array(open('../nn/names.csv', 'r').readlines())
# features = np.array(open('../nn/features.csv', 'r').readlines())
# test = pd.read_csv('neighbor_test.csv')
# test.reset_index()
# X_test = test.to_numpy()
# y_test = np.array(list(test.index.values))
# 
# error_rate = []
# # Might take some time
# for i in range(1, 33):
#     knn = KNeighborsClassifier(n_neighbors=i)
#     knn.fit(X_train, y_train)
#     pred_i = knn.predict(X_test)
#     error_rate.append(np.mean(pred_i != y_test))
# plt.figure(figsize=(10, 6))
# plt.plot(range(1, 33), error_rate, color='blue', linestyle='dashed', marker='o',
#          markerfacecolor='red', markersize=10)
# plt.title('Error Rate vs. K Value')
# plt.xlabel('K')
# plt.ylabel('Error Rate')
# plt.show()
