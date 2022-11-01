from StatGetters import *


# This file will contain all of the methods used for a user entering data into the database
# Every function below is called within the I/O file depending on the user input type


#Allows for individual races to be put into the system
#takes in the current database, racecount, kartscores, placements, played track, racers, their scores and the dictionary for tracks

def inputRace(currentData,RaceCount,dfKartScore, dfPlacement, Track, Racers, Scores,TrackIndex):  
  #checks to see if the track exists
  if Track in set(currentData["Tracks x Players"]):
    print('Valid', Track)
    #seperates the players into an array, make sure that all players also exist

    racersArray = Racers.split()
    # checks that all players are valid
    validCount = 0
    for racer in racersArray:
      if(racer in set(currentData.columns.values.tolist())):
          print('Valid', racer)
          validCount = validCount + 1
      else: 
          validCount = validCount - 1
          print('Invalid', racer)

  
    if validCount == len(racersArray):
      print("....Everything is valid, Updating the scores....")

      ##if all players are valid update the scores

      #gets scores into an array
      newScores = Scores.split()
      #changes to integers
      for i in range(len(newScores)):
        newScores[i] = int(newScores[i])
      #Adds new Score to the current score for each racer, uses the track index to find the track
      for i in range(len(racersArray)):
        
        #only gives the points if there is a singular MVP
        if(len(getTrackOwner(currentData,RaceCount, Track, TrackIndex).split()) == 1):
        #gives the track owner a tally for each person that played the track
          dfKartScore.at[0, getTrackOwner(currentData,RaceCount, Track, TrackIndex)] = int(dfKartScore.at[0, getTrackOwner(currentData,RaceCount, Track, TrackIndex)]) + 1


        #if the score is then 15, 12, 10, or 8, then increment the placement stats
        FIRSTPLACE_ROW = 0
        TOP2_ROW = 1
        TOP3_ROW = 2
        TOP4_ROW = 3
        #adds to the row if that place or higher was achieved, this is for percentage stats later!
        if newScores[i] == 15:
          dfPlacement.at[FIRSTPLACE_ROW,racersArray[i]] =  int(dfPlacement.at[FIRSTPLACE_ROW,racersArray[i]]) + 1
          dfPlacement.at[TOP2_ROW,racersArray[i]] =  int(dfPlacement.at[TOP2_ROW,racersArray[i]]) + 1
          dfPlacement.at[TOP3_ROW,racersArray[i]] =  int(dfPlacement.at[TOP3_ROW,racersArray[i]]) + 1
          dfPlacement.at[TOP4_ROW,racersArray[i]] =  int(dfPlacement.at[TOP4_ROW,racersArray[i]]) + 1
        elif newScores[i] == 12:
          dfPlacement.at[TOP2_ROW,racersArray[i]] =  int(dfPlacement.at[TOP2_ROW,racersArray[i]]) + 1
          dfPlacement.at[TOP3_ROW,racersArray[i]] =  int(dfPlacement.at[TOP3_ROW,racersArray[i]]) + 1
          dfPlacement.at[TOP4_ROW,racersArray[i]] =  int(dfPlacement.at[TOP4_ROW,racersArray[i]]) + 1
        elif newScores[i] == 10:
          dfPlacement.at[TOP3_ROW,racersArray[i]] =  int(dfPlacement.at[TOP3_ROW,racersArray[i]]) + 1
          dfPlacement.at[TOP4_ROW,racersArray[i]] =  int(dfPlacement.at[TOP4_ROW,racersArray[i]]) + 1
        elif newScores[i] == 8:
          dfPlacement.at[TOP4_ROW,racersArray[i]] =  int(dfPlacement.at[TOP4_ROW,racersArray[i]]) + 1
        
        #increments the score
        currentData.at[TrackIndex[Track],racersArray[i]] =  int(currentData.at[TrackIndex[Track],racersArray[i]]) + newScores[i]
        #increments the count
        RaceCount.at[TrackIndex[Track],racersArray[i]] =  int(RaceCount.at[TrackIndex[Track],racersArray[i]]) + 1
       
        
    else: 
      print('There was an error entering the racers, please try again')
  else:
    print('There was an error entering the track name, please try again:', Track, "was invalid")


#allows for the edit of a single players score on a given track.
#typically only used for fixing a mistake when entering in a race, i.e if a person inputs 1 instead of 10 for a score, this method can be called with
# a paramater of 9 to fix the changes.
# if the reverse happens the person can use a negative number to decrease the score by that much

def editAScore(dfScores, Track, Racer, Score,TrackIndex):
 #makes sure track is valid
  if Track in set(dfScores["Tracks x Players"]):
    print('Valid', Track)
    # makes sure racer is valid
    if Racer in set(dfScores.columns.values.tolist()):
      print('Valid', Racer)
      #changes a specific score
      dfScores.at[TrackIndex[Track],Racer] =  int(dfScores.at[TrackIndex[Track],Racer]) + int(Score)
      print(Racer, '\'s Score was changed by ', Score, ' on ', Track)
    else:  
      print('There was an error entering the racer, please try again')
  else:
     print('There was an error entering the track name, please try again:', Track, "was invalid")



#whenever a GP is over, this method is used to keep track of who overall won

#allows for GP winners to be counted
def enterWinner(dfWins, Player):

  if Player in set(dfWins.columns.values.tolist()):
    
    dfWins.at[0, Player] = int(dfWins.at[0,Player]) + 1
    print(Player, 'has', dfWins.at[0,Player], 'wins')


  else: 
    print(Player, "does not exist within the Database, Please try again")



#This method tracks player shock dodges

#allowes for Shock dodges
def enterDodges(dfShock, Player, Count):
  if Player in set(dfShock.columns.values.tolist()):
    
    dfShock.at[0, Player] = int(dfShock.at[0,Player]) + int(Count)
    print(Player, 'has', dfShock.at[0,Player], 'shock dodges')


  else: 
    print(Player, "does not exist within the Database, Please try again")


#this method counts both the amount of blueshells a player has been hit by, and the ones that they have dodged

def addBlueShells(dfBlue, Player, hit, dodge):
  if Player in set(dfBlue.columns.values.tolist()):
    
    dfBlue.at[0, Player] = int(dfBlue.at[0,Player]) + int(hit)
    print(Player, 'has been hit by', dfBlue.at[0,Player], 'Blue Shells')
    dfBlue.at[1, Player] = int(dfBlue.at[1,Player]) + int(dodge)
    print(Player, 'has', dfBlue.at[1,Player], 'Blue Shell Dodges')
    
  else: 
    print(Player, "does not exist within the Database, Please try again")
