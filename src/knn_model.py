import pandas as pd
from bunch import bunchify

print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from sklearn.datasets import load_iris
from sklearn.ensemble import (RandomForestClassifier, ExtraTreesClassifier,
                              AdaBoostClassifier)
from sklearn.tree import DecisionTreeClassifier
from TypingTestResultsFormatter import init
init()
# Parameters
n_classes = 3
n_estimators = 30
cmap = plt.cm.RdYlBu
plot_step = 0.02  # fine step width for decision surface contours
plot_step_coarser = 0.5  # step widths for coarse classifier guesses
RANDOM_SEED = 13  # fix the seed on each iteration

train = pd.read_csv('train.csv')
y_train = np.array(list(train.index.values))
train = pd.read_csv('train.csv')
train.drop(index=0, axis=0)
X_train = train.to_numpy()
names = np.genfromtxt('names.csv', delimiter=',')
features = np.genfromtxt('features.csv', delimiter=',')
test = pd.read_csv('test.csv')
test.reset_index()
X_test = test.to_numpy()
y_test = np.array(list(test.index.values))

# data scaling will be done as follow
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# train the model with the help of KNeighborsClassifier class of sklearn
from sklearn.neighbors import KNeighborsClassifier

classifier = KNeighborsClassifier(n_neighbors=8)
classifier.fit(X_train, y_train)

# make prediction
y_pred = classifier.predict(X_test)

# print the results
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

result = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(result)
result1 = classification_report(y_test, y_pred)
print("Classification Report:", )
print(result1)
result2 = accuracy_score(y_test, y_pred)
print("Accuracy:", result2)


