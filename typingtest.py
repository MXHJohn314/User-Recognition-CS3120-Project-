import hashlib
from tkinter import *
from tkinter import messagebox
import re
import time

code_hash = hashlib.md5(''.join(open('typingtest.py', 'r').readlines()).encode('utf-8'))
'''csv column names header'''
COLUMN_NAMES = 'timeDown::timeUp::key::l_shift::r_shift\n'
'''Regex captures matches for each word and space to keep track of highlighting.'''
word_regex = re.compile(r'(\s+|\S+)')
'''Require a different format for keybinding.'''

chars = {_ for _ in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRS" \
                    "TUVWXYZ1234567890-=`~!@#$%^&*()_+[{]}\\|\'\";:,./?>"} | {'less'}
spacers = {'BackSpace', 'space'}
'''Small dictionary that keeps track of which shift keys are being held at any moment.'''
shifts = {'Shift_L': '0', 'Shift_R': '0'}
shift_presses = {'<Shift_R>', '<Shift_L>', '<KeyRelease-Shift_L>', '<KeyRelease-Shift_R>'}
'''Set of keys should be ignored by the program.'''
ignored_keys = {'Escape', 'Delete',
                'Left', 'Up', 'Down', 'Right', 'Home', 'Prior', 'End', 'Next',
                'Insert', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R',
                'Return', 'Control-v', 'Control-a', 'Control-c', 'Return'} \
               | set([_ for __ in [[f'Button-{i}', f'Double-Button-{i}']
                                   for i in range(1, 4)] for _ in __])
'''Dictionary to simplify colorization.'''
colors = {
    'white': {'bg': 'black', 'fg': 'white'},
    'black': {'bg': 'white', 'fg': 'black'},
    False: {'bg': 'red', 'fg': 'white'},
    True: {'bg': 'lightblue', 'fg': 'black'},
}


#  Return "1" if shift key is down, otherwise "0"
def shift_check(e):
    if e.type == '2':
        shifts[e.keysym] = '1'
    elif e.type == '3':
        key = 'Shift_L' if shifts['Shift_L'] == '1' else 'Shift_R'
        shifts[key] = '0'

#  Used to simplify colorization of text in either of the Text widgets.
def change_color(txt, name, color):
    txt.tag_configure(name, foreground=color['fg'], background=color['bg'])


# Converts string indices into Text widget indices format as a str ("row.column")
def get_ranges(t_):
    tags = []
    s_ = '1.0'
    for match in re.finditer(word_regex, t_.get('1.0', 'end-1c')):
        str_len = match.end() - match.start()
        e_ = t_.index(f'{s_}+{str_len}c')
        tags.append((s_, e_))
        s_ = t_.index(f'{e_}')
    return tags


#  This class creates text widgets to facilitate a typing test.
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"): editor.root.destroy()


# Use the regex to make a list of words from a Text widget.
def get_words(txt):
    return [_ for _ in re.findall(word_regex, txt.get('1.0', 'end-1c'))]


class TypingTest:
    def __init__(self):
        self.data = {}  # Hold some previous word data about typing correctness
        self.close_result = None
        self.current = 0  # keeps track of the current word or space that should be typed.
        self.root = Tk()  # Gui root window object
        self.root.title("Typing Test")
        self.logger = Logger()  # Stores info on keystrokes to a file
        self.prompt_dict = None  # Indexes every word in the prompt for highlighting
        self.usr_in_dict = None  # Indexes every word typed by the user for highlighting
        self.size = None  # Count of # of words typed by the user, to tell when the test is over.
        self.prompt = Text(height=14, font=("Arial", 10))  # Words to type will appear here
        self.usr_in = Text(height=14, font=("Arial", 10))  # User input will appear here
        self.generate_prompt()  # Fill self.prompt with the first test, and index the words.
        messagebox.showinfo('Get Ready!', 'The test will begin now.', parent=self.usr_in)
        self.usr_in.focus_force()  # User should only be able to edit the bottom half.
        #  Set key binds for all keys and combos (ignore keys we don't care about)
        bnd = self.root.bind
        usr_bnd = self.usr_in.bind
        release = self.logger.log_release
        [bnd(i, self.check_text) for i in chars]
        [bnd(_, shift_check) for _ in shift_presses]
        [usr_bnd(f'<{_}>', 'break') for _ in ignored_keys]
        [bnd(f'<{_}>', 'break') for _ in ignored_keys]
        [bnd(f'<{i}>', self.check_text) for i in spacers]
        bnd('<KeyRelease>', lambda e: release(e, '::'.join(shifts.values())))

    #  Set up the typing test for use.
    def generate_prompt(self, txt='train_prompt.txt'):
        self.prompt.config(state='normal')
        self.prompt.delete('1.0', END)  # Remove any text if it exists
        self.usr_in.delete('1.0', END)
        with open(f'src/{txt}', 'r') as file: prompt = file.read().strip()  # Get text to be inserted
        self.logger.open(f"{txt.split('.')[0].split('_')[0]}.csv")  # Name the logger output
        self.prompt.insert(1.0, prompt)  # Fill the top text widget with the prompt
        prompt_words = get_words(self.prompt)  # Use regex to get all words
        self.prompt_dict = get_ranges(self.prompt)  # Get widget string indices for word bounds
        self.usr_in_dict = get_ranges(self.prompt)  # will be checked against prompt_dict for change
        #  Change list of tuples into list of dictionaries with ordered indices of words & ranges
        for i, (r, w) in enumerate(zip(self.prompt_dict, prompt_words)):
            s, e = r
            self.usr_in_dict[i] = {'tag': f'{(s, e)}', 'word': w, 's': s, 'e': e}
            self.prompt_dict[i] = {'tag': f'{(s, e)}', 'word': w, 's': s, 'e': e}
            r = {'tag': f'{(s, e)}', 'word': w, 's': s, 'e': e}
            self.prompt.tag_add(r['tag'], s, e)
        self.size = self.prompt.index(self.prompt.index(f'end-1c'))  # Store text size

        '''!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        For debugging toward the end of the prompt, uncomment the next two lines.'''
        # self.usr_in.insert(1.0, ''.join(prompt_words[:-3]))
        # self.current = len(prompt_words) - 3

        # Configure prompt and user input widget options, colorize the first word to type.
        self.prompt.config(wrap=WORD, exportselection=0, insertbackground='white')
        change_color(self.prompt, '', colors['black'])
        self.usr_in.grid(row=2, column=0, padx=10, pady=10)
        self.prompt.grid(row=0, column=0, padx=10, pady=10)
        self.usr_in.config(wrap=WORD, exportselection=0)
        temp = self.prompt_dict[self.current]
        self.prompt.tag_add(temp['tag'], temp['s'], temp['e'])
        change_color(self.prompt, temp['tag'], colors['white'])
        self.prompt.config(state='disabled')

    # This method highlights words near the current word in the bottom half.
    # Also highlights the word the user should be typing in the top half.
    def highlight_typed_words(self, key):
        txt_ranges = get_ranges(self.usr_in)  # Get updated list of user input words/ranges
        txt_words = get_words(self.usr_in)

        # Update the user input dictionary for words near current
        start = max(self.current - 2, 0)
        end = min(self.current + 3, len(txt_ranges))
        _zip = zip(
            [_ for _ in range(start, end + 1)],
            txt_ranges[start:end],
            txt_words[start:end])
        for i, (start_, end_), word in _zip:
            if i > len(self.usr_in_dict) - 1: return False
            txt = self.usr_in_dict[i]
            self.usr_in.tag_remove(txt['tag'], txt['s'], txt['e'])
            self.usr_in_dict[i]['word'] = word
            self.usr_in_dict[i]['s'] = start_
            self.usr_in_dict[i]['e'] = end_
            self.usr_in_dict[i] = txt
            self.usr_in.tag_add(txt['tag'], txt['s'], txt['e'])
        prompt_entry = self.prompt_dict[self.current]  # Get current indexing info for comparison
        user_entry = self.usr_in_dict[self.current]
        change_color(self.prompt, prompt_entry['tag'], colors['black'])  # Un-highlight current word
        if prompt_entry['word'].isspace():  # User should be typing a space
            if key.isspace():
                txt = self.usr_in_dict[self.current]
                txt['is_correct'] = True
                change_color(self.usr_in, txt['tag'], colors[True])
                self.current += 1
            elif key == '\b':
                self.current -= 1  # If backspace typed, go back to the previous word
            else:  # Otherwise they added extra stuff to the last word, highlight the word red
                self.current -= 1
                txt = self.usr_in_dict[self.current]
                txt['is_correct'] = False
                change_color(self.usr_in, txt['tag'], colors[False])
                self.highlight_typed_words('')  # recurse this method to fix highlighting
        else:  # User should be typing non-space character
            if key.isspace():  # Prematurely went to word, highlight word red and go to next word
                txt = self.usr_in_dict[self.current]
                txt['is_correct'] = False
                start, end = [_.strip() for _ in txt['tag'][1:-1].split(',')]
                txt['tag '] = f'{(start, self.usr_in.index(INSERT))}'
                self.usr_in_dict[self.current] = txt
                change_color(self.usr_in, txt['tag'], colors[False])
                txt = self.usr_in_dict[self.current]
                change_color(self.usr_in, txt['tag'], colors[True])
            elif key == '\b':  # If backspace typed, check if current word is now previous word
                insert = int(self.usr_in.index(f'{INSERT}').split('.')[1])
                start = int(user_entry['s'].split('.')[1])
                if insert < start:
                    self.current -= 2  # Go back to last word
                    self.highlight_typed_words('')  # recurse this method to fix highlighting
                else:  # If still on same word, update the user_in_dict with new range
                    color = colors[prompt_entry['word'].startswith(user_entry['word'])]
                    change_color(self.usr_in, user_entry['tag'], color)
                    if prompt_entry['word'] == user_entry['word']:
                        self.current += 1
            elif prompt_entry['word'].startswith(user_entry['word']):  # User typed correct char
                txt = self.usr_in_dict[self.current]
                change_color(self.usr_in, txt['tag'], colors[True])
                txt['is_correct'] = True
                if prompt_entry['word'] == user_entry['word']:  # If word is complete, move on
                    self.current += 1
            else:  # Key pressed was the wrong character, highlight current word red
                txt = self.usr_in_dict[self.current]
                change_color(self.usr_in, txt['tag'], colors[False])
                txt['is_correct'] = False
        if self.current > len(self.prompt_dict) - 1: return False
        prompt_entry = self.prompt_dict[self.current]  # Get current prompt_dict entry
        change_color(self.prompt, prompt_entry['tag'], colors['white'])  # Highlight it in prompt
        return True

    # This method:
    # - Checks to see if the last key event should be logged (ignores some keys).
    # - Ends the test if prompt is complete
    # - Calls for the second test to begin after the first
    # - Exits the program after the second test.
    # - Calls logger to close (write) the key events to a csv file.
    # - Calls for re-highlighting
    def check_text(self, event):
        t = time.time_ns()
        shifts_state = f'{shifts["Shift_L"]}::{shifts["Shift_R"]}'
        self.logger.log_press(event.char, shifts_state, t)
        prompt_index = self.prompt.index(f'{self.size}-1c')
        user_in_index = self.usr_in.index(f'{self.size}-1c')
        if prompt_index == user_in_index or not self.highlight_typed_words(event.char):
            self.close_result = self.logger.close()
            if self.close_result == 'train.csv':
                file_name = self.logger.name
                """For debugging towards the end of the prompt, use self.current = 428.
                For normal functionality, set self.current = 0"""
                # self.current = 428
                self.current = 0
                messagebox.showinfo('Warm Up Complete', 'Now time for the Real Prompt!',
                                    parent=self.usr_in)
                self.generate_prompt('test_prompt.txt')
                self.usr_in.focus_force()
                return
            else:
                # scraper = DataScraper()
                messagebox.showinfo(
                    f'Thank You', 'Thanks for participating! Please contactAdam Wojdyla or '\
                                  ' Malcolm Johnson to submit.', parent=self.root)
            self.root.destroy()

    #  Prevent the window from closing automatically
    def mainloop(self):
        self.root.mainloop()
        return self.close_result


# This class is responsible for formatting csv rows of typing
# data, writing it to files, and echoing the output to the console.
class Logger:
    def __init__(self):
        self.log = ''  # Holds a file's worth of csv lines
        self.completed_logs = 0  # count for which file is current
        self.name = ''  # Name of the file that will be written to
        self.event_buffer = {}  # Pairs every down event row with an up event row
        self.test_hash = None
        self.train_hash = None

    # Format the row for KeyDown info and store it in the buffer
    def log_press(self, key, shifts_state, t):
        if key in self.event_buffer: return  # prevents repeat logs when holding a key
        key = 'backspace' if key == '\b' else key  # writing '\b' to a file is trouble
        self.event_buffer[key] = (t, f'{key}::{shifts_state}\n')  # store down event

    # Format the row for KeyRelease info if a matching down event exists in the buffer
    def log_release(self, event, shifts_state):
        t = time.time_ns()
        key = event.char if event.char != '' else 'backspace'  # backspace shenanigans
        if key not in self.event_buffer: return  # prevents repeat logs when releasing a key
        entry = self.event_buffer[key]  # get the matching down event from the buffer
        self.log += f'{entry[0]}::{t}::{entry[1]}'  # concat key event info to log
        del self.event_buffer[key]  # delete the key from the buffer

    # Write contents stored in log to a file, and return the file name created.
    def close(self):
        print(COLUMN_NAMES + self.log + '\n\n')
        with open(self.name, 'w') as file:
            file.write(COLUMN_NAMES + self.log)
        if 'train' in self.name:
            self.train_hash = hashlib.md5(COLUMN_NAMES + self.log)
            self.log = ''
            return self.name
        else:
            self.test_hash = hashlib.md5(COLUMN_NAMES + self.log)
            return hashlib.md5(f'{code_hash}{self.train_hash}{self.test_hash}')

    # Does not open a file immediately, but will open and write the file when test is over.
    def open(self, param):
        self.name = param


class CheckSum:
    def __init__(self, code_hash):
        self.code_hash = code_hash

    def __hash_file(self, file):
        return hashlib.md5(''.join(open(file, 'r').readlines()).encode('utf-8'))

    def verify_hash(self, file_1, file_2, result):
        h_1 = self.__hash_file(file_1)
        h_2 = self.__hash_file(file_2)
        return hashlib.md5(f'{self.code_hash}{h_1}{h_2}'.encode('utf-8')) == result


if __name__ == "__main__":
    editor = TypingTest()
    editor.root.protocol("WM_DELETE_WINDOW", on_closing)
    result_hash = editor.mainloop()
    checker = CheckSum(code_hash)
    if checker.verify_hash('train.csv', 'test.csv'):
        print('all good')
    else:
        print('this was tampered with...')



