from Constants import *
from LeaderboardGenerators import *
from StatGetters import * 

import time
import pdfkit
import yagmail
#import wkhtmltopdf

import sys
from IPython import display
import pdfkit
from datetime import date

#this file gets all of the leaderboards and generates a html player profile for any given player

#it will get all of the stats, generate html code, convert it to a pdf, and the email it out to the given player

#CHECK AROUND LINES 150-160 FOR THE PAGE ORDER,CODE FOR PAGE GENERATION IS BELOW THIS

#############################################

#this method generates all of the stats and wraps them in html tags and formatting

def createPlayerProfile(season,allTime,player,TrackIndex):
  #----OPENING THE DATA----
  print('Loading Data....')
  #seasonal stats
  kartData = season.worksheet('Total Scores').get_all_values()
  RaceCount = season.worksheet('Race Count').get_all_values()
  Wins = season.worksheet('GP Wins').get_all_values()
  Shock = season.worksheet('Shock Dodges').get_all_values()
  OwnedScore = season.worksheet('Owned Score').get_all_values()
  Blue = season.worksheet('Blue Shells').get_all_values()
  kvr = season.worksheet('KVR Stats').get_all_values()
  placement = season.worksheet('Placement Stats').get_all_values()

  #alltime stats
  kartDataAllTime = allTime.worksheet('Total Scores').get_all_values()
  RaceCountAllTime = allTime.worksheet('Race Count').get_all_values()
  WinsAllTime = allTime.worksheet('GP Wins').get_all_values()
  ShockAllTime = allTime.worksheet('Shock Dodges').get_all_values()

  OwnedScoreAllTime = allTime.worksheet('Owned Score').get_all_values()

  BlueAllTime = allTime.worksheet('Blue Shells').get_all_values()
  SeedingAllTime = allTime.worksheet('All-Time Seeding').get_all_values()
  placementAllTime = allTime.worksheet('Placement Stats').get_all_values()
  

  print('Analyzing Old and New Data....')

  #the dataframes from each of the sheets (seasonal)
  dfSeasonOwnedScore = pd.DataFrame(OwnedScore[1:], columns = OwnedScore[0])
  dfSeasonScores = pd.DataFrame(kartData[1:], columns=kartData[0])
  dfSeasonRaceCount = pd.DataFrame(RaceCount[1:], columns = RaceCount[0])
  dfSeasonWins = pd.DataFrame(Wins[1:], columns = Wins[0])
  dfSeasonShock = pd.DataFrame(Shock[1:], columns = Shock[0])
  dfSeasonBlue = pd.DataFrame(Blue[1:], columns = Blue[0])
  dfKVR = pd.DataFrame(kvr[1:],columns = kvr[0])
  dfSeasonPlacement = pd.DataFrame(placement[1:],columns = placement[0])

  #all time
  dfAllTimeOwnedScore = pd.DataFrame(OwnedScoreAllTime[1:], columns = OwnedScoreAllTime[0])
  dfAllTimeScores = pd.DataFrame(kartDataAllTime[1:], columns=kartDataAllTime[0])
  dfAllTimeRaceCount = pd.DataFrame(RaceCountAllTime[1:], columns = RaceCountAllTime[0])
  dfAllTimeWins = pd.DataFrame(WinsAllTime[1:], columns = WinsAllTime[0])
  dfAllTimeShock = pd.DataFrame(ShockAllTime[1:], columns = ShockAllTime[0])
  dfAllTimeBlue = pd.DataFrame(BlueAllTime[1:], columns = BlueAllTime[0])
  dfAllTimeSeeding = pd.DataFrame(SeedingAllTime[1:], columns =SeedingAllTime[0])
  dfAllTimePlacement = pd.DataFrame(placementAllTime[1:],columns = placementAllTime[0])

  print('Doing Calculations...')
 
  dfAllTimeWins = dfAllTimeWins[dfAllTimeWins.columns.difference(["Tracks x Players"])]
  players = dfAllTimeWins.columns
 
  for racer in players:
  #combine the data frames into one df for use later in displaying the stats
    for track in TrackIndex:
      dfAllTimeScores.loc[TrackIndex[track], racer] = int(dfAllTimeScores.at[TrackIndex[track], racer]) + int(dfSeasonScores.at[TrackIndex[track], racer])
      dfAllTimeRaceCount.loc[TrackIndex[track], racer] = int(dfAllTimeRaceCount.at[TrackIndex[track], racer]) + int(dfSeasonRaceCount.at[TrackIndex[track], racer])
      
    #others not related to tracks
    dfAllTimeOwnedScore.loc[0,racer] = float(dfAllTimeOwnedScore.loc[0,racer]) + float(dfSeasonOwnedScore.loc[0,racer])
    dfAllTimeWins.loc[0,racer] = int(dfAllTimeWins.loc[0,racer]) + int(dfSeasonWins.loc[0,racer])
    dfAllTimeShock.loc[0,racer] = int(dfAllTimeShock.loc[0,racer]) + int(dfSeasonShock.loc[0,racer])
    
    #blueshell is two columns
    dfAllTimeBlue.loc[0,racer] = int(dfAllTimeBlue.loc[0,racer]) + int(dfSeasonBlue.loc[0,racer])
    dfAllTimeBlue.loc[1,racer] = int(dfAllTimeBlue.loc[1,racer]) + int(dfSeasonBlue.loc[1,racer])

    #placement is 4 rows
    dfAllTimePlacement.loc[0,racer] = int(dfAllTimePlacement.loc[0,racer]) + int(dfSeasonPlacement.loc[0,racer])
    dfAllTimePlacement.loc[1,racer] = int(dfAllTimePlacement.loc[1,racer]) + int(dfSeasonPlacement.loc[1,racer])
    dfAllTimePlacement.loc[2,racer] = int(dfAllTimePlacement.loc[2,racer]) + int(dfSeasonPlacement.loc[2,racer])
    dfAllTimePlacement.loc[3,racer] = int(dfAllTimePlacement.loc[3,racer]) + int(dfSeasonPlacement.loc[3,racer])







  #all data is now combined, so do any calculations for stats :)
  
  #Players Seasonal stats
    seasonalTotalPoints = 0
    seasonalTotalRaces = 0
    seasonalTracksOwned = 0
    for track in TrackIndex:
      seasonalTotalPoints = seasonalTotalPoints + int(dfSeasonScores.loc[TrackIndex[track],player])
      seasonalTotalRaces = seasonalTotalRaces + int(dfSeasonRaceCount.loc[TrackIndex[track],player])
      if (getTrackOwner(dfSeasonScores,dfSeasonRaceCount,track,TrackIndex) == player):
        seasonalTracksOwned = seasonalTracksOwned + 1

      #fixes divide by 0 error
      if seasonalTotalRaces == 0:
        seasonalAverage = 0
        seasonalFirstPlaceRate = 0
        seasonalAvgGPScore= 0
      else:
        seasonalAverage = seasonalTotalPoints/seasonalTotalRaces
        seasonalFirstPlaceRate = (int(dfSeasonWins.at[0,player]) / (seasonalTotalRaces/8))*100
        seasonalAvgGPScore = (seasonalTotalPoints) / (seasonalTotalRaces/8)

    #-----Players AllTime stats-----------
    allTimeTotalPoints = 0
    allTimeTotalRaces = 0
    allTimeTracksOwned = 0
    for track in TrackIndex:
      allTimeTotalPoints =  allTimeTotalPoints + int(dfAllTimeScores.loc[TrackIndex[track],player])
      allTimeTotalRaces =  allTimeTotalRaces + int(dfAllTimeRaceCount.loc[TrackIndex[track],player])
      if (getAllTimeTrackOwner(dfAllTimeScores,dfAllTimeRaceCount,track,TrackIndex) == player):
         allTimeTracksOwned =  allTimeTracksOwned + 1

      #fixes divide by 0 error
      if  allTimeTotalRaces == 0:
        allTimeAverage = 0
        allTimeFirstPlaceRate = 0
        allTimeAvgGPScore= 0
      else:
        allTimeAverage =  allTimeTotalPoints/ allTimeTotalRaces
        allTimeFirstPlaceRate = (int(dfAllTimeWins.at[0,player]) / (allTimeTotalRaces/8))*100
        allTimeAvgGPScore = (allTimeTotalPoints) / ( allTimeTotalRaces/8)
  

  time.sleep(60) #API calls aint free

  #placement stats
  seasonaltop1 = int(dfSeasonPlacement.at[0,player])
  seasonaltop2 = int(dfSeasonPlacement.at[1,player])
  seasonaltop3= int(dfSeasonPlacement.at[2,player])
  seasonaltop4 = int(dfSeasonPlacement.at[3,player])
  allTimetop1 = int(dfAllTimePlacement.at[0,player])
  allTimetop2 = int(dfAllTimePlacement.at[1,player]) 
  allTimetop3 = int(dfAllTimePlacement.at[2,player])
  allTimetop4 = int(dfAllTimePlacement.at[3,player])


  #gets all of the all time leaderboards (10), this is needed all the way up here so that the players seed can be found
  dfPowerPoints1,dfNormalizedKart1,dfKartRating1,dfMiscScore1,dfAllTimeWins1,dfAllTimeAverage1,dfAllTimeShockDodges1,dfAllTimeBlueShells1,dfAllTimeRaceCount1,dfAllTimeTotalPoints1 = getAllTimeLeaderboads(season,allTime,TrackIndex,display = False)

  #generation of the seasonal and all time placement leaderboards for count 
  dfSeasonFirst,dfSeasonSecond,dfSeasonThird,dfSeasonFourth = getPlacementLeaderboards(dfSeasonPlacement,display = False)
  dfAllTimeFirst,dfAllTimeSecond,dfAllTimeThird,dfAllTimeFourth = getPlacementLeaderboards(dfAllTimePlacement,display = False)

  ##do percentages here


  #all of the stats are generated, so create the files
  #---------GENERATING THE HTML FILE---------

  #for output redirection later
  print('Generating HTML File...')
  default_stdout = sys.stdout

  #HTML File name and redirecting output
  filename = player + '.html'
  sys.stdout = open(filename, 'w')


  #---initalize HTML file with stlyles and headers
  htmlHeaders()
  
  #----HTML Page Order for the PDF (these can be changed if the order wants to be changed)---
  
  ##Creates the first page of the PDF, has the player name, and thier seasonal and all time stats. #find what is needed and pass them in
  coverPage(player,seasonalTotalPoints,seasonalAverage,seasonalTotalRaces,seasonaltop1,allTimeAverage,
  dfSeasonWins,seasonalFirstPlaceRate,allTimeFirstPlaceRate,seasonalAvgGPScore,allTimeAvgGPScore,seasonalTracksOwned,allTimeTracksOwned,dfSeasonShock,
  dfSeasonBlue,dfSeasonOwnedScore, allTimeTotalPoints,allTimeTotalRaces,allTimetop1,dfAllTimeWins,dfAllTimeShock,dfAllTimeBlue,dfAllTimeOwnedScore,dfPowerPoints1,
  seasonaltop2,seasonaltop3,seasonaltop4,allTimetop2,allTimetop3,allTimetop4) 
  

  #KVR History Page
  KVRHistoryPage(player,dfKVR)

  #shows all of the current and all time track mvps
  trackMVPPage(dfSeasonScores,dfSeasonRaceCount,TrackIndex,dfAllTimeScores,dfAllTimeRaceCount) 

  time.sleep(30) #API Calls are NOT FREE

  #pages with seasonal leaderbaords
  seasonalLeaderboardPage(season,TrackIndex,dfSeasonScores,dfSeasonRaceCount,dfSeasonWins,dfSeasonShock,dfSeasonBlue,dfSeasonFirst,dfSeasonSecond,dfSeasonThird,dfSeasonFourth) 

  #pages with all time boards
  allTimeLeaderboardsPages(dfPowerPoints1,dfNormalizedKart1,dfKartRating1,dfMiscScore1,dfAllTimeWins1,dfAllTimeAverage1,dfAllTimeShockDodges1,
    dfAllTimeBlueShells1,dfAllTimeRaceCount1,dfAllTimeTotalPoints1,dfAllTimeFirst,dfAllTimeSecond,dfAllTimeThird,dfAllTimeFourth)  

    
  awardsPage(player) #a page with the player awards

 #----------Setting Output back to console--------
  sys.stdout = default_stdout
  print('Generation Complete')
  return filename


