#This file contains the functions nessassary to reset the season whenever seen fit. Typically the seasons that we currently play are 
#summer and winter since we are at school during the spring and fall. These methods clear the seasonal stats and move them into the all 
#time database

from LeaderboardGenerators import *
from StatGetters import *

import pandas as pd
from pandas.core.dtypes.cast import sanitize_to_nanoseconds


#this code takes in the name of the files, and then the sheet name, and then transfers all the data
#moves the data from old to the new sheet
def transfer_data(old,new,name):
  oldKart = old.worksheet(name).get_all_values()
  newKart= new.worksheet(name).get_all_values()
  dfOldKart = pd.DataFrame(oldKart[1:], columns = oldKart[0])
  dfNewKart = pd.DataFrame(newKart[1:], columns = newKart[0])

  #deleats first column
  colList = dfOldKart.columns.values.tolist()
  del colList[0]
 
  #iterates through the sheets
  for col in colList:
    for row in dfOldKart.index:
        dfNewKart.at[row,col] = int(dfNewKart.at[row,col]) + int(dfOldKart.at[row,col])
        #clears the old stats
        dfOldKart.at[row,col] = 0
 
  return dfNewKart,dfOldKart


#This function will take all of the seasonal stats that have been aquired, 
#increment them into the all time sheet, and the reset the season for the next use
def end_season(season, all_time,TrackIndex):
  #season is the sheet for the current season
  #all time is the all time stats'

  #first get the seeding points and then update the kart sheet
  dfFinalRanks = getSeedings(season,TrackIndex)

  #find the score of each player using the decided algorythem, and then 
  #increment this score with the all time score
  
  totalScores = 0
  #get the total points,
  for index in dfFinalRanks.index:
    totalScores += dfFinalRanks.at[index,'Kart Score']

  
  #make a new leaderboard, and then add all the players to it with their new scores:
  dfSeasonScores = pd.DataFrame({'Player': [], 'Season Score':[]})
  for index in dfFinalRanks.index:
    #make score percent of score of the total:
    score = (int(dfFinalRanks.at[index,'Kart Score']) / totalScores) * 100
    #multiplier for placements
    if(index == 0):
      score *= 1.25
    elif(index == 1):
      score *= 1.125
    elif(index == 2):
      score *= 1.05

    dfSeasonScores.at[index] = [dfFinalRanks.at[index,'Player'],score]
    
  print("Below are the Final Scores Normalized for the Season")
  print(dfSeasonScores)


  #adds the new df to the all time scoring sheet
  all_timeScores= all_time.worksheet('All-Time Seeding').get_all_values()
  dfAll_timeScores = pd.DataFrame(all_timeScores[1:], columns = all_timeScores[0])  


  print('Updating All Time Seeding....')
  print('Diminishing Old Seasons by 15%...')
  print('Incrementing The New Seasons Scores...')
  
  for index in dfSeasonScores.index:
    player = dfSeasonScores.at[index,'Player']

  
    dfAll_timeScores.at[0,player] = (float(dfAll_timeScores.at[0,player])*.85) + float(dfSeasonScores.at[index,'Season Score'])

  #increments the all time stats with the seasonal stats, and then clears all of the seasonal stats

  #calls the transfer function on points score
  newPoints,oldPoints = transfer_data(season,all_time,'Total Scores')
  
  #calls it for the race count
  newRaceCount,oldRaceCount = transfer_data(season,all_time,'Race Count')

  #GP Wins
  newWins,oldWins = transfer_data(season,all_time,'GP Wins')

  #Shock Dodges
  newDodge,oldDodge = transfer_data(season,all_time,'Shock Dodges')

  #races owned
  newOwned,oldOwned = transfer_data(season,all_time,'Owned Score')

  #blue Shells
  newShells,oldShells = transfer_data(season,all_time,'Blue Shells')


  return newPoints,newRaceCount,newWins,newDodge,newOwned,newShells,dfAll_timeScores,oldPoints,oldRaceCount,oldWins,oldDodge,oldOwned,oldShells

 



 