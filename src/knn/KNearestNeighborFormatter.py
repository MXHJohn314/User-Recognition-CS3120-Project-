import random

import pandas
import pandas as pd

from TypingTestTools import *
from statistics import mean
from enchant.utils import levenshtein
from sklearn.model_selection import train_test_split


# This class is meant to clean up the suboptimal format of the provided data
class NNFormatter:
    def __init__(self, prompt_path='../train_prompt.txt', _split=0.2):
        self.user_data = None  # Will be a dataframe for input from a user
        self.name = ''  # Name of the current user (an object for classification)
        self.user_string = ''  # What the user ended up typing
        self.user_words = None
        self.rows_train = []  # List to hold all info from split train
        self.rows_test = []  # List to hold all info from split test
        self.split = _split  # percent split of train, the rest will be for test group
        self.backspace_count = 0  # Todo
        self.missed_words = 0  # Todo

        self.prompt_string = open(prompt_path,
                                  'r').read()  # The entire string of what should have been typed
        self.prompt_words = re.split('(\s|\S)',
                                     self.prompt_string)  # List of all the words that should have been typed
        self.prompt_chars = set(
            self.prompt_string)  # know which chars to look out for when creating stats

    def add_user(self, usr_name, data) -> None:
        self.user_data = data
        key_event_list = self.user_data['key'].tolist()
        self.user_string = get_user_string(key_event_list)
        self.user_words = re.split('(\s|\S)',
                                   self.user_string)  # List of all the words that the user typed have been typed
        dicts = self.__get_char_stats(data)
        train_dict, test_dict = dicts
        _train_frame = pd.DataFrame(train_dict, index=[usr_name])
        _test_frame = pd.DataFrame(test_dict)
        self.rows_train.append(_train_frame)
        self.rows_test.append(_test_frame)
        self.__clear()

    def __get_char_stats(self, new_user_dataframe) -> (dict, dict):
        train_dict = {}
        test_dict = {}
        start_event_rows = drop_row_bound(new_user_dataframe, 'first')
        stop_event_rows = drop_row_bound(new_user_dataframe, 'last')
        _zip = zip(stop_event_rows, start_event_rows)
        last_idx = len(new_user_dataframe.index)
        test_indices = random.sample(range(1, last_idx - 1), int(last_idx * self.split))
        train_indices = [x for x in range(1, last_idx - 1) if x not in test_indices]
        test_dict['backspaces'] = [
            (new_user_dataframe.iloc[test_indices]['key'] == "backspace").sum()]
        train_dict['backspaces'] = [
            (new_user_dataframe.iloc[train_indices]['key'] == "backspace").sum()]
        test_indices = set(test_indices)
        rollovers = []
        holds = []
        speeds = []
        for idx in range(len(stop_event_rows) - 1):
            newer_row = stop_event_rows.iloc[idx]
            older_row = start_event_rows.iloc[idx]
            char = older_row['key']
            if char in ['\b', ''] or char.isupper() or char not in self.prompt_chars: continue
            if any([newer_row[_] - older_row[_] <= 0 for _ in ['timeDown', 'timeUp']]):
                if idx < len(stop_event_rows) - 2:
                    pass
                    # Todo if idx in indices, add another one:
                # indices.add(random.sample(range(idx + 1, last_idx - 1), 1))
                continue
            speeds.append(newer_row['timeUp'] - newer_row['timeDown'])
            rollovers.append(newer_row['timeDown'] - older_row['timeUp'])
            holds.append(older_row['timeUp'] - older_row['timeDown'])
        test_rollovers = [mean(_ for i, _ in enumerate(rollovers) if i in test_indices)]
        test_rollover_rate = self.rollover_rate(rollovers, test_indices)
        test_holds = [mean(_ for i, _ in enumerate(holds) if i in test_indices)]
        train_rollovers = [mean(_ for i, _ in enumerate(rollovers) if i in train_indices)]
        train_rollover_rate = self.rollover_rate(rollovers, test_indices)
        train_holds = [mean(_ for i, _ in enumerate(holds) if i in train_indices)]
        train_speeds = [sum([_ for i, _ in enumerate(speeds) if i in train_indices])]
        test_speeds = [sum([_ for i, _ in enumerate(speeds) if i not in train_indices])]
        train_dict = {'backspaces': test_dict['backspaces'], 'holds': train_holds, 'rollover': train_rollovers, 'roll_rate': train_rollover_rate, 'speed': train_speeds}
        test_dict = {'backspaces': test_dict['backspaces'], 'holds': test_holds, 'rollover': test_rollovers, 'roll_rate': test_rollover_rate, 'speed': test_speeds}
        return train_dict, test_dict

    def rollover_rate(self, rollovers, test_indices):
        len1 = len([_ for i, _ in enumerate(rollovers) if i in test_indices and _ > 0])
        len2 = len([_ for i, _ in enumerate(rollovers) if i in test_indices and _ < 0])
        return [len1 / len2] if len2 > 0 else [len2 / len1]

    def __clear(self):
        self.user_data = None
        self.name = ''
        self.results = ''
        self.user_string = ''
        self.backspace_count = 0
        self.missed_words = 0

    def __str__(self):
        return self.results

    def to_csv(self):
        df_train = self.impute(self.rows_train)
        df_train.to_csv('neighbor_train.csv', index=False)
        df_test = self.impute(self.rows_train)
        df_test.to_csv('neighbor_test.csv', index=False)
        names = df_train.index.tolist()
        features = df_train.columns.tolist()
        with open('../nn/names.csv', 'w') as csv:
            csv.write('\n'.join(names))
        with open('../nn/features.csv', 'w') as csv:
            csv.write('\n'.join(features))
        return df_train, df_test

    def impute(self, rows) -> pd.DataFrame:
        _df = pd.concat(rows)
        for _user_name, r in _df.iterrows():
            for pattern in ['_u_d_avg', '_d_d_avg', '_u_u_avg', '_d_u_avg', '_count']:
                temp = _df.loc[[_user_name]]
                subset = temp.filter(regex=pattern)
                _mean = subset.mean(1)[_user_name]
                _df.loc[_user_name] = _df.loc[_user_name].T.fillna(_mean).T
        return _df


# def init():
formatter = NNFormatter()
files = get_file_names()
for i, user_name in enumerate(files):
    print(user_name, i)
    [os_check(_) for _ in files[user_name].values()]
    train_frame = pd.read_csv(files[user_name]['train'], delimiter='::', engine='python')
    test_frame = pd.read_csv(files[user_name]['test'], delimiter='::', engine='python')
    user_data = pd.concat([train_frame, test_frame])
    formatter.add_user(user_name, user_data)
    # if i == 1: break
formatter.to_csv()
