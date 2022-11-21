from InputFunctions import *
from Constants import *
from Kartnite_Python.PlayerProfile import createPlayerProfile
from LeaderboardGenerators import *
from PlayerProfile import *
from SeasonReset import *
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
  print('1. Input a Race \n2. Edit A Singular Score \n3. Enter A Grand Prix Winner \n4. Enter Shock Dodges \n5. Enter Blue Shell Stats \n6. View Leaderboards \n7. View All Databases \n8. View Track Records \n9. View Player Stats  \n10. View All Current Track MVPs \n11. View Player All-Time Stats \n12. View All Time Track MVPs \n13. View All Time Leaderboards \n14. Email A Player Profile\n')
 
  selection = input('What Would You Like To Do: ')
  
  #selection logic
  
  #depending on the user selection it will ask for different inputs, and load the nessassary databases needed for that operation

  #input a race
  if selection == '1':
    print('Warining: track and racer names must be formatted correctally \nTrack names must match their full name or a registered nickname \nRacer names must have their first letter capital')
    Track = input("Name of Track: ")
    if Track in NickNameIndex:
      Track = NickNameIndex[Track]
    Racers = input("Names of Racers: ")
    Scores = input("Scores:")
    #loading statment
    print("\nYour selection of", selection, "is loading...." )
    print('\n\n')
    kartData = sh.worksheet('Total Scores').get_all_values()
    RaceCount = sh.worksheet('Race Count').get_all_values()
    KartScore = sh.worksheet('Owned Score').get_all_values()
    Placement = sh.worksheet('Placement Stats').get_all_values()
    dfScores = pd.DataFrame(kartData[1:], columns=kartData[0])
    dfRaceCount = pd.DataFrame(RaceCount[1:], columns = RaceCount[0])
    dfKartScore = pd.DataFrame(KartScore[1:], columns = KartScore[0])
    dfPlacement = pd.DataFrame(Placement[1:], columns = Placement[0])
    inputRace(dfScores,dfRaceCount, dfKartScore, dfPlacement, Track,Racers,Scores,TrackIndex)
 
 #edit a score
  elif selection == '2':
    print('Edit A Score is used to fix an error that may have occured while entering a race \nUse a positive number to increase a score, and a negative to decrease \nUse the net change you want to make as the value')
    Track = input("Name of Track: ")
    if Track in NickNameIndex:
      Track = NickNameIndex[Track]
    Racer = input("Names of Racer: ")
    Score = input("Score: ")
    print("\nYour selection of", selection, "is loading...." )
    print('\n\n')
    kartData = sh.worksheet('Total Scores').get_all_values()
    dfScores = pd.DataFrame(kartData[1:], columns=kartData[0])
    editAScore(dfScores, Track, Racer, Score,TrackIndex)

  #enter a winner
  elif selection == '3':
    Player = input("Winning Player: ")
    print("\nYour selection of", selection, "is loading...." )
    print('\n')
    Wins = sh.worksheet('GP Wins').get_all_values()
    dfWins = pd.DataFrame(Wins[1:], columns = Wins[0])
    enterWinner(dfWins, Player)
   
  #enter a dodge
  elif selection == '4':
    Player = input("Player Name: ")
    Count = input("How Many Dodges: ")
    print("\nYour selection of", selection, "is loading...." )
    print('\n')
    Shock = sh.worksheet('Shock Dodges').get_all_values()
    dfShock = pd.DataFrame(Shock[1:], columns = Shock[0])
    enterDodges(dfShock,Player,Count)


  elif selection == '5':
    Player = input("Player Name: ")
    hit = input("How Many times where they hit by a blue shell? ")
    dodge = input("How many did they dodge? ")
    print("\nYour selection of", selection, "is loading...." )
    print('\n')
    
    BlueShells = sh.worksheet("Blue Shells").get_all_values()
    dfBlueShell = pd.DataFrame(BlueShells[1:], columns = BlueShells[0])

    addBlueShells(dfBlueShell, Player, hit, dodge)

   #leaderboards
  elif selection == '6':
    print("\nYour selection of", selection, "is loading...." )
    kartData = sh.worksheet('Total Scores').get_all_values()
    RaceCount = sh.worksheet('Race Count').get_all_values()
    Wins = sh.worksheet('GP Wins').get_all_values()
    Shock = sh.worksheet('Shock Dodges').get_all_values()
    KartScore = sh.worksheet('Owned Score').get_all_values()
    Blue = sh.worksheet('Blue Shells').get_all_values()
    Placement = sh.worksheet('Placement Stats').get_all_values()

    dfKartScore = pd.DataFrame(KartScore[1:], columns = KartScore[0])
    dfScores = pd.DataFrame(kartData[1:], columns=kartData[0])
    dfRaceCount = pd.DataFrame(RaceCount[1:], columns = RaceCount[0])
    dfWins = pd.DataFrame(Wins[1:], columns = Wins[0])
    dfShock = pd.DataFrame(Shock[1:], columns = Shock[0])
    dfBlue = pd.DataFrame(Blue[1:], columns = Blue[0])
    dfPlacement = pd.DataFrame(Placement[1:], columns = Placement[0])
    print('\n\n')
   
    print('Seeding Leaderboard')
    getSeedings(sh,TrackIndex)
    print('\nPoints Per Race Leaderboard')
    getPointsPerRace(dfScores,dfRaceCount,TrackIndex)
    print('\nTotal Races Played')
    getRaceCountLeaderbaords(dfRaceCount, TrackIndex)
    print('\nGP Wins')
    getGPWinsLeaderboard(dfWins)
    print('\nShock Dodges')
    getShockDodges(dfShock)
    print('\n Blue Shells')
    getBlueLeaderboard(dfBlue)
    print('\n Getting Placement Stats')
    getPlacementLeaderboards(dfPlacement)
 
  #print all data
  elif selection == '7':
    print("\nYour selection of", selection, "is loading...." )
    kartData = sh.worksheet('Total Scores').get_all_values()
    RaceCount = sh.worksheet('Race Count').get_all_values()
    Wins = sh.worksheet('GP Wins').get_all_values()
    Shock = sh.worksheet('Shock Dodges').get_all_values()
    dfScores = pd.DataFrame(kartData[1:], columns=kartData[0])
    dfRaceCount = pd.DataFrame(RaceCount[1:], columns = RaceCount[0])
    dfWins = pd.DataFrame(Wins[1:], columns = Wins[0])
    dfShock = pd.DataFrame(Shock[1:], columns = Shock[0])
    

    print('\nDatabase of total scores')
    print(dfScores)
    print('\nDatabase of Race Count')
    print(dfRaceCount)
    print('\nDatabase GP Wins')
    print(dfWins)
    print('\nDatabase of Shock Dodges')
    print(dfShock)
  #track data
  elif selection == '8':
    Track = input("Name of Track: ")
    if Track in NickNameIndex:
      Track = NickNameIndex[Track]
    print("\nYour selection of", selection, "is loading...." )
    print("\n\n")
    kartData = sh.worksheet('Total Scores').get_all_values()
    RaceCount = sh.worksheet('Race Count').get_all_values()
    dfScores = pd.DataFrame(kartData[1:], columns=kartData[0])
    dfRaceCount = pd.DataFrame(RaceCount[1:], columns = RaceCount[0])
    GetTrackData(dfScores,dfRaceCount,Track,TrackIndex)
  
  #racer data
  elif selection == '9':
    Racer = input("Name of Racer: ")
    print("\nYour selection of", selection, "is loading...." )
    print("\n\n")

    kartData = sh.worksheet('Total Scores').get_all_values()
    RaceCount = sh.worksheet('Race Count').get_all_values()
    Wins = sh.worksheet('GP Wins').get_all_values()
    Shock = sh.worksheet('Shock Dodges').get_all_values()
    KartScore = sh.worksheet('Owned Score').get_all_values()
    Blue = sh.worksheet('Blue Shells').get_all_values()
    dfKartScore = pd.DataFrame(KartScore[1:], columns = KartScore[0])
    dfScores = pd.DataFrame(kartData[1:], columns=kartData[0])
    dfRaceCount = pd.DataFrame(RaceCount[1:], columns = RaceCount[0])
    dfWins = pd.DataFrame(Wins[1:], columns = Wins[0])
    dfShock = pd.DataFrame(Shock[1:], columns = Shock[0])
    dfBlue = pd.DataFrame(Blue[1:], columns = Blue[0])
    
    getPlayerStats(dfScores, dfRaceCount, dfWins, dfShock, dfKartScore, dfBlue, Racer, TrackIndex)
 
  #All Track MVPs
  elif selection == '10':
    print("\nYour selection of", selection, "is loading...." )
    print('\n')
    kartData = sh.worksheet('Total Scores').get_all_values()
    RaceCount = sh.worksheet('Race Count').get_all_values()
    dfScores = pd.DataFrame(kartData[1:], columns=kartData[0])
    dfRaceCount = pd.DataFrame(RaceCount[1:], columns = RaceCount[0])
    print("Displaying all track MVPs...\n")

    getAllTrackOwners(dfScores,dfRaceCount,TrackIndex)

  elif selection == 'reset':
    answer = input("Are you sure you want to end the current season? ")
    
    if answer == 'yes' or answer == 'YES':
      #open up all time sheet
      change = 0
      all_time = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nolol4P63e7WY-wRPnogcePkWuPPE3JF6QBRgXgF8gE/edit#gid=524408434')
      print("Ending Season....")
      #call end of season function
      newPoints,newRaceCount,newWins,newDodge,newOwned,newShells,newSeeds,oldPoints,oldRaceCount,oldWins,oldDodge,oldOwned,oldShells,newPlacement,oldPlacement = end_season(sh,all_time,TrackIndex)
      #prompt to end the season
      save = input("are you sure you want to save? ")
      if save == 'YES' or save == 'yes':
        #if yes set change to = 1
        change = 1
        print('Finializing the data....')
      else:
        print('Canceling Change of Season...')
        print('End of Program')
    else:
      print('Stopping program')
    
  #view the all time stats for a player
  elif selection == '11':
    #gets inputs for player(s)
    Racer = input("Name of Racer (type 'all' to view everybody's): ")
    #output formatting
    print("\nYour selection of", selection, "is loading...." )
    print("\n\n")
    #gets the all time sheet open
    all_time = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nolol4P63e7WY-wRPnogcePkWuPPE3JF6QBRgXgF8gE/edit#gid=524408434')
    
    #calls the function for all time stats
    getAllTimeStats(sh,all_time,Racer,TrackIndex)
  
  #prints the all time track owners
  elif selection == '12':
    print("\nYour selection of", selection, "is loading...." )
    print('\n\nDisplaying the All Time Best Player for Each Track')
    print('Note there is a', RACE_MINIMUM, 'race minimum to be considered\n')
    all_time = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nolol4P63e7WY-wRPnogcePkWuPPE3JF6QBRgXgF8gE/edit#gid=524408434')

    #opens, creates and combines the nessassary sheets
    #opens
    kartData = sh.worksheet('Total Scores').get_all_values()
    RaceCount = sh.worksheet('Race Count').get_all_values()
    kartDataAllTime = all_time.worksheet('Total Scores').get_all_values()
    RaceCountAllTime = all_time.worksheet('Race Count').get_all_values()
    #create
    dfSeasonScores = pd.DataFrame(kartData[1:], columns=kartData[0])
    dfSeasonRaceCount = pd.DataFrame(RaceCount[1:], columns = RaceCount[0])
    dfAllTimeScores = pd.DataFrame(kartDataAllTime[1:], columns=kartDataAllTime[0])
    dfAllTimeRaceCount = pd.DataFrame(RaceCountAllTime[1:], columns = RaceCountAllTime[0])

    dfAllTimeScores = dfAllTimeScores[dfAllTimeScores.columns.difference(["Tracks x Players"])]
    players = dfAllTimeScores.columns
    for player in players:
    #combines
      for track in TrackIndex:
        dfAllTimeScores.loc[TrackIndex[track], player] = int(dfAllTimeScores.at[TrackIndex[track], player]) + int(dfSeasonScores.at[TrackIndex[track], player])
        dfAllTimeRaceCount.loc[TrackIndex[track], player] = int(dfAllTimeRaceCount.at[TrackIndex[track], player]) + int(dfSeasonRaceCount.at[TrackIndex[track], player])

    #function call
    getAllTimeAllTrackOwners(dfAllTimeScores,dfAllTimeRaceCount,TrackIndex)


  #prints the all time leaderboards
  elif selection == '13':
    print("\nYour selection of", selection, "is loading...." )
    print('\n\nDisplaying the All Time Leaderboards')
    all_time = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nolol4P63e7WY-wRPnogcePkWuPPE3JF6QBRgXgF8gE/edit#gid=524408434')
    #calls the function
    getAllTimeLeaderboads(sh,all_time,TrackIndex)


  #generates a pdf profile of the inputted players stats for viewing pleasure
  elif selection == '14':
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

   
 #invalid selection
  else: 
    print('invalid selection restart the program')



  ##COMMENT THIS OUT WHEN TESTING

  #upadates the google sheet, a psyudo save of the data
  TotalScores = sh.worksheet('Total Scores')
  RaceCount = sh.worksheet('Race Count')
  WinCount = sh.worksheet('GP Wins')
  Shock = sh.worksheet('Shock Dodges')
  KartScore = sh.worksheet('Owned Score')
  BlueShells = sh.worksheet('Blue Shells')
  Placement = sh.worksheet('Placement Stats')
  
  #saves to the google sheet if nessassary, depending on the input of the user
  #saves if enter a race
  if selection =='1':
    set_with_dataframe(TotalScores, dfScores)
    set_with_dataframe(RaceCount,dfRaceCount)
    set_with_dataframe(KartScore,dfKartScore)
    set_with_dataframe(Placement,dfPlacement)
    print("Success - The Database Has Been Updated")
  #saves if edit a score
  elif selection =='2':
    set_with_dataframe(TotalScores, dfScores)
    print("Success - The Database Has Been Updated")
 #saves when winner added
  elif selection =='3':
    set_with_dataframe(WinCount,dfWins)
    print("Success - The Database Has Been Updated")
  #saves when shock dodges are counted
  elif selection =='4':
    set_with_dataframe(Shock,dfShock)
    print("Success - The Database Has Been Updated")
  elif selection  == '5':
    #saves the data for blue shells
    set_with_dataframe(BlueShells,dfBlueShell)
    print("Success - The Database Has Been Updated")

  elif selection == 'reset':
    if change == 1:
      #opens up the all time list
      print("Saving All-Time Stats")
      aTotalScores = all_time.worksheet('Total Scores')
      aRaceCount = all_time.worksheet('Race Count')
      aWinCount = all_time.worksheet('GP Wins')
      aShock = all_time.worksheet('Shock Dodges')
      aKartScore = all_time.worksheet('Owned Score')
      aBlueShells = all_time.worksheet('Blue Shells')
      aSeeds = all_time.worksheet("All-Time Seeding")
      aPlacement = all_time.worksheet("Placement Stats")
      #saves the data for the all time list
      set_with_dataframe(aTotalScores,newPoints)
      set_with_dataframe(aRaceCount,newRaceCount)
      set_with_dataframe(aWinCount,newWins)
      set_with_dataframe(aShock,newDodge)
      set_with_dataframe(aKartScore,newOwned)
      set_with_dataframe(aBlueShells,newShells)
      set_with_dataframe(aSeeds,newSeeds)
      set_with_dataframe(aPlacement,newPlacement)



      #sets all od the old ones to 0
      print("Resetting Season Stats...")
      set_with_dataframe(TotalScores, oldPoints)
      set_with_dataframe(RaceCount,oldRaceCount)
      set_with_dataframe(KartScore,oldOwned)
      set_with_dataframe(WinCount,oldWins)
      set_with_dataframe(Shock,oldDodge)
      set_with_dataframe(BlueShells,oldShells)
      set_with_dataframe(Placement,oldPlacement)

      print("The Seasonal Stats have been successfully merged into the All-Time Stats")
      print("Time for a new season to begin!")

