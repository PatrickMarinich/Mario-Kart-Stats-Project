from StatGetters import *
import pandas as pd
#This file contains all of the functions that generate different leaderboards for any of the stats

#Gets the shock dodge leaderboard
#by default will print on the concole, but this can be toggeld

def getShockDodges(dfShock, display = True):
  #dataframe without the label
    dfNoLabel = dfShock[dfShock.columns.difference(["Tracks x Players"])]
  #leaderboard object
    dfLeaderboard = pd.DataFrame({'Player': [], 'Shock Dodges':[]})
    counter = 0
    #for each player in dodges
    for player in set(dfNoLabel.columns.values.tolist()):
      #adds the dodges to the leaderboard
      dfLeaderboard.loc[counter] = [player, int(dfNoLabel.at[0, player])]
      counter = counter + 1
      racecount = 0
   
    #sorts and prints the leaderboards
    dfLeaderboard = dfLeaderboard.sort_values(['Shock Dodges', 'Player'],  ascending=[0, 1])
   
    if display == True:
      print(dfLeaderboard)
    
    return dfLeaderboard



#Gets the race count leaderboards

def getRaceCountLeaderbaords(dfRaceCount,TrackIndex, display = True):
  
    #determine the score for each player within the data
    dfNoTracks = dfRaceCount[dfRaceCount.columns.difference(["Tracks x Players"])]
    #leaderboard object
    dfLeaderboard = pd.DataFrame({'Player': [], 'Races Played':[]})
    counter = 0
   
    racecount = 0
    #sets up the scores for each player
    for player in set(dfNoTracks.columns.values.tolist()):
      
      for track in TrackIndex:
        racecount = racecount + int(dfRaceCount.at[TrackIndex[track], player])


      #adds the racecount to the leaderboard
      dfLeaderboard.loc[counter] = [player, racecount]
      counter = counter + 1
      racecount = 0
   
    #sorts and prints the leaderboards
    dfLeaderboard = dfLeaderboard.sort_values(['Races Played', 'Player'],  ascending=[0, 1])
    
    if display == True:
      print(dfLeaderboard)
      
    return dfLeaderboard



#Gets the GP Wins Leaderboard
def getGPWinsLeaderboard(dfWins, display = True):
    #dataframe without the label
    dfNoLabel = dfWins[dfWins.columns.difference(["Tracks x Players"])]

    #leaderboard object
    dfLeaderboard = pd.DataFrame({'Player': [], 'Grand Prix Wins':[]})
    counter = 0
    #for each player in wins
    for player in set(dfNoLabel.columns.values.tolist()):
      #adds the wins to the leaderboard
      dfLeaderboard.loc[counter] = [player, int(dfNoLabel.at[0, player])]
      counter = counter + 1
      racecount = 0
   
    #sorts and prints the leaderboards
    dfLeaderboard = dfLeaderboard.sort_values(['Grand Prix Wins', 'Player'],  ascending=[0, 1])
    if display == True:
      print(dfLeaderboard)
    return dfLeaderboard




#Get the points per race leaderboards

def getPointsPerRace(dfScores,dfRaceCount, TrackIndex, display = True):
  #creates a leaderboard object
  dfLeaderboard = pd.DataFrame({'Player': [], 'Points Per Race': []})
  counter = 0


   #dataframe without the track names
  dfNoTracks = dfScores[dfScores.columns.difference(["Tracks x Players"])]

  #iterates through each player
  for player in set(dfNoTracks.columns.values.tolist()):

    #gets the total points of each player
    totalPoints = 0
    for track in TrackIndex:
      totalPoints = totalPoints + int(dfScores.at[TrackIndex[track],player])
    #gets total racecount
    totalRaces = 0
    for track in TrackIndex:
      totalRaces = totalRaces + int(dfRaceCount.at[TrackIndex[track],player])

    #gets the PPR and then sets it to the approperate place
    
    if (totalRaces != 0):
      PPR = float(totalPoints) / float(totalRaces)
      dfLeaderboard.loc[counter] = [player, PPR]
      counter = counter + 1
    else:
      dfLeaderboard.loc[counter] = [player,0]
      counter = counter + 1
     
    

   #sorts and prints the leaderboard
  dfLeaderboard = dfLeaderboard.sort_values(['Points Per Race', 'Player'], ascending=[0,1]) 
  if display == True:
    print(dfLeaderboard)

  return dfLeaderboard


#Blue shell leaderboards

def getBlueLeaderboard(dfBlue, display = True):
     #dataframe without the label
    dfNoLabel = dfBlue[dfBlue.columns.difference(["Blue Shell"])]
    
    #leaderboard object
    dfLeaderboard = pd.DataFrame({'Player': [], 'Blue Shells':[]})

    counter =0
    #for each player 
    for player in set(dfNoLabel.columns.values.tolist()):
      #adds the blues to the leaderboard
      dfLeaderboard.loc[counter] = [player, int(dfNoLabel.at[0, player]) + int(dfNoLabel.at[1,player])]
      counter = counter + 1
      racecount = 0
   
    #sorts and prints the leaderboards
    dfLeaderboard = dfLeaderboard.sort_values(['Blue Shells', 'Player'],  ascending=[0, 1])
    if display == True:
      print(dfLeaderboard)
    return dfLeaderboard


#Placement leaderbaords for top 1 -> top4 finishes

def getPlacementLeaderboards(dfPlacement, display = True):
    FIRST_ROW = 0
    SECOND_ROW = 1
    THIRD_ROW = 2
    FOURTH_ROW = 3
     
     #dataframe without the label
    dfNoLabel = dfPlacement[dfPlacement.columns.difference(["Placement"])]
    
    #leaderboard object
    dfLeaderboard1 = pd.DataFrame({'Player': [], 'First Places':[]})
    dfLeaderboard2 = pd.DataFrame({'Player': [], 'Top 2 Finishes':[]})
    dfLeaderboard3 = pd.DataFrame({'Player': [], 'Top 3 Finishes':[]})
    dfLeaderboard4 = pd.DataFrame({'Player': [], 'Top 4 Finishes':[]})
    
    counter = 0
    #for each player 
    for player in set(dfNoLabel.columns.values.tolist()):
      #adds the blues to the leaderboard
      dfLeaderboard1.loc[counter] = [player, int(dfNoLabel.at[FIRST_ROW, player])]
      dfLeaderboard2.loc[counter] = [player, int(dfNoLabel.at[SECOND_ROW, player])]
      dfLeaderboard3.loc[counter] = [player, int(dfNoLabel.at[THIRD_ROW, player])]
      dfLeaderboard4.loc[counter] = [player, int(dfNoLabel.at[FOURTH_ROW, player])]
      counter = counter + 1
      

    #sorts and prints the leaderboards
    dfLeaderboard1 = dfLeaderboard1.sort_values(['First Places', 'Player'],  ascending=[0, 1])
    dfLeaderboard2 = dfLeaderboard2.sort_values(['Top 2 Finishes', 'Player'],  ascending=[0, 1])
    dfLeaderboard3 = dfLeaderboard3.sort_values(['Top 3 Finishes', 'Player'],  ascending=[0, 1])
    dfLeaderboard4 = dfLeaderboard4.sort_values(['Top 4 Finishes', 'Player'],  ascending=[0, 1])

    if display == True:
      print(dfLeaderboard1)
      print(dfLeaderboard2)
      print(dfLeaderboard3)
      print(dfLeaderboard4)
    return dfLeaderboard1,dfLeaderboard2,dfLeaderboard3,dfLeaderboard4