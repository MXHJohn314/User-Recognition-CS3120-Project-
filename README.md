# CS_3120_Project

A user-recognition project powered by keyboard input data. This program uses features discerned from data collected by volunteers. Our processes will explore several elementary techniques of machine learning.
                
## Want to become a volunteer?

We would really appreciate it! [See the official documentation here](https://github.com/GalacticWafer/CS_3120_Project/blob/main/getting_started/GETTING_STARTED.md)

## User Data and Privacy

### It's a big deal

<p>
We take the safety of all volunteers very seriously. Several precautions are taken to maintain this privacy.

- No data sets will be available on this repo
- Only text editors and IDEs and communication apps (Teams, Zoom, Discord, Slack) are allowed to 
  log keystrokes
- The keylogger can be conveniently turned off at any time from the Windows taskbar


This repository merely acts as a storage for code that can be used to demonstrate how to identify users based on the way that they type. 
</p>

### Data Collection

<p>
Although the machine learning processes are exclusively done in Python, we use a scripting language called AutoHotkey to record keystrokes and the time they occurred in the form of csv files. Here is a list of all the types of data we collect:

- When a key was held down
- When a key was released
- Which modifiers were held (control, alt, windows, and shift)

All time accuracies are expressed in milliseconds.
</p>
<p>
We encourage volunteers to check out this simple automation language for the Windows environment. Learn more about AutoHotkey here:

https://www.autohotkey.com/

We have included the source code for our keylogger [here](/keylogger.ahk) if anyone would like to run the program from source for themselves.
</p>
<p>
For the security of the user, this program will only collect 	keystrokes from the following programs:

- VS Code
- Spyder
- IntelliJ
- PyCharm
- Webstorm
- CLion
- Notepad
- Notepad++
- Sublime Text
- Microsoft Word
- Microsoft Teams
- Zoom
- Slack
- Discord
</p>

## Maintainers

- Malcolm Johnson https://galacticwafer.github.io
- Adam Wojdyla https://github.com/awojdyla89
