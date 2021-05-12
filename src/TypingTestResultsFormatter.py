import random

import pandas
import pandas as pd

from TypingTestTools import *
from statistics import mean
from enchant.utils import levenshtein
from sklearn.model_selection import train_test_split


# This class is meant to clean up the suboptimal format of the provided data
class TypingTestResultsFormatter:
    def __init__(self, prompt_path='train_prompt.txt', _split=0.2):
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
        self.user_words = re.split('(\s|\S)', self.user_string)  # List of all the words that the user typed have been typed
        dicts = self.__get_char_stats(data)
        train_dict, test_dict = dicts
        _train_frame = pd.DataFrame(train_dict, index=[usr_name])
        _test_frame = pd.DataFrame(test_dict)
        self.rows_train.append(_train_frame)
        self.rows_test.append(_test_frame)
        self.__clear()

    def __get_char_stats(self, new_user_dataframe) -> (dict, dict):
        row = {}
        train_dict = {}
        test_dict = {}
        start_event_rows = drop_row_bound(new_user_dataframe, 'first')
        stop_event_rows = drop_row_bound(new_user_dataframe, 'last')
        _zip = zip(stop_event_rows, start_event_rows)
        last_idx = len(new_user_dataframe.index)
        test_indices = random.sample(range(1, last_idx - 1), int(last_idx * self.split))
        train_indices = [x for x in range(1, last_idx - 1) if x not in test_indices]
        test_dict['backspaces'] = [(new_user_dataframe.iloc[test_indices]['key'] == "backspace").sum()]
        train_dict['backspaces'] = [(new_user_dataframe.iloc[train_indices]['key'] == "backspace").sum()]
        test_indices = set(test_indices)
        for idx in range(len(stop_event_rows) - 1):
            newer_row = stop_event_rows.iloc[idx]
            older_row = start_event_rows.iloc[idx]
            char = older_row['key']
            if char in ['\b', ''] or char.isupper() or char not in self.prompt_chars: continue
            if f'{char}_count' not in row:
                for dict_ in [f'{char}_u_d_avg', f'{char}_d_d_avg', f'{char}_d_u_avg',
                              f'{char}_u_u_avg']: row[dict_] = []
                row[f'{char}_count'] = 0
            if any([newer_row[_] - older_row[_] <= 0 for _ in ['timeDown', 'timeUp']]):
                if idx < len(stop_event_rows) - 2:
                    pass
                    # Todo if idx in indices, add another one:
                # indices.add(random.sample(range(idx + 1, last_idx - 1), 1))
                continue
            row[f'{char}_u_d_avg'].append(newer_row['timeDown'] - older_row['timeUp'])
            row[f'{char}_d_d_avg'].append(newer_row['timeDown'] - older_row['timeDown'])
            row[f'{char}_u_u_avg'].append(newer_row['timeUp'] - older_row['timeUp'])
            row[f'{char}_d_u_avg'].append(older_row['timeUp'] - older_row['timeDown'])
            row[f'{char}_count'] += 1
            char_columns = [f'{char}_u_d_avg', f'{char}_d_d_avg', f'{char}_d_u_avg',
                            f'{char}_u_u_avg', f'{char}_count']
            if idx not in test_indices:
                for dict_ in char_columns:
                    train_dict[dict_] = row[dict_]
            else:
                for dict_ in char_columns:
                    test_dict[dict_] = row[dict_]
        for dict_ in [test_dict, train_dict]:
            for key_ in dict_:
                if not isinstance(dict_[key_], list):
                    dict_[key_] = [dict_[key_]]
                else: dict_[key_] = [mean(dict_[key_])]
        # for dict_ in [test_dict, train_dict]:
        #     user_means = {}
        #     for key_ in dict_:
        #         if key_.endswith('count'):
        #             dict_[key_] = [dict_[key_]]
        #         elif key_.endswith('avg'):
        #             avg = key_[-7:]
        #             if avg not in user_means:
        #                 user_means[avg] = []
        #             user_means[avg].append(mean(dict_[key_]))
        #     for key_ in user_means:
        #         user_means[key_] = [mean(user_means[key_])]
        #     dict_.update(user_means)
        #     for key_ in dict_:
        #         if isinstance(dict_[key_], list) and len(dict_[key_]) > 1:
        #             dict_[key_] = [mean(dict_[key_])]
        #     for key_ in dict_:
        #         if not isinstance(dict_[key_], list) or len(dict_[key_]) != 1:
        #             print(dict_[key_])
            # Todo: impute the data where needed
        return train_dict, test_dict

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
        df_train.to_csv('train.csv')
        df_test = self.impute(self.rows_train)
        df_test.to_csv('test.csv')
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


if __name__ == "__main__":
    formatter = TypingTestResultsFormatter()
    files = get_file_names()
    for i, user_name in enumerate(files):
        print(user_name, i)
        [os_check(_) for _ in files[user_name].values()]
        train_frame = pd.read_csv(files[user_name]['train'], delimiter='::', engine='python')
        test_frame = pd.read_csv(files[user_name]['test'], delimiter='::', engine='python')
        user_data = pd.concat([train_frame, test_frame])
        formatter.add_user(user_name, user_data)
        # if i == 1: break
    train, test = formatter.to_csv()
    print(train.isnull().sum().sum())
    print(test.isnull().sum().sum())
