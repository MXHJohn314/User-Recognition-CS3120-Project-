import os
import re
import pandas as pd


def drop_row_bound(new_user, row) -> pd.DataFrame:
    idx = new_user.count()[0] - 1 if row == 'first' else 0
    return new_user.drop(new_user.index[idx])


def get_file_names() -> list:
    users = "../DATA/users"
    trains = tests = []
    names = {}
    for user_name in os.listdir(users):
        names[user_name] = {
            'train': f'{users}/{user_name}/train.csv',
            'test': f'{users}/{user_name}/test.csv'
        }
    return names


def get_user_string(_list) -> (str, int):
    target = 'backspace'
    user_string = ''.join([_ for _ in _list])
    while user_string.startswith(target):
        user_string = user_string[len(target):]
    while target in user_string:
        idx = user_string.index(target)
        user_string = user_string[:idx - 1] + user_string[idx + len(target):]
        while user_string.startswith(target):
            user_string = user_string[len(target):]
    return user_string


def get_word_faults(user_dict) -> int:
    count = 0
    for value in user_dict:
        if not value['is_correct']: count += 1
    return count


def os_check(csv_name) -> bool:
    string = ''.join(open(csv_name, 'r').readlines())
    matches = re.findall('\x7f', string)
    if len(matches) == 0:
        return False
    string = string.replace('\x7f', 'backspace')
    with open(csv_name, 'w') as file:
        file.write(string)
    return True