#CODE FOR MAKING PAGES GOES BELOW

def htmlHeaders():
  #file headers
  print('<!DOCTYPE html>')
  print('<html>')
  print('<body>')
  #divs for text

  print('<style> div.center {text-align: center; } </style>')
  print('<style> div.bar { display: flex; align-items: center; width: 100%; height: 3px; background-color: #1faadb; padding: 4px;} </style>')
  print('<style> div.left {text-align: left; } </style>')
  print('<style> div.statbox {text-align: left; display: inline-block; align-items:left; width: 30%; height: 320px; border: 3px solid black; padding: 7px; margin: auto; vertical-align: top;} </style>')
  print('<style> div.leaderboard {text-align:center; display: inline-block; align-items:center; width: 45%; height: 950px; border: 1px solid black; padding: 4px; margin: auto; vertical-align: top; margin:auto;} </style>')
  print('<style> div.empty {display: flex; width: 100%; height: 15px;} </style>')
  print('<style> div.statbox2 {text-align: left; display: inline-block; align-items:left; width: 30%; height: 325px; border: 3px solid black; padding: 7px; margin: auto; vertical-align: top;text-overflow: ellipsis;white-space: nowrap;overflow: hidden; } </style>')
  print('<style> .arrow {border: solid black;border-width: 0 3px 3px 0;display: inline-block;padding: 3px;} .up {transform: rotate(-135deg); -webkit-transform: rotate(-135deg); border: solid green;border-width: 0 3px 3px 0;}.down {transform: rotate(45deg);-webkit-transform: rotate(45deg); border: solid red; border-width: 0 3px 3px 0;} </style>')

