from Constants import *
from PlayerProfile import createPlayerProfile
from LeaderboardGenerators import *
from PlayerProfile import *
from StatGetters import *

#This file controls the main I/O Experiance for the User, it will promt the user and ask what they would like to do in regards to inputs
#viewing, or making a player profile, and then it will execute this, by calling any of the other methods in the other files as
#nessassary

#This is the main bulk of the code, it culminates all of the previous functions 
#into the user inputted choices, this is the method that gets user inputs and does all 
#of the database scraping and saving for this program to work.
def RunKartniteStats(version, contributors):
### Patrick Marinich December 2021

  #constants
  VERSION_NUMBER = version
  CONTRIBUTORS = contributors



  #imports
  import pandas as pd
  #from google.colab import auth
  import gspread
  from gspread_dataframe import get_as_dataframe, set_with_dataframe
  from google.auth import default
  from pydrive.auth import GoogleAuth
  
  gc = gspread.oauth()

  # Puts the google sheet into a python object, we will be calling the sh object after a selection is made
  sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1G0z4XeBjG7Q_Zk_uPtV4v8BPkVT8GD9pmsuk7VIwFKc/edit#gid=1608384215')

  #Track Dictionary, all track names and nicknames go here
  #track indexes are starting at 0 in the mushroom cup ending at 31 at N64 Bowsers castle, +32 for Lava Lake
  TrackIndex = {"Luigi Circuit":0,
  "Moo Moo Meadows":1,
  "Mushroom Gorge":2,
  "Toad's Factory":3,
  "Mario Circuit":4,
  "Coconut Mall":5,
  "DK Summit":6,
  "Wario's Gold Mine":7,
  "Daisy Circuit":8,
  "Koopa Cape":9,
  "Maple Treeway":10,
  "Grumble Volcano":11,
  "Dry Dry Ruins":12,
  "Moonview Highway":13,
  "Bowser's Castle":14,
  "Rainbow Road":15,
  "GCN Peach Beach":16,
  "DS Yoshi Falls":17,
  "SNES Ghost Valley 2":18,
  "N64 Mario Raceway":19,
  "N64 Sherbet Land":20,
  "GBA Shy Guy Beach":21,
  "DS Delfino Square":22,
  "GCN Waluigi Stadium":23,
  "DS Desert Hills":24,
  "GBA Bowser's Castle 3":25,
  "N64 DK's Jungle Parkway":26,
  "GCN Mario Circuit":27,
  "SNES Mario Circuit 3":28,
  "DS Peach Gardens":29,
  "GCN DK Mountain":30,
  "N64 Bowser's Castle":31,
  "Lava Lake":32 }

