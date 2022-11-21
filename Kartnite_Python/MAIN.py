#This is where the program should be run, it will call the I/O Method and then go to work depending on what the user inputs

#This is now the cell you need to run the program
#The old main cell was redefined from the main cell to the singular method below
#This is to reduce the amount of scrolling needed when inputing or viewing the data

from InputOutput import *
from Constants import *
#RUNS THE ENTIRE PROGRAM :)

#credentials for loading must be stored in this file, if you need the credentials ask pat and he can send them

#they must be stored at this place in your filesystem
# ..\%APPDATA%\gspread\credentials.json


RunKartniteStats(VERSION,CONTRIBUTORS)