def coverPage(player,seasonalTotalPoints,seasonalAverage,seasonalTotalRaces,seasonaltop1,allTimeAverage,
  dfSeasonWins,seasonalFirstPlaceRate,allTimeFirstPlaceRate,seasonalAvgGPScore,allTimeAvgGPScore,seasonalTracksOwned,allTimeTracksOwned,dfSeasonShock,
  dfSeasonBlue,dfSeasonOwnedScore, allTimeTotalPoints,allTimeTotalRaces,allTimetop1,dfAllTimeWins,dfAllTimeShock,dfAllTimeBlue,dfAllTimeOwnedScore,dfPowerPoints1,
  seasonaltop2,seasonaltop3,seasonaltop4,allTimetop2,allTimetop3,allTimetop4):
 
  #header
  print("<div class=\"center\">")
  print('<h1> Kartnite Profile:', player, '</h1>')
  print('<h3> Player Stats as of: ', date.today(), '</h3>')
  print('<p> PDF generated by Pat Marinich </p>')
  print('</div>')

  #break line
  print('<div class = \"bar\"> </div>')


  #gets the seed of the player
  playerIndex = dfPowerPoints1.index[dfPowerPoints1['Player']==player].tolist()
  seedingList = dfPowerPoints1['Seeding Power Points'].rank(ascending = False)
  playerSeed = seedingList[playerIndex]
  
  print("<div class=\"center\">")
  print('<h3> You are the all-time', int(playerSeed),'seed! </h3>')
  print('</div>')
  #vertical bar
  print("<div class=\"bar\">")
  print('</div>')

  #seasonal stats
  print("<div class=\"center\">")
  print('<h1> Seasonal Stats </h1>')
  print('</div>')

  #centers the boxes

  print('<div class = \"center\">')
  #stat box left for race stats
  print("<div class=\"statbox\">")
  #title for race stats
  print("<div class=\"center\">")
  print('<h2> Race Stats </h2>')
  print('</div>')
  #STATS HERE
  greenCount = 0
  print('<p>Total Race Points: ', seasonalTotalPoints,'</p>',) 
  print('<p>Total Race Count: ', seasonalTotalRaces,'</p>')
  #if statement for triangles
  if( seasonalAverage >= allTimeAverage):
    print('<p>Average Placement Points: ', seasonalAverage, '<i class="arrow up"></i>','</p>')
    greenCount = greenCount + 1
  else:
     print('<p>Average Placement Points: ', seasonalAverage, '<i class="arrow down"></i>','</p>')

  print('<p>First Places: ', seasonaltop1,'</p>')
  print('<p>Top 2 Finishes: ', seasonaltop2,'</p>')
  print('<p>Top 3 Finishes: ', seasonaltop3,'</p>')
  print('<p>Top 4 Finishes: ', seasonaltop4,'</p>')
  print('</div>')

  #stat box center for GP
  print("<div class=\"statbox\">")
  #title for GP stats
  print("<div class=\"center\">")
  print('<h2> GP Stats </h2>')
  print('</div>')
  #STATS HERE
  print('<p> Total GP Wins:', dfSeasonWins.at[0,player],'</p>')
  print('<p> Total GPs Played:', seasonalTotalRaces/8,'</p>')
  
  #if statements for triangles
  if(seasonalFirstPlaceRate >= allTimeFirstPlaceRate):
    print('<p> GP First Place Rate: ', seasonalFirstPlaceRate , '% <i class="arrow up"></i> </p>'  )
    greenCount = greenCount + 1
  else:
     print('<p> GP First Place Rate: ', seasonalFirstPlaceRate , '% <i class="arrow down"></i> </p>'  )
  if(seasonalAvgGPScore >= allTimeAvgGPScore):
    print('<p> Average GP Score: ', seasonalAvgGPScore,'<i class="arrow up"></i>','</p>')
    greenCount = greenCount + 1
  else:
    print('<p> Average GP Score: ', seasonalAvgGPScore,'<i class="arrow down"></i>','</p>')
  
  print('</div>')

  #stat box right for MISC stats
  print("<div class=\"statbox\">")
  #title for MISC
  print("<div class=\"center\">")
  print('<h2> Misc Stats </h2>')
  print('</div>')
  #stats here
  #if statement for triangle
  if(seasonalTracksOwned >= allTimeTracksOwned):
    print('<p>#1 Player on a Track: ', seasonalTracksOwned,'<i class="arrow up"></i>''</p>')
    greenCount = greenCount + 1
  else:
    print('<p>#1 Player on a Track: ', seasonalTracksOwned,'<i class="arrow down"></i>''</p>')
  print('<p>Shock Dodges:', dfSeasonShock.at[0,player])
  print('<p>Times Hit By A Blue Shell:', dfSeasonBlue.at[0,player],'</p>')
  print('<p>Blue Dodges: ', dfSeasonBlue.at[1,player],'</p>')
  print('<p>Races Played on Owned Track:', float(dfSeasonOwnedScore.at[0,player])/4,'</p>')
  print('</div>')

  #end center
  print('</div>')

  #empty space bar
  print("<div class=\"empty\">")
  print('</div>')

  #message based on current preformance
  ##center these messages
  print("<div class=\"center\">")
  if(greenCount == 4):
    print('<p>You are on fire this season! Keep it up!</p>')
  elif(greenCount == 3):
    print('<p> This season is looking good for you so far!</p>')
  elif(greenCount == 2):
    print('<p>You are playing to your standard, good job!</p>')
  elif(greenCount == 1):
    print('<p>It looks like you are on a cold streak, you\'ll get them next time!</p>')
  else:
    print('<p>Yikes, looks like you have to be good to be lucky </p>')
  print('</div>')
  
  #vertical bar
  print("<div class=\"bar\">")
  print('</div>')

  #----All time stats----
  #seasonal stats
  print("<div class=\"center\">")
  print('<h1> All-Time Stats </h1>')
  print('</div>')

  #centers the boxes
  print('<div class = \"center\">')
  #stat box left for race stats
  print("<div class=\"statbox\">")
  #title for race stats
  print("<div class=\"center\">")
  print('<h2> All-Time Race Stats </h2>')
  print('</div>')
  #STATS HERE
  print('<p>Total Race Points: ',  allTimeTotalPoints, '</p>')
  print('<p>Total Race Count: ',  allTimeTotalRaces,'</p>')
  print('<p>Average Placement Points: ',  allTimeAverage,'</p>')
  print('<p>First Places: ',  allTimetop1,'</p>')
  print('<p>Top 2 Finishes: ',  allTimetop2,'</p>')
  print('<p>Top 3 Finishes: ',  allTimetop3,'</p>')
  print('<p>Top 4 Finishes: ',  allTimetop4,'</p>')

  print('</div>')

  #stat box center for GP
  print("<div class=\"statbox\">")
  #title for GP stats
  print("<div class=\"center\">")
  print('<h2> All-Time GP Stats </h2>')
  print('</div>')
  #STATS HERE
  print('<p> Total GP Wins:', dfAllTimeWins.at[0,player],'</p>')
  print('<p> Total GPs Played:', allTimeTotalRaces/8,'</p>')
  print('<p> GP First Place Rate: ',  allTimeFirstPlaceRate , '% </p>'  )
  print('<p> Average GP Score: ',  allTimeAvgGPScore,'</p>')
  print('</div>')

  #stat box right for MISC stats
  print("<div class=\"statbox\">")
  #title for MISC
  print("<div class=\"center\">")
  print('<h2> All-Time Misc Stats </h2>')
  print('</div>')
  #stats here
  print('<p>#1 Player on a Track: ',  allTimeTracksOwned,'</p>')
  print('<p>Shock Dodges:', dfAllTimeShock.at[0,player])
  print('<p>Times Hit By A Blue Shell:', dfAllTimeBlue.at[0,player],'</p>')
  print('<p>Blue Dodges: ', dfAllTimeBlue.at[1,player],'</p>')
  print('<p>Races Played on Owned Track:', float(dfAllTimeOwnedScore.at[0,player])/4,'</p>')
  print('</div>')

  #end center
  print('</div>')


  print('<br>')
  print('<div class=\"bar\"> </div>')

 

