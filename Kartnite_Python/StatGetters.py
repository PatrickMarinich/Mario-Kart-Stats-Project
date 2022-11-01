import pandas as pd

#This file will contain all of the methods that get different stats
#this will include all track stat getters, player stat getters, and seasonal and all time stat getters

#All of these stats are calculated here, and they are called within the I/O file or the Player Profile if nessassary



#This function gets all of the data for a specific track, includes things such as total race count,
#and a track ownership leaderboard
def GetTrackData(dfScores,dfRaceCount,Track,TrackIndex):
 
  AVERAGE_PERCENT = .96
  TOTAL_PERCENT = .04

  #eliminates the first row, to allow for players only
  dfNoTracks = dfScores[dfScores.columns.difference(["Tracks x Players"])]
 
  #make sure that the track exists in the data
  if Track in set(dfScores["Tracks x Players"]):
    print("Stats For: ", Track)
    #now display the data for the track plus any interesting stats
    print("\n", "Total Scores")
    print(dfScores.loc[[TrackIndex[Track]]])

    races = 0
    for player in set(dfNoTracks.columns.values.tolist()):
      races = races + int(dfRaceCount.at[TrackIndex[Track], player])
    print('\nTimes Played:',races )

    #prints player averages. 
    print('\nPlayer Averages:')
    for racer in set(dfNoTracks.columns.values.tolist()):
      print(racer,": ", getPlayerAverage(dfScores,dfRaceCount,racer,Track,TrackIndex))
    print('\n')
    print(getTrackOwner(dfScores, dfRaceCount, Track, TrackIndex), "is the MVP for this track")
    
    print('\nMVP Leaderboard')
    #determine the score for each player within the data
    dfNoTracks = dfScores[dfScores.columns.difference(["Tracks x Players"])]
    #leaderboard object
    dfLeaderboard = pd.DataFrame({'Player': [], 'MVP Points':[]})
    counter = 0
   
    #gets the ownership scores of each player for the track
    TrackTotalPoints = 0
    for player in set(dfNoTracks.columns.values.tolist()):
      TrackTotalPoints = TrackTotalPoints + int(dfScores.at[TrackIndex[Track], player])
    for player in set(dfNoTracks.columns.values.tolist()):
      ownershipScore = ((int(dfScores.at[TrackIndex[Track],player])/TrackTotalPoints)*100) *TOTAL_PERCENT + getPlayerAverage(dfScores,dfRaceCount,player,Track,TrackIndex) * AVERAGE_PERCENT


      #puts the score into the datafram
      dfLeaderboard.loc[counter] = [player, ownershipScore]
      counter = counter + 1
      playerScore = 0

    #sorts and prints the leaderboards
    dfLeaderboard = dfLeaderboard.sort_values(['MVP Points', 'Player'],  ascending=[0, 1])
    print(dfLeaderboard)

  else:
    print('Track Selection Was Invalid')



#this gets the track MVP of any specific track.
#A mix between total score and average is used to prevent a player from goign 1/1 on a track and owning it the whole season
#we all can agree that something along the lines of 9/10 is better then 2/2
def getTrackOwner(dfScores,dfRaceCount, Track, TrackIndex):

  AVERAGE_PERCENT = .96
  TOTAL_PERCENT = .04

  #eliminates the first row, to allow for players only
  dfNoTracks = dfScores[dfScores.columns.difference(["Tracks x Players"])]


  #goes through all players and then find the max score

  currentMaxScore = 0
  currentPlayer = ""
  TrackTotalPoints = 0
  for player in set(dfNoTracks.columns.values.tolist()):
    TrackTotalPoints = TrackTotalPoints + int(dfScores.at[TrackIndex[Track], player])

  if TrackTotalPoints != 0:
    for player in set(dfNoTracks.columns.values.tolist()):
      #way to calculate track owner, total points + average
      playerScore = ((int(dfScores.at[TrackIndex[Track],player])/TrackTotalPoints)*100) *TOTAL_PERCENT + getPlayerAverage(dfScores,dfRaceCount,player,Track,TrackIndex) * AVERAGE_PERCENT
  
      if playerScore > currentMaxScore:
        currentPlayer = player
        currentMaxScore = playerScore
      elif playerScore == currentMaxScore:
        currentPlayer = currentPlayer + ", " + player
      else:
        continue

  return currentPlayer


#This is for the track owner all time, it uses only average rather then
#a mix of point total and average,
#there is a race minimum
RACE_MINIMUM = 5

