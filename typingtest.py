from tkinter import *
import tkinter as tk
from tkinter import messagebox
import re
import time
from datetime import datetime

shifts = {'Shift_L': '0', 'Shift_R': '0'}
bad_keys = {'XF86AudioPlay', 'XF86AudioLowerVolume', 'Win_L', 'Win_R',
            'XF86AudioRaiseVolume', 'XF86AudioMute', 'Shift_L',
            'Shift_R', 'Escape', 'Delete', 'Left', 'Up', 'Down',
            'Right', 'Home', 'Prior', 'End', 'Next', 'Insert', 'App',
            'Control_L', 'Control_R', 'Alt_L', 'Alt_R'}


def shift_check(e):
    shifts[e.keysym] = '1' if '2' == e.type else '0'


def change_color(txt, name, c):
    txt.tag_configure(name, foreground=c['fg'], background=c['bg'])


class TextEditor:
    def __init__(self):
        self.logger = Logger()
        self.sorted_ranges = []
        self.tags = []
        self.tags2 = {}
        self.num_ranges = 0
        self.spaces = []
        self.colors = {
            'white': {'bg': 'black', 'fg': 'white'},
            'black': {'bg': 'white', 'fg': 'black'},
            'grey': {'bg': 'white', 'fg': 'grey'},
            'red': {'bg': 'red', 'fg': 'white'},
            'blue': {'bg': 'lightblue', 'fg': 'black'},
        }
        self.root = Tk()
        self.root.title("Typing Test")
        # self.root.geometry("600x470+200+125")
        self.prompt = Text(height=14, font=("Arial", 10))
        self.txt_in = Text(height=14, font=("Arial", 10))

        self.btn = tk.Button(self.root, text="Generate Prompt", command=self.generate_prompt)
        self.generate_prompt()
        self.prev = None
        messagebox.showinfo('Get Ready!', 'The test will begin now.', parent=self.txt_in)
        self.txt_in.focus_force()
        self.root.bind('<Key>', self.check_text)
        self.root.bind('<KeyRelease>', lambda e: self.logger.log_release(e, ','.join(shifts.values())))

        chars = [_ for _ in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`1234567890" \
                            "-=~!@#$%^&*()_+[{]}\\|\'\";:,./?>"]
        self.root.bind('<Shift_L>', shift_check)
        self.root.bind('<Shift_R>', shift_check)
        self.root.bind('Control-v', 'break')
        self.root.bind('<KeyRelease-Shift_L>', shift_check)
        self.root.bind('<KeyRelease-Shift_R>', shift_check)
        for i in ['less', 'BackSpace', 'space', 'Caps_Lock']:
            self.root.bind(i, self.check_text)
            if i == 'great':
                break
            self.root.bind(f'<KeyRelease-{i}>', lambda e: self.logger.log_release(e, ','.join(shifts.values())))

        for i in chars:
            self.root.bind(i, self.check_text)
            self.root.bind(f'<KeyRelease-{i}>', lambda e: self.logger.log_release(e, ','.join(shifts.values())))

    def generate_prompt(self, txt='train_prompt.txt'):
        self.prompt.config(state='normal')
        self.prompt.delete('1.0', END)
        self.txt_in.delete('1.0', END)
        with open(txt, 'r') as file:
            prompt = file.read().strip()
            file.close()
        self.logger.open(f"{txt.split('.')[0]}.csv")
        self.prompt.insert(1.0, prompt)
        self.size = self.prompt.index(self.prompt.index(f'end-1c'))

        '''For testing purposes. Use to shortcut the train
         and test phase to type only the last 4 chars of each prompt.'''
        # self.txt_in.insert(1.0, prompt[: len(prompt) - 25])

        self.prompt.config(wrap=WORD, exportselection=0, insertbackground='white', state='disabled')
        self.prompt.tag_add('', '1.0', END)
        change_color(self.prompt, '', self.colors['black'])
        self.txt_in.grid(row=2, column=0, padx=10, pady=10)
        self.prompt.grid(row=0, column=0, padx=10, pady=10)
        s = '1.0'
        matches = [_ for _ in re.finditer(r'(\s+|\S+)', prompt)]
        for i, match in enumerate(matches):
            str_len = match.end() - match.start()
            e = self.prompt.index(f'{s}+{str_len}c')
            rng = f'{s}-{e}'
            self.tags.append(rng)
            for j in range(str_len + 1):
                index = self.prompt.index(f'{s}+{j}c')
                self.tags2[index] = rng
            self.prompt.tag_add(f'{s}-{e}', s, e)
            self.txt_in.tag_add(f'{s}-{e}', s, e)
            if i < len(matches) - 1:
                offset = matches[i + 1].start() - match.end()
                space_start = self.prompt.index(f'{e}')
                space_end = self.prompt.index(f'{e}+{offset}c')
                space_tag = f'{space_start}-{space_end}'
                self.tags.append(space_tag)
                self.txt_in.tag_add(space_tag, space_start, space_end)
                s = self.prompt.index(f'{e}+{offset}c')
            if i == 0:
                c = self.colors['white']
                change_color(self.prompt, f'{s}-{e}', c)
        self.txt_in.config(wrap=WORD, exportselection=0)

    def check_text(self, e):
        if e.keysym in bad_keys:
            return

        """For degugging"""
        shifts_state = f'{shifts["Shift_L"]},{shifts["Shift_R"]}'
        current = self.tags2[self.txt_in.index(INSERT)]
        if self.prev and current != self.prev:
            prev_s, prev_e = self.prev.split('-')
            check = self.txt_in.get(prev_s, prev_e) == self.prompt.get(prev_s, prev_e)
            c = self.colors['blue'] if check else self.colors['red']
            self.txt_in.tag_remove(self.prev, prev_s, prev_e)
            self.txt_in.tag_add(self.prev, prev_s, prev_e)
            self.txt_in.config(state='normal')
            change_color(self.txt_in, self.prev, c)
            change_color(self.prompt, current, self.colors['white'])
            change_color(self.prompt, self.prev, self.colors['black'])
        self.prev = current
        self.prompt.config(state='disabled')
        self.logger.log_press(e.keysym, shifts_state)
        if self.prompt.index(f'{self.size}-1c') == self.txt_in.index(f'{self.size}-1c'):
            if self.logger.close() == 'train_prompt.csv':
                messagebox.showinfo('Training Complete', 'Now time for the test prompt.',
                                    parent=self.txt_in)
                self.generate_prompt('test_prompt.txt')
                self.txt_in.focus_force()
            else:
                messagebox.showinfo(
                    'Testing Complete!',
                    'Thanks for participating! Please contact '
                    'AdaM Wojdyla or Malcolm Johnson to submit.', parent=self.root)
                self.root.destroy()

    def mainloop(self):
        self.root.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.logger.close()
            editor.root.destroy()


class Logger:
    def __init__(self):
        self.log = ''
        self.completed_logs = 0
        self.t_array = ['D', 'H', 'M', 'S']
        self.mods = ['shift', 'ctrl', 'alt', 'windows']
        self.check = None
        self.file = None
        self.name = ''
        self.presses = {}

    def log_press(self, key, shifts_state):
        t = datetime.now()
        if key in self.presses:
            return
        self.presses[key] = [self.format_row(key, t, '1', shifts_state)]

    def format_row(self, key, t, is_down, shifts_state):
        millis = int((time.mktime(t.timetuple()) + t.microsecond / 1E6) * 1000) % 1000
        time_str = ','.join([f'{t.strftime("%" + i)}' for i in self.t_array])
        # day, hour, minute, sec, millis, isDown, key, l_shift, r_shift\n
        row = f'{time_str},{millis},{is_down},{key},{shifts_state}\n'
        return row

    def log_release(self, event, shifts_state):
        t = datetime.now()
        key = event.char
        if key not in self.presses:
            return
        self.presses[key].append(self.format_row(key, t, '0', shifts_state))
        self.log += ''.join(self.presses[key])
        del self.presses[key]

    def close(self):
        with open(self.name, 'w') as file:
            file.write('day,hour,minute,sec,millis,isDown,key,l_shift,r_shift\n' + self.log)
        self.log = ''
        return self.name

    def open(self, param):
        self.name = param


if __name__ == "__main__":
    editor = TextEditor()
    editor.root.protocol("WM_DELETE_WINDOW", editor.on_closing)
    editor.mainloop()