def trackMVPPage(dfSeasonScores,dfSeasonRaceCount,TrackIndex,dfAllTimeScores,dfAllTimeRaceCount):
  #page split
  print('<p style= \"page-break-after: always;\"> &nbsp; </p>')
  print('<p style= \"page-break-before: always;\"> &nbsp; </p>')

  print('<div class =\"center\">')
  #header
  print('<h1> Track MVPs </h1>')

  #seasonal

  print("<div class=\"leaderboard\">")
  print('<div class =\"center\">')
  print('<h2> Seasonal MVPs </h2>')
  #gets all the seasonal mvps, the the to_html prints the html nessassary
  dfSeasonOwners = getAllTrackOwners(dfSeasonScores,dfSeasonRaceCount,TrackIndex, display= False)
  print(dfSeasonOwners.to_html())
  print('</div>')
  print('</div>')

  #all time MVPs
  print("<div class=\"leaderboard\">")
  print('<div class =\"center\">')
  print('<h2> All-Time MVPs </h2>')
  #same as above conversion to html from pandas
  dfAllTimeOwners = getAllTimeAllTrackOwners(dfAllTimeScores,dfAllTimeRaceCount,TrackIndex, display= False)
  print(dfAllTimeOwners.to_html())
  print('</div>')
  print('</div>')


  #end center
  print('</div>')

  #ending bar
  print('<br>')
  print('<div class=\"bar\"> </div>')

