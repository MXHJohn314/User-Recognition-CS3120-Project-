# Define useful functions
# Activation function
def sigmoid(t):
    return 1 / (1 + np.exp(-t))


# Derivative of sigmoid
def sigmoid_derivative(p):
    return p * (1 - p)


def cls(): return print("\033[2J\033[;H", end='')


cls()

# Imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Class definition
class NeuralNetwork:
    def __init__(self, x, y):
        self.input = x
        self.weights1 = np.random.rand(self.input.shape[1], 2)
        self.weights2 = np.random.rand(2, 33)
        self.y = y
        self.output = np.zeros(y.shape)
        # plt.hist(self.weights2)
        # plt.show

    def feedforward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.weights1))
        self.layer2 = sigmoid(np.dot(self.layer1, self.weights2))
        return self.layer2

    def backprop(self):
        d_weights2 = np.dot(self.layer1.T,
                            2 * (self.y - self.output) * sigmoid_derivative(self.output))
        d_weights1 = np.dot(self.input.T,
                            np.dot(2 * (self.y - self.output) * sigmoid_derivative(self.output),
                                   self.weights2.T) *
                            sigmoid_derivative(self.layer1))
        self.weights1 += d_weights1
        self.weights2 += d_weights2
        rows1 = len(d_weights1)
        columns1 = len(d_weights1[0])
        rows2 = len(d_weights2)
        columns2 = len(d_weights2[0])
        result = 'Dimension Weight Matrix 1:', rows1, columns1, '\nDimension Weight Matrix 2:', rows2, columns2
        return result

    def train(self, X, y):
        self.output = self.feedforward()
        self.backprop()

# Each row is a training example, each column is a feature  [X1, X2, X3]
X = np.array([_.split(',') for _ in open('train_data.csv', 'r').readlines()[1:]], dtype=float)
names = open('names.csv', 'r').readlines()
y = np.array([[i] for i in range(len(names))])
NN = NeuralNetwork(X, y)

for i in range(1500):  # trains the NN 1,000 times
    if i % 300 == 0:
        print("for iteration # " + str(i) + "\n")
        print("Input : \n" + str(X))
        print("Actual Output: \n" + str(y))
        print("Predicted Output: \n" + str(NN.feedforward()))
        print("Loss: \n" + str(np.mean(np.square(y - NN.feedforward()))))
        # mean sum squared loss
        print("\n")
    NN.train(X, y)

# tests
X_test = np.array([_.split(',') for _ in open('data.csv', 'r').readlines()[1:]], dtype=float)
h1 = sigmoid(np.dot(X_test, NN.weights1))
y_pred = sigmoid(np.dot(h1, NN.weights2))
first_row = y_pred[0]
second_row = y_pred[1]

print("Predicted Output y values: \nX1=[0,0,0] y1=", first_row, "\nX2=[1,1,1] y2=", second_row)

weighted_result = NN.backprop()

for i in weighted_result:
    print(str(i))