def getAllTimeTrackOwner(dfScores,dfRaceCount,Track,TrackIndex):
  #eliminates the first row, to allow for players only
  dfNoTracks = dfScores[dfScores.columns.difference(["Tracks x Players"])]


  #goes through all players and then find the max score

  currentMaxScore = 0
  currentPlayer = ""
  TrackTotalPoints = 0
  for player in set(dfNoTracks.columns.values.tolist()):
    TrackTotalPoints = TrackTotalPoints + int(dfScores.at[TrackIndex[Track], player])

  if TrackTotalPoints != 0:
    for player in set(dfNoTracks.columns.values.tolist()):
      #way to calculate track owner, total points + average
      playerScore =  getPlayerAverage(dfScores,dfRaceCount,player,Track,TrackIndex)
  
      if playerScore > currentMaxScore and int(dfRaceCount.at[TrackIndex[Track], player]) >= RACE_MINIMUM:
        currentPlayer = player
        currentMaxScore = playerScore
      elif playerScore == currentMaxScore and int(dfRaceCount.at[TrackIndex[Track], player]) >= RACE_MINIMUM:
        currentPlayer = currentPlayer + ", " + player
      else:
        continue

  if currentPlayer == "":
    currentPlayer = "N/A"

  return currentPlayer


#gets a list of all of the track owners of every single track that the stats are kept for

def getAllTrackOwners(dfScores,dfRaceCount,TrackIndex, display=True):
  #the list that will get all of the track mvps
  dfList = pd.DataFrame({'Track': [], 'Current MVP': []})

  counter = 0
  for track in TrackIndex:
    mvp = getTrackOwner(dfScores,dfRaceCount, track, TrackIndex)
    dfList.loc[counter] = [track,mvp]
    counter = counter + 1

  if (display == True):
    print(dfList)
  return dfList


#Gets a list of the all time track owners, this uses a play minimum and only track average
#this never resets as the seasons change.

def getAllTimeAllTrackOwners(dfScores,dfRaceCount,TrackIndex,display = True):
  #the list that will get all of the track mvps
  dfList = pd.DataFrame({'Track': [], 'Current MVP': []})

  counter = 0
  for track in TrackIndex:
    mvp = getAllTimeTrackOwner(dfScores,dfRaceCount, track, TrackIndex)
    dfList.loc[counter] = [track,mvp]
    counter = counter + 1

  if (display == True):
    print(dfList)
  return dfList


#Gets the given players average on any specific track

def getPlayerAverage(dfScores, dfRaceCount, Player, Track, TrackIndex):
  #eliminates the first row, to allow for players only
  dfNoTracks = dfScores[dfScores.columns.difference(["Tracks x Players"])]
  
  if Player in set(dfNoTracks.columns.values.tolist()):
    #checks for divide by 0

    RaceCount = int(dfRaceCount.at[TrackIndex[Track],Player])
    Score =  int(dfScores.at[TrackIndex[Track],Player])
   
    if(Score == 0 or RaceCount == 0):
      averageScore = 0
    else: 
      averageScore = Score/RaceCount
  
    

  else:
    averageScore = "ERROR"
    print("There was an internal with Averaging Have Pat re-read code")
  

  return averageScore


#-----------------------PLAYER SEEDING-------------------------------

#Point Values, constants which can be adjusted for ease of balancing
POINTS_SCORED_POINTS = 0.25        #points for each GP point scored
GP_WINS_POINTS = 125               #points per gp win
OWNER_POINTS = 0.25                #points per player on owned track
DODGE_POINTS = 3                 #points per dodge
AVERAGE_POINTS = 3                 #points for track average
BLUE_POINTS = 0.5                 #points for getting hit with blue shell
BLUE_D_POINTS = 8                  #points for dodging a blue shell



