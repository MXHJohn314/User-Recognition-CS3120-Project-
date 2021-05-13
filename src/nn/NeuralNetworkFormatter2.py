import random
import tkinter as tk
import pandas as pd

from src.knn.TypingTestTools import *
from statistics import mean


# This class is meant to clean up the suboptimal format of the provided data
class NeighborsFormatter:
    def __init__(self, prompt_path='../train_prompt.txt', _split=0.2):
        self.subjects = []
        self.user_data = None  # Will be a dataframe for input from a user
        self.name = ''  # Name of the current user (an object for classification)
        self.user_string = ''  # What the user ended up typing
        self.user_words = None
        self.rows = []  # List to hold all info from split test
        self.split = _split  # percent split of train, the rest will be for test group
        self.backspace_count = 0  # Todo
        self.missed_words = 0  # Todo
        self.test = []
        self.train = []

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
        test_dict, train_dict = self.__get_char_stats(data)
        self.subjects.append(usr_name)
        self.test.append(pd.DataFrame(test_dict))
        self.train.append(pd.DataFrame(train_dict))
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
        for idx in range(len(stop_event_rows) - 1):
            newer_row = stop_event_rows.iloc[idx]
            older_row = start_event_rows.iloc[idx]
            char = older_row['key']
            if char not in self.prompt_chars: continue
            if idx not in test_indices:
                self.generate_col_vals(char, newer_row, older_row, row, train_dict)
            else:
                self.generate_col_vals(char, newer_row, older_row, row, test_dict)
        return test_dict, train_dict

    def generate_col_vals(self, char, newer_row, older_row, row, test_dict):
        if f'{char}_count' not in row:
            test_dict[f'{char}_count'] = [0]
            j = 0
        else:
            j = test_dict[f'{char}_count'][0]
        test_dict[f'{char}_{j}_u_d'] = [newer_row['timeDown'] - older_row['timeUp']]
        test_dict[f'{char}_{j}_d_d'] = [newer_row['timeDown'] - older_row['timeDown']]
        test_dict[f'{char}_{j}_u_u'] = [newer_row['timeUp'] - older_row['timeUp']]
        test_dict[f'{char}_{j}_d_u'] = [older_row['timeUp'] - older_row['timeDown']]
        test_dict[f'{char}_count'][0] += 1

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
        df_train = pd.concat(self.train).dropna(axis=1, how='any')
        df_test = pd.concat(self.test).dropna(axis=1, how='any')
        df_train.to_csv('train_data.csv', index=False)
        df_test.to_csv('test_data.csv', index=False)
        with open('names.csv', 'w') as csv:
            csv.write('\n'.join(self.subjects))
        features = (set(df_test.columns) | set(df_train.columns))
        with open('features.csv', 'w') as csv:
            csv.write('\n'.join(features))
            print(df_test.equals(df_train))
        return df_train, df_test

def init():
    formatter = NeighborsFormatter()
    files = get_file_names()
    for i, user_name in enumerate(files):
        print(user_name, i)
        [os_check(_) for _ in files[user_name].values()]
        train_frame = pd.read_csv(files[user_name]['train'], delimiter='::', engine='python')
        test_frame = pd.read_csv(files[user_name]['test'], delimiter='::', engine='python')
        user_data = pd.concat([train_frame, test_frame])
        formatter.add_user(user_name, user_data)
        # if i == 1: break
    return formatter.to_csv()
init()