def seasonalLeaderboardPage(season,TrackIndex,dfSeasonScores,dfSeasonRaceCount,dfSeasonWins,dfSeasonShock,dfSeasonBlue,dfSeasonFirst,dfSeasonSecond,dfSeasonThird,dfSeasonFourth):

  #page split
  print('<p style= \"page-break-after: always;\"> &nbsp; </p>')
  print('<p style= \"page-break-before: always;\"> &nbsp; </p>')

  
  #header
  print('<div class =\"center\">')
  print('<h1> Seasonal Leaderboards </h1>')
  print('</div>')

  #stat boxes for seasonal leaderboards

  #generate the leaderboards
  kartSeasonalLeaderboard= getSeedings(season,TrackIndex,display = False)
  PPRLeaderboard = getPointsPerRace(dfSeasonScores,dfSeasonRaceCount,TrackIndex,display = False)
  raceCountLeaderboard = getRaceCountLeaderbaords(dfSeasonRaceCount, TrackIndex,display = False)
  GPWinsLeaderboard = getGPWinsLeaderboard(dfSeasonWins,display = False)
  shockLeaderboard = getShockDodges(dfSeasonShock,display = False)
  blueLeaderboard = getBlueLeaderboard(dfSeasonBlue,display = False)

  #box 1 kart score
  print('<div class = "\center\">')
  print("<div class=\"statbox2\">")
  print('<h2> Kart Score </h2>')
  print(kartSeasonalLeaderboard.to_html())
  print('</div>')
  #box 2 player average
  print("<div class=\"statbox2\">")
  print('<h2> Player Average</h2>')
  print(PPRLeaderboard.to_html())
  print('</div>')
  #box 3 Race Count
  print("<div class=\"statbox2\">")
  print('<h2> Race Count </h2>')
  print(raceCountLeaderboard.to_html())
  print('</div>')

  #break line
  print('<br>')
  print('<br>')
  print('<div class = \"bar\"> </div>')
  print('<br>')

  #box 4 GP Wins
  print("<div class=\"statbox2\">")
  print('<h2> GP Wins</h2>')
  print(GPWinsLeaderboard.to_html())
  print('</div>') 
  #box 5
  print("<div class=\"statbox2\">")
  print('<h2> Shock Dodges </h2>')
  print(shockLeaderboard.to_html())
  print('</div>')
  #box 6
  print("<div class=\"statbox2\">")
  print('<h2> Blue Shells </h2>')
  print(blueLeaderboard.to_html())
  print('</div>')
  print('</div>')

  #bar
  print('<br>')
  print('<div class=\"bar\"> </div>')
  print('<br>')
  
  #first places
  print("<div class=\"statbox2\">")
  print('<h2> First Place Finishes </h2>')
  print(dfSeasonFirst.to_html())
  print('</div>') 
  #second places
  print("<div class=\"statbox2\">")
  print('<h2> Top 2 Finishes </h2>')
  print(dfSeasonSecond.to_html())
  print('</div>')
  #third places
  print("<div class=\"statbox2\">")
  print('<h2> Top 3 Finishes </h2>')
  print(dfSeasonThird.to_html())
  print('</div>')
  print('</div>')

  #bar
  print('<br>')
  print('<div class=\"bar\"> </div>')
  print('<br>')

  #Fourth places
  print("<div class=\"statbox2\">")
  print('<h2> Top 4 Finishes </h2>')
  print(dfSeasonFourth.to_html())
  print('</div>')
  print('</div>')


  ##percentages go here

  #end of pahe bar
  print('<br>')
  print('<div class=\"bar\"> </div>')
  print('<br>')