def getPlayerStats(dfScores,dfRaceCount, dfWins,dfShock, dfKartScore, dfBlue, Player, TrackIndex):
  
  print("Displaying All Seasonal Stats for", Player)
  print("\n")
  print("---------------")
  #gets all of the tracks that the player owns
  Owns = ''
  for track in TrackIndex:
    if getTrackOwner(dfScores,dfRaceCount,track,TrackIndex) == Player:
      
      if Owns == '':
        Owns = track
      else:
        Owns = Owns + "\n" + track

  if(Owns == ''):
    print("Track MVP on: None")
  else:
    print("Tracks MVP on:\n", Owns)

  print("---------------")

  #prints total wins
  totalRaces = 0
  for Track in TrackIndex:
    totalRaces = totalRaces + int(dfRaceCount.at[TrackIndex[Track],Player])
  print("Total Races Played:", totalRaces)

  #Gp Wins
  print("Grand Prix Wins:", dfWins.at[0,Player])
  #dodges
  print("Shock Dodges:", dfShock.at[0,Player])
  #blue shell hits
  print("Times hit with a Blue:", dfBlue.at[0,Player])
  #blue shell dodges
  print("Blue Dodges:", dfBlue.at[1,Player])

  ####KART SCORE####
  dfNoTracks = dfScores[dfScores.columns.difference(["Tracks x Players"])]
  KartScore = 0
  
  #gp wins points
  WinsScore = int(dfWins.at[0,Player])*GP_WINS_POINTS
    
  #owner score 
  OwnedScore = int(dfKartScore.at[0, Player]) * OWNER_POINTS
     
  #Dodges
  DodgeScore = int(dfShock.at[0,Player])*DODGE_POINTS
    
  #total points
  PointsScore = 0
  for track in TrackIndex:
   PointsScore = PointsScore + (int(dfScores.at[TrackIndex[track], Player])*POINTS_SCORED_POINTS)

  #adds in track averages
  avgScore = 0
  for track in TrackIndex:
    avgScore = avgScore + (int(getPlayerAverage(dfScores,dfRaceCount,Player,track,TrackIndex))*AVERAGE_POINTS)
  
  #points for blue shells
  blueScore = (int(dfBlue.at[0,Player]) * BLUE_POINTS) + (int(dfBlue.at[1,Player]) * BLUE_D_POINTS)



  KartScore = WinsScore + OwnedScore + DodgeScore + avgScore  + PointsScore + blueScore
  print('---------------')
  print("Kart Score:", KartScore)
  print('---------------')
  print("Kart Score Breakdown:")
  print('GP Win Points:', WinsScore)
  print('Points From Being Track MVP:', OwnedScore)
  print('Race Points:', PointsScore)
  print('Track Avg Points:', avgScore)
  print('Shock Dodge Points:', DodgeScore)
  print('Blue Shell Points:', blueScore)

  #prints the total Scores
  dfPlayerScores = dfScores[["Tracks x Players", Player]]
  print(Player, "\'s Total Scores")
  print("\n")
  print(dfPlayerScores)

  #prints Averages
  print("\n")
  print(Player, "\'s Track Averages")
  print("\n")
  for track in TrackIndex:
    print(track, "- ", getPlayerAverage(dfScores,dfRaceCount,Player,track,TrackIndex))

def getSeedings(sh,TrackIndex,display=True):
    
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

    #determine the score for each player within the data
    dfNoTracks = dfScores[dfScores.columns.difference(["Tracks x Players"])]
    #leaderboard object
    dfLeaderboard = pd.DataFrame({'Player': [], 'Kart Score':[]})
    counter = 0
   
    #sets up the scores for each player
    for player in set(dfNoTracks.columns.values.tolist()):
      playerScore = 0
      #gp wins 
      playerScore = int(dfWins.at[0,player])*GP_WINS_POINTS
    
      #enters the owned track score 
      playerScore = playerScore + int(dfKartScore.at[0, player])*OWNER_POINTS


      #Dodges
      playerScore = int(dfShock.at[0,player])*DODGE_POINTS + playerScore
    
      #total points
      points = 0
      for track in TrackIndex:
        points = points + int(dfScores.at[TrackIndex[track], player]) * POINTS_SCORED_POINTS
      playerScore = playerScore + points

      #adds in track averages
      avgpoints = 0
      for track in TrackIndex:
        avgpoints = avgpoints + (int(getPlayerAverage(dfScores,dfRaceCount,player,track,TrackIndex))*AVERAGE_POINTS)
      playerScore = playerScore + avgpoints

      #adds blue points
      playerScore = playerScore + (int(dfBlue.at[0,player]) * BLUE_POINTS) + (int(dfBlue.at[1,player]) * BLUE_D_POINTS)

      #puts the score into the datafram
      dfLeaderboard.loc[counter] = [player, playerScore]
      counter = counter + 1
      playerScore = 0

    #sorts and prints the leaderboards
    dfLeaderboard = dfLeaderboard.sort_values(['Kart Score', 'Player'],  ascending=[0, 1])
    
    if display == True:
      print(dfLeaderboard)

    return dfLeaderboard





