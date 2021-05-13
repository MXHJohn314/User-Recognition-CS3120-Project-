import pandas as pd
from bunch import bunchify
from sklearn.neighbors import KNeighborsClassifier

print(__doc__)

import numpy as np
import matplotlib.pyplot as plt

# Parameters
n_classes = 3
n_estimators = 30
cmap = plt.cm.RdYlBu
plot_step = 0.02  # fine step width for decision surface contours
plot_step_coarser = 0.5  # step widths for coarse classifier guesses
RANDOM_SEED = 13  # fix the seed on each iteration

train = pd.read_csv('neighbor_train.csv')
y_train = np.array(list(train.index.values))
train = pd.read_csv('neighbor_train.csv')
train.drop(index=0, axis=0)
X_train = train.to_numpy()
names = np.array(open('../nn/names.csv', 'r').readlines())
features = np.array(open('../nn/features.csv', 'r').readlines())
test = pd.read_csv('neighbor_test.csv')
test.reset_index()
X_test = test.to_numpy()
y_test = np.array(list(test.index.values))

error_rate = []
# Might take some time
for i in range(1, 3):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train, y_train)
    pred_i = knn.predict(X_test)
    error_rate.append(np.mean(pred_i != y_test))
plt.figure(figsize=(10, 6))
plt.plot(range(1, 3), error_rate, color='blue', linestyle='dashed', marker='o',
         markerfacecolor='red', markersize=10)
plt.title('Error Rate vs. K Value')
plt.xlabel('K')
plt.ylabel('Error Rate')
plt.show()