#for nicknames 
  NickNameIndex= {"Luigi":"Luigi Circuit",
   "moo moo": "Moo Moo Meadows",
   "Moo Moo": "Moo Moo Meadows",
   "Gorge":"Mushroom Gorge",
   "gorge":"Mushroom Gorge",
   "toads":"Toad's Factory",
   "Toads":"Toad's Factory",
   "toads factory": "Toad's Factory",
   "mario circuit": "Mario Circuit",
   "coconut mall":"Coconut Mall",
   "coconut":"Coconut Mall",
   "summit":"DK Summit",
   "Summit":"DK Summit",
   "gold mine":"Wario's Gold Mine",
   "Gold Mine":"Wario's Gold Mine",
   "koopa": "Koopa Cape",
   "Koopa": "Koopa Cape",
   "maple":"Maple Treeway",
   "Maple":"Maple Treeway",
   "grumble":"Grumble Volcano",
   "Grumble":"Grumble Volcano",
   "Dry Dry":"Dry Dry Ruins",
   "dry dry":"Dry Dry Ruins",
   "Moonview":"Moonview Highway",
   "moonview":"Moonview Highway",
   "BC Wii":"Bowser's Castle",
   "bc wii":"Bowser's Castle",
   "BC wii":"Bowser's Castle",
   "rainbow road":"Rainbow Road",
   "rainbow":"Rainbow Road",
   "Rainbow":"Rainbow Road",
   "Peach Beach":"GCN Peach Beach",
   "peach beach":"GCN Peach Beach",
   "yoshi falls":"DS Yoshi Falls",
   "Yoshi Falls":"DS Yoshi Falls",
   "Ghost Valley":"SNES Ghost Valley 2",
   "ghost valley":"SNES Ghost Valley 2",
   "mario raceway":"N64 Mario Raceway",
   "raceway": "N64 Mario Raceway",
   "Raceway": "N64 Mario Raceway",
   "Sherbet Land":"N64 Sherbet Land",
   "sherbet land":"N64 Sherbet Land",
   "Shy Guy Beach":"GBA Shy Guy Beach",
   "shy guy beach":"GBA Shy Guy Beach",
   "Shy Guy":"GBA Shy Guy Beach",
   "shy guy":"GBA Shy Guy Beach",
   "Delfino Square":"DS Delfino Square",
   "delfino square":"DS Delfino Square",
   "Delfino":"DS Delfino Square",
   "delfino":"DS Delfino Square",
   "Waluigi Stadium":"GCN Waluigi Stadium",
   "waluigi stadium":"GCN Waluigi Stadium",
   "Waluigi":"GCN Waluigi Stadium", 
   "waluigi":"GCN Waluigi Stadium",
   "Desert Hills":"DS Desert Hills",
   "desert hills":"DS Desert Hills",
   "GBA 3":"GBA Bowser's Castle 3",
   "gba 3":"GBA Bowser's Castle 3",
   "BC3":"GBA Bowser's Castle 3",
   "bc3":"GBA Bowser's Castle 3",
   "Parkway":"N64 DK's Jungle Parkway",
   "parkway":"N64 DK's Jungle Parkway",
   "GCN mario circuit":"GCN Mario Circuit",
   "GCN mario":"GCN Mario Circuit",
   "gcn mario":"GCN Mario Circuit",
   "GCN Mario":"GCN Mario Circuit",
   "SNES 3":"SNES Mario Circuit 3",
   "snes 3":"SNES Mario Circuit 3",
   "Peach Gardens":"DS Peach Gardens",
   "peach gardens":"DS Peach Gardens",
   "DK Mountain": "GCN DK Mountain",
   "dk mountain": "GCN DK Mountain",
   "mountain": "GCN DK Mountain",
   "Mountain": "GCN DK Mountain",
   "BC64":"N64 Bowser's Castle",
   "bc64":"N64 Bowser's Castle",
   "bc 64":"N64 Bowser's Castle",
   "N64BC":"N64 Bowser's Castle",
   "n64bc":"N64 Bowser's Castle"}

  #Below is the logic for asking a user what they would like to do
  ########


  #displaying inputs for the user
  print('Welcome to Kartnite Stats ' ,VERSION_NUMBER , "\nDeveloped by:", CONTRIBUTORS, '\n')
  print('Below are the options, type the number of the option you would like')
  print('1. Email A Player Profile\n2. Test Something New')
 
  selection = input('What Would You Like To Do: ')
  
  #Generate the PDF for the player or players
  if selection == '1':
    #generates a pdf profile of the inputted players stats for viewing pleasure
    print('Generate a player Report below by entering their name, and your email infromation')
    players = input('Player Name: ')
    email = input('Enter Your Email:')
    password = input('Password: ')
    message = input('Message for the email:')
    all_time = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nolol4P63e7WY-wRPnogcePkWuPPE3JF6QBRgXgF8gE/edit#gid=524408434')
    
    #allows for all players reports to be generated at once
    if players == 'all' or players == 'All' or players == 'ALL':
      racers = ['Pat', 'Kevin', 'Demitri', 'Chris', 'Joe']
      for player in racers:
        HTML = createPlayerProfile(sh,all_time,player,TrackIndex)
        generatedFile = convertHTMLtoPDF(HTML)
        sendReport(player,email,password,message,generatedFile)
    else:
        player = players
        HTML = createPlayerProfile(sh,all_time,player,TrackIndex)
        generatedFile = convertHTMLtoPDF(HTML)
        sendReport(player,email,password,message,generatedFile)

  
  #put any test leaderboards or stats here to make sure that they work as expected before they go into the pdf
  elif selection == '2':
    kvr = sh.worksheet('KVR Stats').get_all_values()
    dfKVR = pd.DataFrame(kvr[1:],columns = kvr[0])
    text = make_line_plot(dfKVR,'Pat')
    print(text)


  #invalid selection
  else: 
    print('invalid selection restart the program')