#----------------ALL TIME PLAYER STATS-----------------


#This function will gather all of the stats for each player, all time.
#this is opposed to just the seasonal stats

#This function will get the data from the two different sheets and combine them into 
#a place where a given player can see all of their stats

#constants
#misc score constants
BLUE_DODGE = 8
BLUE_HIT = 0.5
SHOCK = 2


def getAllTimeStats(season,allTime,player,TrackIndex):


    print('Loading Data....')
    #seasonal stats
    kartData = season.worksheet('Total Scores').get_all_values()
    RaceCount = season.worksheet('Race Count').get_all_values()
    Wins = season.worksheet('GP Wins').get_all_values()
    Shock = season.worksheet('Shock Dodges').get_all_values()
    OwnedScore = season.worksheet('Owned Score').get_all_values()
    Blue = season.worksheet('Blue Shells').get_all_values()
    
    #alltime stats
    kartDataAllTime = allTime.worksheet('Total Scores').get_all_values()
    RaceCountAllTime = allTime.worksheet('Race Count').get_all_values()
    WinsAllTime = allTime.worksheet('GP Wins').get_all_values()
    ShockAllTime = allTime.worksheet('Shock Dodges').get_all_values()

    OwnedScoreAllTime = allTime.worksheet('Owned Score').get_all_values()

    BlueAllTime = allTime.worksheet('Blue Shells').get_all_values()
    SeedingAllTime = allTime.worksheet('All-Time Seeding').get_all_values()
  

    print('Combining Old and New Data....')

    #the dataframes from each of the sheets (seasonal)
    dfSeasonOwnedScore = pd.DataFrame(OwnedScore[1:], columns = OwnedScore[0])
    dfSeasonScores = pd.DataFrame(kartData[1:], columns=kartData[0])
    dfSeasonRaceCount = pd.DataFrame(RaceCount[1:], columns = RaceCount[0])
    dfSeasonWins = pd.DataFrame(Wins[1:], columns = Wins[0])
    dfSeasonShock = pd.DataFrame(Shock[1:], columns = Shock[0])
    dfSeasonBlue = pd.DataFrame(Blue[1:], columns = Blue[0])

    #all time
    dfAllTimeOwnedScore = pd.DataFrame(OwnedScoreAllTime[1:], columns = OwnedScoreAllTime[0])
    dfAllTimeScores = pd.DataFrame(kartDataAllTime[1:], columns=kartDataAllTime[0])
    dfAllTimeRaceCount = pd.DataFrame(RaceCountAllTime[1:], columns = RaceCountAllTime[0])
    dfAllTimeWins = pd.DataFrame(WinsAllTime[1:], columns = WinsAllTime[0])
    dfAllTimeShock = pd.DataFrame(ShockAllTime[1:], columns = ShockAllTime[0])
    dfAllTimeBlue = pd.DataFrame(BlueAllTime[1:], columns = BlueAllTime[0])
    dfAllTimeSeeding = pd.DataFrame(SeedingAllTime[1:], columns =SeedingAllTime[0])


    print('Doing Calculations...')

    if player == 'all':
      dfAllTimeWins = dfAllTimeWins[dfAllTimeWins.columns.difference(["Tracks x Players"])]
      players = dfAllTimeWins.columns
    else:
      players = []
      players.append(player)


    for player in players:
    #combine the data frames into one df for use later in displaying the stats
      for track in TrackIndex:
        dfAllTimeScores.loc[TrackIndex[track], player] = int(dfAllTimeScores.at[TrackIndex[track], player]) + int(dfSeasonScores.at[TrackIndex[track], player])
        dfAllTimeRaceCount.loc[TrackIndex[track], player] = int(dfAllTimeRaceCount.at[TrackIndex[track], player]) + int(dfSeasonRaceCount.at[TrackIndex[track], player])
      
      #others not related to tracks
      dfAllTimeOwnedScore.loc[0,player] = float(dfAllTimeOwnedScore.loc[0,player]) + float(dfSeasonOwnedScore.loc[0,player])
      dfAllTimeWins.loc[0,player] = int(dfAllTimeWins.loc[0,player]) + int(dfSeasonWins.loc[0,player])
      dfAllTimeShock.loc[0,player] = int(dfAllTimeShock.loc[0,player]) + int(dfSeasonShock.loc[0,player])
    
      #blueshell is two columns
      dfAllTimeBlue.loc[0,player] = int(dfAllTimeBlue.loc[0,player]) + int(dfSeasonBlue.loc[0,player])
      dfAllTimeBlue.loc[1,player] = int(dfAllTimeBlue.loc[1,player]) + int(dfSeasonBlue.loc[1,player])
    

      #players total points scores, and races, tracks owned
      totalPoints = 0
      totalRaces = 0
      tracksOwned = 0
      for track in TrackIndex:
        totalPoints = totalPoints + int(dfAllTimeScores.loc[TrackIndex[track],player])
        totalRaces = totalRaces + int(dfAllTimeRaceCount.loc[TrackIndex[track],player])
        if (getAllTimeTrackOwner(dfAllTimeScores,dfAllTimeRaceCount,track,TrackIndex) == player):
          tracksOwned = tracksOwned + 1

        #fixes divide by 0 error
        if totalRaces == 0:
          average = 0
          FirstPlaceRate = 0
          avgGPScore= 0
          FirstPlaceEquivilent = 0

        else:
          average = totalPoints/totalRaces
          FirstPlaceRate = (int(dfAllTimeWins.at[0,player]) / (totalRaces/8))*100
          avgGPScore = (totalPoints) / (totalRaces/8)
          FirstPlaceEquivilent = totalPoints/15

    
        

        ##Display formatting and print statements
      print('\n\nDisplaying the All-Time Stats for', player)
      print('\n---Seeding Stats---')
      print('Normalized KartScore: ', dfAllTimeSeeding.at[0,player])
      print('All Time Kart Rating: ', getKartRating(dfAllTimeScores,dfAllTimeRaceCount,dfAllTimeWins,player,TrackIndex))
      
      print('\n---Race Stats---')
      print('Total Race Points: ', totalPoints)
      print('Total Race Count: ', totalRaces)
      print('Average Placement Points: ', average)
      print('First Place Equivalents: ', FirstPlaceEquivilent)
    
      print('\n---GP Stats---')
      print('Total GP Wins:', dfAllTimeWins.at[0,player])
      print('Total GPs Played:', totalRaces/8)
      print('GP First Place Rate: ', FirstPlaceRate , '%'  )
      print('Average GP Score: ', avgGPScore)

      print('\n---Misc Stats---')
      print('#1 Player on a Track: ', tracksOwned)
      print('Shock Dodges:', dfAllTimeShock.at[0,player])
      print('Times Hit By A Blue Shell:', dfAllTimeBlue.at[0,player])
      print('Blue Dodges: ', dfAllTimeBlue.at[1,player])
      print('Races Played on Owned Track', float(dfAllTimeOwnedScore.at[0,player])/4)
    


