import pandas as pd

test = pd.read_csv('scape_test.csv', delimiter='::', engine='python').values.tolist()
train = pd.read_csv('scape_train.csv', delimiter='::', engine='python').values.tolist()


# Todod average key down time
# Todod average key roll-over time
downs = [int(b[0]) - int(a[0]) for a, b in zip(test[::2], test[1::2])]
rollover = [int(b[0]) - int(a[0]) for a, b in zip(test[1::2], test[2::2])]
avg_down = sum(downs) / len(downs)
avg_rollover = sum(rollover) / len(rollover)
print(f'avg down time ={avg_down}\n'
      f'avg rollover ={avg_rollover}\n')


# Todod number of times pressed backspace
#  user_string = the full string that was created by the user.
user_string = ''.join([_[2] for _ in test[::2]])
print(f'user_string before manipulation:\n\t"{user_string}"')
target = 'backspace'
backspace_count = 0
while user_string.startswith(target):
    user_string = user_string[len(target):]
    backspace_count += 1
while target in user_string:
    backspace_count += 1
    idx = user_string.index(target)
    user_string = user_string[:idx - 1] + user_string[idx + len(target):]
print(f'user_string after manipulation:\n\t"{user_string}"\n')

# Todo lshift/rshift ratio
# Todo train time
# Todo test time                                                    \n\t
# Todo train/test ratio
# Todo mistake count
# Todo mistake ratio
# Todo most accurate keys ranking
