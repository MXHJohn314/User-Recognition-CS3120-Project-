from tkinter import *
import tkinter as tk
from tkinter import messagebox
import re
import os
import time
from datetime import datetime

bad_keys = {'XF86AudioPlay', 'XF86AudioLowerVolume', 'Win_L', 'Win_R',
            'XF86AudioRaiseVolume', 'XF86AudioMute',  'Shift_L',
            'Shift_R', 'Escape', 'Delete', 'Left', 'Up', 'Down',
            'Right', 'Home', 'Prior', 'End', 'Next', 'Insert', 'App',
            'Control_L', 'Control_R', 'Alt_L', 'Alt_R'}


def change_color(txt, name, c):
    txt.tag_configure(name, foreground=c['fg'], background=c['bg'])


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        logger.close()
        editor.root.destroy()


class TextEditor:
    def __init__(self, _logger):
        self.logger = _logger
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
        self.root.geometry("600x470+200+125")
        self.prompt = Text(height=14, font=("Arial", 10))
        self.txt_in = Text(height=14, font=("Arial", 10))
        self.btn = tk.Button(self.root, text="Generate Prompt", command=self.generate_prompt)
        self.generate_prompt()
        self.size = self.prompt.index(self.prompt.index(f'end-1c'))
        self.prev = None
        self.root.bind('<Key>', self.check_text)
        self.root.bind('<KeyRelease>', self.logger.log_release)

    def generate_prompt(self):
        with open('prompt.txt', 'r') as file:
            prompt = file.read()
            file.close()
        self.prompt.insert(1.0, prompt)
        self.prompt.config(wrap=WORD, exportselection=0, insertbackground='white', state='disabled')
        self.prompt.tag_add('', '1.0', END)
        change_color(self.prompt, '', self.colors['black'])
        self.prompt.pack()
        self.txt_in.pack()
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
        for j in [self.txt_in, self.prompt]:
            for i in ['<Control-a>', '<Control-x>', '<Control-c>', '<Control-v>', '<Button-3>',
                      '<Button-2>']:
                j.bind(i, lambda _e: 'break')
        self.txt_in.config(wrap=WORD, exportselection=0)

    def check_text(self, e):
        if e.state and e.state != 0x0001 or e.keysym in bad_keys:
            return
        key = e.char
        print(f"e='{key}'")
        current = self.tags2[self.txt_in.index(INSERT)]
        if self.prev and current != self.prev:
            prev_s, prev_e = self.prev.split('-')
            check = self.txt_in.get(prev_s, prev_e) == self.prompt.get(prev_s, prev_e)
            c = self.colors['blue'] if check else self.colors['red']
            self.txt_in.tag_remove(self.prev, prev_s, prev_e)
            self.txt_in.tag_add(self.prev, prev_s, prev_e)
            self.txt_in.config(state='normal')
            change_color(self.txt_in, self.prev, c)
            change_color(self.prompt, self.prev, self.colors['black'])
        change_color(self.prompt, current, self.colors['white'])
        self.prev = current
        self.prompt.config(state='disabled')
        self.logger.log_press(e.keysym, 1)
        if self.size == self.txt_in.index(self.txt_in.index(f'end-1c')):
            tk.messagebox.showinfo("Done", "Thanks for participating!")
            self.root.destroy()
            return 0

    def mainloop(self):
        self.root.mainloop()


class Logger:
    def __init__(self):
        self.t_array = ['Y', 'm', 'D', 'H', 'M', 'S']
        self.mods = ['shift', 'ctrl', 'alt', 'windows']
        self.check = None
        csv = 'pylogs.csv'
        if not (os.path.exists(csv) and os.path.isfile(csv)):
            self.file = open(f'{csv}', 'w')
            self.file.write('year,month,day,hour,minute,sec,millis,isDown,key\n')
        else:
            self.file = open(f'{csv}', 'a')
        self.presses = {}

    def log_press(self, key, result):
        t = datetime.now()
        if key in self.presses:
            return
        row = self.format_row(key, t)
        self.presses[key] = [row]
        if result == 0:
            self.close()

    def format_row(self, key, t):
        millis = int((time.mktime(t.timetuple()) + t.microsecond / 1E6) * 1000) % 1000
        time_str = ','.join([f'{t.strftime("%" + i)}' for i in self.t_array])
        row = f'{time_str},{millis},1,{key}\n'
        return row

    def log_release(self, event):
        t = datetime.now()
        key = event.char
        if key not in self.presses:
            return
        self.presses[key].append(self.format_row(key, t))
        both_rows = ''.join(self.presses[key])
        if self.file.closed:
            self.file = open('pylogs.csv')
        self.file.write(both_rows)
        del self.presses[key]

    def close(self):
        self.file.close()


if __name__ == "__main__":
    logger = Logger()
    editor = TextEditor(logger)
    editor.root.protocol("WM_DELETE_WINDOW", on_closing)
    editor.mainloop()