def allTimeLeaderboardsPages(dfPowerPoints1,dfNormalizedKart1,dfKartRating1,dfMiscScore1,dfAllTimeWins1,dfAllTimeAverage1,dfAllTimeShockDodges1,
    dfAllTimeBlueShells1,dfAllTimeRaceCount1,dfAllTimeTotalPoints1,dfAllTimeFirst,dfAllTimeSecond,dfAllTimeThird,dfAllTimeFourth):

  #Page 4, All-Time Leaderboards
 
  #page split
  print('<p style= \"page-break-after: always;\"> &nbsp; </p>')
  print('<p style= \"page-break-before: always;\"> &nbsp; </p>')

  #header
  print('<div class =\"center\">')
  print('<h1> All-Time Leaderboards </h1>')
  print('</div>')

  
  print('<div class = "\center\">')
  #statbox 1 power points
  print("<div class=\"statbox2\">")
  print('<h2> Seed Power Points</h2>')
  print(dfPowerPoints1.to_html())
  print('</div>')
  #statbox 2 kart Score
  print("<div class=\"statbox2\">")
  print('<h2> Kart Score </h2>')
  print(dfNormalizedKart1.to_html())
  print('</div>')
  #statbox 3 kart rating
  print("<div class=\"statbox2\">")
  print('<h2> Kart Rating</h2>')
  print(dfKartRating1.to_html())
  print('</div>')

  #break line
  print('<br>')
  print('<br>')
  print('<div class = \"bar\"> </div>')
  print('<br>')

  #statbox 4 misc scores
  print("<div class=\"statbox2\">")
  print('<h2> Misc Points</h2>')
  print(dfMiscScore1.to_html())
  print('</div>')
  #statbox 5 all time wins
  print("<div class=\"statbox2\">")
  print('<h2> GP Wins</h2>')
  print(dfAllTimeWins1.to_html())
  print('</div>')
  #statbox 6 average
  print("<div class=\"statbox2\">")
  print('<h2> Average Points</h2>')
  print(dfAllTimeAverage1.to_html())
  print('</div>')

  #break line
  print('<br>')
  print('<br>')
  print('<div class = \"bar\"> </div>')
  print('<br>')

  #statbox 7 shock dodges
  print("<div class=\"statbox2\">")
  print('<h2> Shock Dodges</h2>')
  print(dfAllTimeShockDodges1.to_html())
  print('</div>')
  #statbox 8  blue shells
  print("<div class=\"statbox2\">")
  print('<h2> Blue Shells</h2>')
  print(dfAllTimeBlueShells1.to_html())
  print('</div>')
  #statbox 9 race count
  print("<div class=\"statbox2\">")
  print('<h2> Race Count</h2>')
  print(dfAllTimeRaceCount1.to_html())
  print('</div>')

  #break line
  print('<br>')
  print('<br>')
  print('<div class = \"bar\"> </div>')
  print('<br>')

  #disclamer on the stat being tracked
  print('<div class =\"center\">')
  print("<h7> Placement Stats Started Season 3 </h7>")
  print('<br>')
  print('</div>')

  #statbox first places
  print("<div class=\"statbox2\">")
  print('<h2> First Place Finishes</h2>')
  print(dfAllTimeFirst.to_html())
  print('</div>')
  #statbox second places
  print("<div class=\"statbox2\">")
  print('<h2> Top 2 Finsihes</h2>')
  print(dfAllTimeSecond.to_html())
  print('</div>')
  #statbox 3rd places
  print("<div class=\"statbox2\">")
  print('<h2> Top 3 Finishes </h2>')
  print(dfAllTimeThird.to_html())
  print('</div>')


  #break line
  print('<br>')
  print('<br>')
  print('<div class = \"bar\"> </div>')
  print('<br>')

  #statbox 4th places
  print("<div class=\"statbox2\">")
  print('<h2> Top 4 Finishes </h2>')
  print(dfAllTimeFourth.to_html())
  print('</div>')


  #statbox points scored
  print("<div class=\"statbox2\">")
  print('<h2> Total Points</h2>')
  print(dfAllTimeTotalPoints1.to_html())
  print('</div>')
  print('</div>')


  #break line for page
  print('<br>')
  print('<br>')
  print('<div class = \"bar\"> </div>')
  print('<br>')

