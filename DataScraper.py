import pandas as pd


def get_error_count(_list):
    user_string = ''.join([_[2] for _ in _list[::2]])
    target = 'backspace'
    backspace_count = 0
    while user_string.startswith(target):
        user_string = user_string[len(target):]
        backspace_count += 1
    while target in user_string:
        backspace_count += 1
        idx = user_string.index(target)
        user_string = user_string[:idx - 1] + user_string[idx + len(target):]
    return user_string, backspace_count


def get_avg_hold_time(_list):
    downs = [int(b[0]) - int(a[0]) for a, b in zip(_list[::2], _list[1::2])]
    rollover = [int(b[0]) - int(a[0]) for a, b in zip(_list[1::2], _list[2::2])]
    avg_down = sum(downs) / len(downs)
    avg_rollover = sum(rollover) / len(rollover)
    return avg_down, avg_rollover


class DataScraper:
    def __init__(self):
        test_list = pd.read_csv('scape_test.csv', delimiter='::', engine='python').values.tolist()
        train_list = pd.read_csv('scape_train.csv', delimiter='::', engine='python').values.tolist()
        test_frame = pd.read_csv('scape_test.csv', delimiter='::', engine='python')
        train_frame = pd.read_csv('scape_train.csv', delimiter='::', engine='python')
        avg_hold, avg_up_down = get_avg_hold_time(train_list)
        user_input, error_count = get_error_count(train_list)
        avg_up_up = self.get_avg_up_up(train_frame)
        # Todo lshift/rshift ratio
        # Todo train time
        # Todo test time
        # Todo train/test ratio
        # Todo mistake ratio/expected errors
        # Tod o most accurate keys ranking
        self.results = f'Average key press time: {avg_hold} sec\n' \
                       f'Average key rollover duration: {avg_up_down} sec\n' \
                       f'Average time between key releases: {avg_up_up}\n' \
                       f'Total # of errors: {error_count}'

    def get_avg_up_up(self, train_frame):
        iloc_1 = train_frame['timeUp'].iloc[:-1]
        iloc_2 = train_frame['timeUp'].iloc[1:]
        up_up = [b - a for a, b in zip(iloc_1, iloc_2)]
        return sum(up_up) / len(up_up)

    def __str__(self):
        return self.results

    # Todod error count - number of times pressed backspace
    #  user_string = the full string that was created by the user.

    # Todod average key down time
    # Todod average key roll-over time


print(DataScraper())
