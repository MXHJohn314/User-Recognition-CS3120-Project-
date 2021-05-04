import re
import pandas as pd
import datetime
import json

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
        self.prompt_name = self._list = self._frame = self.word_dict = self.user_words = self.prompt_words = self.user_input = self.avg_hold = self.user_split = self.prompt_split = self.missed_words = self.l_sum = self.r_sum = self.missed_words = self.time_diffs = None
        self.elapsed_time = self.csv_name = self.avg_up_down = self.error_count = None

    def scrape_files(self, csv_name, promt_dict, user_dict):
        self._frame = pd.read_csv(csv_name, delimiter='::', engine='python')
        self._list = self._frame.values.tolist()
        self.user_input, self.error_count = get_error_count(self._list)
        self.avg_hold, self.avg_up_down = get_avg_hold_time(self._list)
        self.user_split = [i for i in re.findall(r'(\s+|\S+)', self.user_input)]
        self.prompt_split = [i for i in re.findall(r'(\s+|\S+)', open('scape_train.csv').read())]
        self.missed_words = 0
        for a, b in zip(self.user_split, self.prompt_split):
            if a != b: self.missed_words += 1
        self.l_sum = self._frame['l_shift'].sum()
        self.r_sum = self._frame['r_shift'].sum()
        self.missed_words = self.get_word_faults()
        self.time_diffs = self.get_time_diffs()
        self.elapsed_time = self.get_elapsed_time()
        print('shift sum: ', self.l_sum / self.r_sum)

        avg_up_up = self.get_avg_up_up(self._frame)

        # Todo train time
        # Todo test time
        # Todo train/test ratio
        # Todo mistake ratio/expected errors
        # Todo most accurate keys ranking
        self.results = f'Average key press time: {self.avg_hold} sec\n' \
                       f'Average key rollover duration: {self.avg_up_down} sec\n' \
                       f'Average time between key releases: {avg_up_up}\n' \
                       f'Total # of errors: {self.error_count}'

    def get_word_entry(self, i):
        pass

    def __str__(self):
        return self.results

    def get_avg_up_up(self, _frame):
        i_loc_1 = _frame['timeUp'].iloc[:-1]
        i_loc_2 = _frame['timeUp'].iloc[1:]
        up_up = [b - a for a, b in zip(i_loc_1, i_loc_2)]
        return sum(up_up) / len(up_up)

    def get_elapsed_time(self):
        t = self._frame['timeUp'].iloc[-1] - self._frame['timeDown'].iloc[0]
        t = (t / 10**9)
        print(f'Total train time: {t}')

        return t

    def get_time_diffs(self):
        _list = self._frame
        df = pd.DataFrame([int(b[0]) - int(a[0]) for a, b in zip(_list[1::2], _list[2::2])],
                                columns=['roll_over'])
        avg = df['roll_over'].sum() / len(df)
        return df, avg

    def get_word_faults(self, user_dict):
        count = 0
        for value in user_dict:
            if not value['is_correct']: count += 1
        return count


if __name__ == "__main__":
    file = open('myfile.json')
    prompt_dict = json.loads(file.readline())
    user_dict = json.loads(file.readline())
    print(prompt_dict)
    print(user_dict)
    scraper = DataScraper()
    scraper.scrape_files('scape_test.csv', prompt_dict, user_dict)
#scraper = DataScraper()
#print(scraper.get_elapsed_time())

# Todod error count: number of times pressed backspace
#  user_string = the full string that was created by the user.

# TODOD lshift/rshift ratio
# TODOD average key down time
# TODOD average key roll-over time
# TODO variance of time ~ for each word
# TODO add bigram and trigram speed for top 100 bigrams and top 30 trigrams

# Testing procedure:
#TODO: Create quality matching csv and JSON files.
#TODO Accurately create a way to manipulate data with dictionaries.