def awardsPage(player):

  #page split Awards time
  print('<p style= \"page-break-after: always;\"> &nbsp; </p>')
  print('<p style= \"page-break-before: always;\"> &nbsp; </p>')


  
  #header
  print('<div class =\"center\">')
  print('<h1> Award Trophy Case </h1>')
  print('</div>')
  #bar
  print('<br>')
  print('<div class = \"bar\"> </div>')
  print('<br>')

  #all of the players awards
  print('<ul>')
  for season in AWARD_LIST[player]:
    for award in season:
      print('<li>', award, '</li>')
  print('</ul>')

  #bar
  print('<br>')
  print('<div class = \"bar\"> </div>')
  print('<br>')


def KVRHistoryPage(player,dfKVR):
  #page split
  print('<p style= \"page-break-after: always;\"> &nbsp; </p>')
  print('<p style= \"page-break-before: always;\"> &nbsp; </p>')

  #page header
  #header
  print('<div class =\"center\">')
  print('<h1> Kart Versus Rating History (KVR) </h1>')
  print('</div>')

  #break line
  print('<br>')
  print('<br>')
  print('<div class = \"bar\"> </div>')

  #center the graph
  print('<div class =\"center\">')
  #get the embedded HTML for the plot
  make_line_plot(dfKVR,player)
  
  #Windows needs to use exact path :( , maybe realitive pathing will work in the future with wkhtmltopdf windows
  path = 'C:\\Users\\patri\\Github_Directories\\Kartnite\\Mario-Kart-Stats-Project\\Kartnite_Python\\KVRHistory.png'
  #path = '.\\Kartnite_Python\\KVRHistory.png'
  
  print('<img src=', path, 'alt=\"KVR History\" width=\"1000\" height=\"800\">' )

  print('</div>')



