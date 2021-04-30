import csv
import pandas as pd

# average key down time
# average key roll-over time
# most accurate keys ranking
# lshift/rshift ratio
# number of times pressed backspace
# train time
# test time
# train/test ratio
# mistake count
# mistake ratio
test = pd.read_csv('test.csv').values.tolist()
train = pd.read_csv('train.csv').values.tolist()

# testa = test[::2]
# testb = test[1::2]
# for a, b in zip(testa, testb):
#     print(f'down time ="{b[0] - a[0]}"')
# 
# 
# testa = test[1::2]
# testb = test[2::2]
# for a, b in zip(testa, testb):
#     print(f'down time ="{b[0] - a[0]}"')

downs = [b[0] - a[0] for a, b in zip(test[::2], test[1::2])]
rollover = [b[0] - a[0] for a, b in zip(test[1::2], test[2::2])]

print(''.join([_[2] for _ in test[::2]]))
# avg_down = sum(downs) / len(downs)
# avg_rollover = sum(rollover) / len(rollover)
# print(f'avg down time ={avg_down}\n'
#       f'avg rollover ={avg_rollover}\n')
# for _ in downs:
#     print(_)
# print(downs)
# print(rollover)