#Generates all of the leaderboards for the all time stats, it will display certin leaderboards if requested
#by the user
def getAllTimeLeaderboads(season,allTime,TrackIndex,display = True):
    #gets all of the data sheets opened, and then combines them into the all time 
   
    if display == True:
      print('Loading Data....')
    #seasonal stats
    kartData = season.worksheet('Total Scores').get_all_values()
    RaceCount = season.worksheet('Race Count').get_all_values()
    Wins = season.worksheet('GP Wins').get_all_values()
    Shock = season.worksheet('Shock Dodges').get_all_values()
    OwnedScore = season.worksheet('Owned Score').get_all_values()
    Blue = season.worksheet('Blue Shells').get_all_values()
    #alltime stats
    kartDataAllTime = allTime.worksheet('Total Scores').get_all_values()
    RaceCountAllTime = allTime.worksheet('Race Count').get_all_values()
    WinsAllTime = allTime.worksheet('GP Wins').get_all_values()
    ShockAllTime = allTime.worksheet('Shock Dodges').get_all_values()
    OwnedScoreAllTime = allTime.worksheet('Owned Score').get_all_values()
    BlueAllTime = allTime.worksheet('Blue Shells').get_all_values()
    SeedingAllTime = allTime.worksheet('All-Time Seeding').get_all_values()
    if display == True:
      print('Combining Old and New Data....')
    #the dataframes from each of the sheets (seasonal)
    dfSeasonOwnedScore = pd.DataFrame(OwnedScore[1:], columns = OwnedScore[0])
    dfSeasonScores = pd.DataFrame(kartData[1:], columns=kartData[0])
    dfSeasonRaceCount = pd.DataFrame(RaceCount[1:], columns = RaceCount[0])
    dfSeasonWins = pd.DataFrame(Wins[1:], columns = Wins[0])
    dfSeasonShock = pd.DataFrame(Shock[1:], columns = Shock[0])
    dfSeasonBlue = pd.DataFrame(Blue[1:], columns = Blue[0])
    #all time
    dfAllTimeOwnedScore = pd.DataFrame(OwnedScoreAllTime[1:], columns = OwnedScoreAllTime[0])
    dfAllTimeScores = pd.DataFrame(kartDataAllTime[1:], columns=kartDataAllTime[0])
    dfAllTimeRaceCount = pd.DataFrame(RaceCountAllTime[1:], columns = RaceCountAllTime[0])
    dfAllTimeWins = pd.DataFrame(WinsAllTime[1:], columns = WinsAllTime[0])
    dfAllTimeShock = pd.DataFrame(ShockAllTime[1:], columns = ShockAllTime[0])
    dfAllTimeBlue = pd.DataFrame(BlueAllTime[1:], columns = BlueAllTime[0])
    dfAllTimeSeeding = pd.DataFrame(SeedingAllTime[1:], columns =SeedingAllTime[0])
    
    if display == True:
      print('Doing Calculations...')
    
    #gets a player list
    players = dfAllTimeWins[dfAllTimeWins.columns.difference(["Tracks x Players"])].columns
    #combines all of the data frames 
    for player in players:
    #combine the data frames into one df for use later in displaying the stats
      for track in TrackIndex:
        dfAllTimeScores.loc[TrackIndex[track], player] = int(dfAllTimeScores.at[TrackIndex[track], player]) + int(dfSeasonScores.at[TrackIndex[track], player])
        dfAllTimeRaceCount.loc[TrackIndex[track], player] = int(dfAllTimeRaceCount.at[TrackIndex[track], player]) + int(dfSeasonRaceCount.at[TrackIndex[track], player])
      
      #others not related to tracks
      dfAllTimeOwnedScore.loc[0,player] = float(dfAllTimeOwnedScore.loc[0,player]) + float(dfSeasonOwnedScore.loc[0,player])
      dfAllTimeWins.loc[0,player] = int(dfAllTimeWins.loc[0,player]) + int(dfSeasonWins.loc[0,player])
      dfAllTimeShock.loc[0,player] = int(dfAllTimeShock.loc[0,player]) + int(dfSeasonShock.loc[0,player])
    
      #blueshell is two columns
      dfAllTimeBlue.loc[0,player] = int(dfAllTimeBlue.loc[0,player]) + int(dfSeasonBlue.loc[0,player])
      dfAllTimeBlue.loc[1,player] = int(dfAllTimeBlue.loc[1,player]) + int(dfSeasonBlue.loc[1,player])


    #empty leaderboards for use below
    
    # -- Leaderboards for Power Points -- 
    dfPowerPointsLeaderboard = pd.DataFrame({'Player' : [], 'Seeding Power Points': []})
    dfNormalizedKartLeaderboard = pd.DataFrame({'Player': [], 'Kart Score' : []})
    dfKartRatingLeaderboard = pd.DataFrame({'Player' : [], 'Kart Rating': []})
    dfMiscRatingLeaderboard = pd.DataFrame({'Player' :  [], 'Misc Points' : []})

    #Other Leaderboards
    dfAllTimeAverageLeaderboard = pd.DataFrame({'Player': [], 'Average' : []})
    dfAllTimeWinsLeaderboard = pd.DataFrame({'Player' : [], 'GP Wins' : []})
    dfShockDodgesLeaderboard = pd.DataFrame({'Player' : [], 'Shock Dodges' : []})
    dfBlueShellsLeaderboard = pd.DataFrame({'Player' : [], 'Blue Shells Dodged': [], 'Blue Shells Hit' : []})
    dfRaceCountLeaderboard = pd.DataFrame({'Player' : [], 'Races Played': []})
    dfTotalPointsLeaderboard = pd.DataFrame({'Player' : [], 'Points Scored' : []})
    dfTracksOwnedLeaderboard = pd.DataFrame({'Player' : [], 'Tracks Owned' : []})

    #-----gets the current seasons normalized Kart scores ----------
    dfFinalRanks = getSeedings(season,TrackIndex,display = False)
    SeasonalKartNormalizedScores = 0
    #get the total points,
    for index in dfFinalRanks.index:
      SeasonalKartNormalizedScores += dfFinalRanks.at[index,'Kart Score']
        #make a new leaderboard, and then add all the players to it with their new scores:
    dfSeasonScores = pd.DataFrame({'Player': [], 'Season Score':[]})
    for index in dfFinalRanks.index:
    #make score percent of score of the total:
      score = (int(dfFinalRanks.at[index,'Kart Score']) / SeasonalKartNormalizedScores) * 100
      #multiplier for placements
      if(index == 0):
        score *= 1.25
      elif(index == 1):
        score *= 1.125
      elif(index == 2):
        score *= 1.05
      dfSeasonScores.at[index] = [dfFinalRanks.at[index,'Player'],score]

    #generates all of the leaderboards
    currRow = 0
    for player in players:

      # ---- Calculations ---
      #players total points scores, and races, tracks owned
      totalPoints = 0
      totalRaces = 0
      tracksOwned = 0
      for track in TrackIndex:
        totalPoints = totalPoints + int(dfAllTimeScores.loc[TrackIndex[track],player])
        totalRaces = totalRaces + int(dfAllTimeRaceCount.loc[TrackIndex[track],player])
        if (getAllTimeTrackOwner(dfAllTimeScores,dfAllTimeRaceCount,track,TrackIndex) == player):
          tracksOwned = tracksOwned + 1

        #fixes divide by 0 error
        if totalRaces == 0:
          average = 0
          avgGPScore= 0
          miscScore = 0
        else:
          average = totalPoints/totalRaces
          FirstPlaceRate = (int(dfAllTimeWins.at[0,player]) / (totalRaces/8))*100
          avgGPScore = (totalPoints) / (totalRaces/8)
          FirstPlaceEquivilent = totalPoints/15
          miscScore = (int(dfAllTimeBlue.at[1,player])*BLUE_DODGE + int(dfAllTimeBlue.at[0,player])*BLUE_HIT + int(dfAllTimeShock.at[0,player])*SHOCK) / (totalRaces/8)
      

      #----LEADERBOARDS ---
      

      #---For Power Points---
      estimatedKartScore = float(dfSeasonScores.loc[dfSeasonScores['Player'] == player,'Season Score']) + 0.85*float(dfAllTimeSeeding.at[0,player])
      dfNormalizedKartLeaderboard.at[currRow] = [player, estimatedKartScore]
      rating = getKartRating(dfAllTimeScores,dfAllTimeRaceCount,dfAllTimeWins,player,TrackIndex)
      dfKartRatingLeaderboard.at[currRow] = [player, rating]
      dfMiscRatingLeaderboard.at[currRow] = [player, miscScore]

      # --- Other Leaderboards --
      dfAllTimeAverageLeaderboard.at[currRow] = [player, average]
      dfAllTimeWinsLeaderboard.at[currRow] = [player, dfAllTimeWins.at[0,player]]
      dfShockDodgesLeaderboard.at[currRow] = [player, dfAllTimeShock.at[0,player]]
      dfBlueShellsLeaderboard.at[currRow] = [player, dfAllTimeBlue.at[1,player], dfAllTimeBlue.at[0,player]]
      dfRaceCountLeaderboard.at[currRow] = [player, totalRaces]
      dfTotalPointsLeaderboard.at[currRow] = [player,totalPoints]
      dfTracksOwnedLeaderboard.at[currRow] = [player,tracksOwned]

      #--loop --
      currRow = currRow + 1



    #-----SORT----
    dfNormalizedKart = dfNormalizedKartLeaderboard.sort_values(['Kart Score','Player'], ascending=[0,1])
    dfKartRating = dfKartRatingLeaderboard.sort_values(['Kart Rating', 'Player'],  ascending=[0, 1])
    dfAllTimeWins = dfAllTimeWinsLeaderboard.sort_values(['GP Wins', 'Player'], ascending=[0,1])
    dfAllTimeAverage = dfAllTimeAverageLeaderboard.sort_values(['Average', 'Player'], ascending=[0,1])
    dfAllTimeShockDodges = dfShockDodgesLeaderboard.sort_values(['Shock Dodges', 'Player'], ascending=[0,1])
    dfAllTimeBlueShells = dfBlueShellsLeaderboard.sort_values(['Blue Shells Dodged', 'Player'], ascending=[0,1])
    dfAllTimeRaceCount = dfRaceCountLeaderboard.sort_values(['Races Played', 'Player'], ascending=[0,1])
    dfAllTimeTotalPoints = dfTotalPointsLeaderboard.sort_values(['Points Scored', 'Player'], ascending=[0,1])
    dfAllTimeTracksOwned = dfTracksOwnedLeaderboard.sort_values(['Tracks Owned', 'Player'], ascending=[0,1]) 
    dfMiscScore = dfMiscRatingLeaderboard.sort_values(['Misc Points', 'Player'], ascending= [0,1])  


     #for the power points seeding leaderboard, matches player index to rank
    dfKartRankList = dfNormalizedKart['Kart Score'].rank(ascending = False)
    dfRatingRankList = dfKartRating['Kart Rating'].rank(ascending = False)
    dfMiscRankList = dfMiscScore['Misc Points'].rank(ascending = False)

    currRow = 0
    for player in players:
      #points for normalized kartscore, Rating, Misc Points.
      #index of the player
      PlayerIndex = dfNormalizedKart.index[dfNormalizedKart['Player']==player].tolist()
      #generate power points based on leaderboard positions
      kartPoints = (3 * len(dfNormalizedKart.index.values)) - (3*int(dfKartRankList[PlayerIndex]))
      ratingPoints = (4 * len(dfKartRating.index.values)) - (4*int(dfRatingRankList[PlayerIndex]))
      miscPoints = (1 * len(dfMiscScore.index.values)) - int(dfMiscRankList[PlayerIndex])
      #sum the points
      powerPoints = kartPoints + ratingPoints + miscPoints
      #add to list
      dfPowerPointsLeaderboard.at[currRow] = [player,powerPoints]
      currRow = currRow + 1

    #sort Power Points to determine final all time seeding
    dfPowerPoints = dfPowerPointsLeaderboard.sort_values(['Seeding Power Points','Player'], ascending=[0,1])

    if display == True:
      print(dfPowerPoints)
      print('\n')
      print(dfNormalizedKart)
      print('\n')
      print(dfKartRating)
      print('\n')
      print(dfMiscScore)
      print('\n')
      print(dfAllTimeWins)
      print('\n')
      print(dfAllTimeAverage)
      print('\n')
      print(dfAllTimeShockDodges)
      print('\n')
      print(dfAllTimeBlueShells)
      print('\n')
      print(dfAllTimeRaceCount)
      print('\n')
      print(dfAllTimeTotalPoints)
      print('\n')
      print(dfAllTimeTracksOwned)
      print('\n')

    #--others--- 
    return dfPowerPoints,dfNormalizedKart,dfKartRating,dfMiscScore,dfAllTimeWins,dfAllTimeAverage,dfAllTimeShockDodges,dfAllTimeBlueShells,dfAllTimeRaceCount,dfAllTimeTotalPoints