###IMPUT NEW PAGES HERE








#this function converts the html file into a pdf so it can be viewed nicely
def convertHTMLtoPDF(filename):
  print('Converting to PDF...')
  path = 'Kartnite_Python\wkhtmltopdf.exe' #sys.path[0]
  config = pdfkit.configuration(wkhtmltopdf=path)

  # Returns the date for file name
  today = date.today()
  today = date.isoformat(today)

  #open the file
  currFile = open(filename, 'r')
  
  #Convert
  output = 'Kartnite Stats - ' + today + '.pdf'
  pdfkit.from_file(currFile, output_path=output, configuration=config,options={"enable-local-file-access": ""})
  print('Conversion Complete...')

  return output

#this is for emailing the created PDF to the player that it was generated for
import yagmail
def sendReport(player,userEmail,userPass,message,pdfFile):

  print('Creating Email....')
  #A dictonary of Players Names and their prefered Email addresses
  emails = {'Pat' : 'patrick.marinich@gmail.com',
            'Kevin' : 'kevinfrancisjr@gmail.com',
            'Chris' : 'chrispauldragone@gmail.com',
            'Demitri' : 'dforand20@gmail.com',
            'Joe' : 'frallerjo@gmail.com',
            'Karla' : 'karlavsetzer@gmail.com'}

  #the user inputs their email infromation, to send the email
  user = yagmail.SMTP(user=userEmail, password=userPass)

  # Returns the date for file name
  today = date.today()
  today = date.isoformat(today)

  #uses the dictionary to get the email for the reciepient
  user.send(to=emails[player], subject=('Kartnite Stats from: ' +  today), contents=message,attachments = pdfFile)

  print('Report Delievered To ', player, '!')