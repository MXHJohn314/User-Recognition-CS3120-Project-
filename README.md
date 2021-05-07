# User Recognition (CS_3120_Project)

A user-recognition project powered by keyboard input data. This program uses features discerned 
from data collected by volunteers, and tries to recognize users based on the way they type. Our processes will explore several elementary techniques of machine learning.
                

## Requirements 

- Python 3.7 or higher
- Python Modules:
  - tkinter
  - re
  - time


## Instructions
1. Clone the repo: `https://github.com/GalacticWafer/CS_3120_Project.git`
2. Use your preferred method of running python files to run typingtest.py
   + Note: If you are on a Linux distribution or running a non-standard Python installation, you may need to run `pip install tkinter`
4. When the gui appears, start typing the prompt in the lower half of the window. Just like a typing test, the current word will be highlighted in the top window. Mistakes are highlighted in red. Fix them if you want.

![alt text](https://github.com/GalacticWafer/CS_3120_Project/blob/main/InstructionPictures/Step3.png)

5. There are two prompts to type. One is for model training, the other is for testing.
6. After you complete both tests, send your `train.csv` and `test.csv` to us. You can use Teams if you're connected to us through MSU Denver, or send to one of the email addresses below.


### Troubleshooting
All modules needed are pre-installed unless you're using certain Mac OS or Linux distros, or 
you are using a Python installation older than 3.7. 


- can't find tkinter
  - If you have anaconda (using Anaconda/Spyder IDE): 
    - `conda install tkinter`
  - If you are on linux:
    - `sudo apt-get install python3-tk`
  - If you are on Mac:
    1. If you don't have Xcode command line tools, install those: `xcode-select --install`
    2. `brew install tcl-tk`
    3. `brew install python --with-tcl-tk`



- can't find time (`No matching distribution found for time`)
  - you need to upgrade to python 3.7 or newer.

## Secure Programming
- This program only records keystrokes from the typing test. 
- No other windows are allowed to log keystrokes
- No data sets will be available on this repo
- The program can be conveniently turned off at any time by closing the typing test

We would really appreciate your support.

## Maintainers
- Malcolm Johnson mjohn314@msudenver.edu
- Adam Wojdyla awojdyl2@msudenver.edu 
