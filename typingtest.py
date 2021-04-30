from tkinter import *
import tkinter as tk
from tkinter import messagebox
import re
import time

specials = ['less', 'BackSpace', 'space', 'Caps_Lock']
shifts = {'Shift_L': '0', 'Shift_R': '0'}
bad_keys = {'XF86AudioPlay', 'XF86AudioLowerVolume', 'Win_L', 'Win_R',
            'XF86AudioRaiseVolume', 'XF86AudioMute', 'Shift_L',
            'Shift_R', 'Escape', 'Delete', 'Left', 'Up', 'Down',
            'Right', 'Home', 'Prior', 'End', 'Next', 'Insert', 'App',
            'Control_L', 'Control_R', 'Alt_L', 'Alt_R'}



def shift_check(e):
    shifts[e.keysym] = '1' if '2' == e.type else '0'


def change_color(txt, name, color):
    txt.tag_configure(name, foreground=color['fg'], background=color['bg'])


class TextEditor:
    def __init__(self):
        self.prompt_ranges = self.prompt_words = self.size = self.current = None
        self.reg = re.compile(r'(\s+|\S+)')
        self.prev_words = self.next_words = []
        self.logger = Logger()
        self.clrs = {
            'white': {'bg': 'black', 'fg': 'white'},
            'black': {'bg': 'white', 'fg': 'black'},
            'grey': {'bg': 'white', 'fg': 'grey'},
            'red': {'bg': 'red', 'fg': 'white'},
            False: {'bg': 'red', 'fg': 'white'},
            'blue': {'bg': 'lightblue', 'fg': 'black'},
            True: {'bg': 'lightblue', 'fg': 'black'},
        }
        self.root = Tk()
        self.current = 0
        self.root.title("Typing Test")
        # self.root.geometry("600x470+200+125")
        self.prompt = Text(height=14, font=("Arial", 10))
        self.txt_in = Text(height=14, font=("Arial", 10))
        self.btn = tk.Button(self.root, text="Generate Prompt", command=self.generate_prompt)
        self.generate_prompt()
        messagebox.showinfo('Get Ready!', 'The test will begin now.', parent=self.txt_in)
        self.txt_in.focus_force()
        chars = [_ for _ in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-=`~!@#$%^&*()_+[{]}\\|\'\";:,./?>"]
        self.root.bind('<Key>', self.check_text)
        self.root.bind('<KeyRelease>', lambda e: self.logger.log_release(e, ','.join(shifts.values())))
        [self.root.bind(i, self.check_text) for i in chars]
        [self.root.bind(_, shift_check) for _ in ['<Shift_R>', '<Shift_L>', '<KeyRelease-Shift_L>', '<KeyRelease-Shift_R>']]
        [self.root.bind(_, self.txt_in.mark_set(INSERT, 'end-1c')) for _ in ['<Button-1>', '<Button-2>', '<Button-3>']]
        [self.root.bind(i, self.check_text) for i in ['less', 'BackSpace', 'space', 'Caps_Lock']]
        [self.root.bind(f'<KeyRelease-{i}>', self.check_text) for i in specials]
        [self.root.bind(f'<KeyRelease-{i}>', lambda e: self.logger.log_release(e, ','.join(shifts.values()))) for i in specials]
        self.root.bind('Control-v', 'break')

    def generate_prompt(self, txt='train_prompt.txt'):
        self.prompt.config(state='normal')
        self.prompt.delete('1.0', END)
        self.txt_in.delete('1.0', END)
        with open(txt, 'r') as file:
            prompt = file.read().strip()
            file.close()
        self.logger.open(f"{txt.split('.')[0].split('_')[0]}.csv")
        self.prompt.insert(1.0, prompt)
        self.prompt_words = self.next_words = self.get_words(self.prompt)
        self.prompt_ranges = self.get_ranges(self.prompt)
        for s, e in self.prompt_ranges:
            self.prompt.tag_add(f'{s}-{e}', s, e)
        self.size = self.prompt.index(self.prompt.index(f'end-1c'))
        '''For testing purposes. Use to shortcut the train
         and test phase to type only the last few chars of each prompt.'''
        self.txt_in.insert(1.0, prompt[: len(prompt) - 35])
        self.prompt.config(wrap=WORD, exportselection=0, insertbackground='white')
        change_color(self.prompt, '', self.clrs['black'])
        self.txt_in.grid(row=2, column=0, padx=10, pady=10)
        self.prompt.grid(row=0, column=0, padx=10, pady=10)
        c = self.get_current()
        change_color(self.prompt, f"{c['s']}-{c['e']}", self.clrs['black'])
        self.txt_in.config(wrap=WORD, exportselection=0)
        self.prompt.tag_add(c['name'], c['s'], c['e'])
        change_color(self.prompt, c['name'], self.clrs['white'])
        self.prompt.config(state='disabled')

    def highlight_typed_words(self, forward, is_space):
        string = self.txt_in.get('1.0', 'end-1c')
        m2 = [_ for _ in re.findall(self.reg, string)]
        txt_in_tags = self.get_ranges(self.txt_in)
        for a, b, (_s, _e) in zip(self.prompt_words, m2, txt_in_tags):
            name = f'{_s}-{_e}' if forward else f'{_s}-{self.txt_in.index(f"{_e}+1c")}'
            ok = self.clrs[a.startswith(b) or a == b]
            self.txt_in.tag_add(name, _s, _e)
            change_color(self.txt_in, f'{_s}-{_e}', ok)
            self.txt_in.tag_configure(name, foreground=ok['fg'], background=ok['bg'])
        if is_space:
            c = self.get_current(len(txt_in_tags) - 2)
            change_color(self.prompt, c['name'], self.clrs['black'])
            self.current += 0 if c['word'].isspace() and self.txt_in.get('end-3c').isspace() else 1
            c = self.get_current(len(txt_in_tags))
            change_color(self.prompt, c['name'], self.clrs['white'])

    def get_ranges(self, t_):
        tags = []
        s_ = '1.0'
        for match in re.finditer(r'(\s+|\S+)', t_.get('1.0', 'end')):
            str_len = match.end() - match.start()
            e_ = t_.index(f'{s_}+{str_len}c')
            tags.append((s_, e_))
            s_ = t_.index(f'{e_}')
        return tags

    def check_text(self, event):
        t = time.time_ns()
        if event.keysym in bad_keys:
            self.txt_in.mark_set(INSERT, 'end-1c')
            return
        self.highlight_typed_words(event.keysym != 'BackSpace', event.keysym == 'space')
        shifts_state = f'{shifts["Shift_L"]},{shifts["Shift_R"]}'
        self.logger.log_press(event.char, shifts_state, t)
        if self.prompt.index(f'{self.size}-1c') == self.txt_in.index(f'{self.size}-1c'):
            if self.logger.close() == 'train.csv':
                messagebox.showinfo('Training Complete', 'Now time for the test prompt.', parent=self.txt_in)
                self.generate_prompt('test_prompt.txt')
                self.txt_in.focus_force()
            else:
                messagebox.showinfo(f'Testing Complete!',
                                    'Thanks for participating! Please contact'
                                    ' Adam Wojdyla or Malcolm Johnson to submit.', parent=self.root)
                self.root.destroy()

    def mainloop(self):
        self.root.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            editor.root.destroy()

    def get_words(self, txt):
        return [_ for _ in re.findall(self.reg, txt.get('1.0', 'end'))]

    def get_current(self, i=0):
        c = self.prompt_ranges[i]
        return {'word': self.prompt_words[i],
                's': c[0], 'e': c[1], 'name': f'{c[0]}-{c[1]}'}


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

    def log_press(self, key, shifts_state, t):
        # print(f'keypress={key}')
        if key in self.presses:
            return
        self.presses[key] = [f'{t},1,{key},{shifts_state}\n']

    def log_release(self, event, shifts_state):
        t = time.time_ns()
        key = event.char
        # print(f'keyrelease={key}')
        if key not in self.presses:
            return
        self.presses[key].append(f'{t},0,{key},{shifts_state}\n')
        self.log += ''.join(self.presses[key])
        del self.presses[key]

    def close(self):
        with open(self.name, 'w') as file:
            file.write('time,isDown,key,l_shift,r_shift\n' + self.log)
        print('time,isDown,key,l_shift,r_shift\n' + self.log + '\n\n')
        self.log = ''
        return self.name

    def open(self, param):
        self.name = param


if __name__ == "__main__":
    editor = TextEditor()
    editor.root.protocol("WM_DELETE_WINDOW", editor.on_closing)
    editor.mainloop()