#--------------------KART RATING----------------------

#kart rating is a new metric that acts like QBR in football,
#a max kart rating will be out of 100 points
#60 points will be from GP win %
#60 points will be from average GP points
#33 points will be from all time tracks owned

POINTS_FOR_WINS = 60
POINTS_FOR_AVERAGE = 60
POINTS_FOR_TRACK = 33

#this function returns the specific kart rating of a player
def getKartRating(dfScores,dfRaces,dfWins,player,TrackIndex):

  #gets total races and total points
  raceCount = 0
  totalPoints = 0
  for track in TrackIndex:
    raceCount = raceCount + int(dfRaces.at[TrackIndex[track], player])
    totalPoints = totalPoints + int(dfScores.at[TrackIndex[track], player])

  
  if raceCount == 0:
    gpWinPercentage = 0
    avgPointsPerGP = 0
  else:
    #assumes 8 race gps which is our standard and a max of 120 points
    gpWinPercentage = (int(dfWins.at[0,player]) / (raceCount / 8))
    #get the average points per GP
    avgPointsPerGP = totalPoints / (raceCount / 8)
    avgPointsPerGP = avgPointsPerGP / 120

  #gets the % of tracks owned
  count = 0
  for track in TrackIndex:
    output = getAllTimeTrackOwner(dfScores,dfRaces,track,TrackIndex)
    if output == player:
      count = count + 1

  tracksOwnedPercentage = count / len(TrackIndex)


  KartRating = (gpWinPercentage * POINTS_FOR_WINS) + (avgPointsPerGP * POINTS_FOR_AVERAGE) + (tracksOwnedPercentage * POINTS_FOR_TRACK)


  return KartRating
