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
    
  #alltime stats
  kartDataAllTime = allTime.worksheet('Total Scores').get_all_values()
  RaceCountAllTime = allTime.worksheet('Race Count').get_all_values()
  WinsAllTime = allTime.worksheet('GP Wins').get_all_values()
  ShockAllTime = allTime.worksheet('Shock Dodges').get_all_values()

  OwnedScoreAllTime = allTime.worksheet('Owned Score').get_all_values()

  BlueAllTime = allTime.worksheet('Blue Shells').get_all_values()
  SeedingAllTime = allTime.worksheet('All-Time Seeding').get_all_values()
  

  print('Analyzing Old and New Data....')

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
        seasonalFirstPlaceEquivilent = 0
      else:
        seasonalAverage = seasonalTotalPoints/seasonalTotalRaces
        seasonalFirstPlaceRate = (int(dfSeasonWins.at[0,player]) / (seasonalTotalRaces/8))*100
        seasonalAvgGPScore = (seasonalTotalPoints) / (seasonalTotalRaces/8)
        seasonalFirstPlaceEquivilent = seasonalTotalPoints/15

    #Players AllTime stats
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
        allTimeFirstPlaceEquivilent = 0
      else:
        allTimeAverage =  allTimeTotalPoints/ allTimeTotalRaces
        allTimeFirstPlaceRate = (int(dfAllTimeWins.at[0,player]) / (allTimeTotalRaces/8))*100
        allTimeAvgGPScore = (allTimeTotalPoints) / ( allTimeTotalRaces/8)
        allTimeFirstPlaceEquivilent =  allTimeTotalPoints/15



  #gets all of the all time leaderboards (10), this is needed all the way up here so that the players seed can be found
  dfPowerPoints1,dfNormalizedKart1,dfKartRating1,dfMiscScore1,dfAllTimeWins1,dfAllTimeAverage1,dfAllTimeShockDodges1,dfAllTimeBlueShells1,dfAllTimeRaceCount1,dfAllTimeTotalPoints1 = getAllTimeLeaderboads(season,allTime,TrackIndex,display = False)


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
  
  #ADD PARAMATERS



  ##Creates the first page of the PDF, has the player name, and thier seasonal and all time stats. #find what is needed and pass them in
  coverPage(player,seasonalTotalPoints,seasonalAverage,seasonalTotalRaces,seasonalFirstPlaceEquivilent,allTimeAverage,
  dfSeasonWins,seasonalFirstPlaceRate,allTimeFirstPlaceRate,seasonalAvgGPScore,allTimeAvgGPScore,seasonalTracksOwned,allTimeTracksOwned,dfSeasonShock,
  dfSeasonBlue,dfSeasonOwnedScore, allTimeTotalPoints,allTimeTotalRaces,allTimeFirstPlaceEquivilent,dfAllTimeWins,dfAllTimeShock,dfAllTimeBlue,dfAllTimeOwnedScore,dfPowerPoints1) 
  
  time.sleep(60) #API calls aint free

  #shows all of the current and all time track mvps
  trackMVPPage(dfSeasonScores,dfSeasonRaceCount,TrackIndex,dfAllTimeScores,dfAllTimeRaceCount) 


  #page with seasonal leaderbaords
  seasonalLeaderboardPage(season,TrackIndex,dfSeasonScores,dfSeasonRaceCount,dfSeasonWins,dfSeasonShock,dfSeasonBlue) 

  allTimeLeaderboardsPages(dfPowerPoints1,dfNormalizedKart1,dfKartRating1,dfMiscScore1,dfAllTimeWins1,dfAllTimeAverage1,dfAllTimeShockDodges1,
    dfAllTimeBlueShells1,dfAllTimeRaceCount1,dfAllTimeTotalPoints1)  #two pages with all time boards

    
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
  print('<style> div.statbox {text-align: left; display: inline-block; align-items:left; width: 30%; height: 250px; border: 3px solid black; padding: 7px; margin: auto; vertical-align: top;} </style>')
  print('<style> div.leaderboard {text-align:center; display: inline-block; align-items:center; width: 45%; height: 950px; border: 1px solid black; padding: 4px; margin: auto; vertical-align: top; margin:auto;} </style>')
  print('<style> div.empty {display: flex; width: 100%; height: 15px;} </style>')
  print('<style> div.statbox2 {text-align: left; display: inline-block; align-items:left; width: 30%; height: 325px; border: 3px solid black; padding: 7px; margin: auto; vertical-align: top;text-overflow: ellipsis;white-space: nowrap;overflow: hidden; } </style>')
  print('<style> .arrow {border: solid black;border-width: 0 3px 3px 0;display: inline-block;padding: 3px;} .up {transform: rotate(-135deg); -webkit-transform: rotate(-135deg); border: solid green;border-width: 0 3px 3px 0;}.down {transform: rotate(45deg);-webkit-transform: rotate(45deg); border: solid red; border-width: 0 3px 3px 0;} </style>')

def coverPage(player,seasonalTotalPoints,seasonalAverage,seasonalTotalRaces,seasonalFirstPlaceEquivilent,allTimeAverage,
  dfSeasonWins,seasonalFirstPlaceRate,allTimeFirstPlaceRate,seasonalAvgGPScore,allTimeAvgGPScore,seasonalTracksOwned,allTimeTracksOwned,dfSeasonShock,
  dfSeasonBlue,dfSeasonOwnedScore, allTimeTotalPoints,allTimeTotalRaces,allTimeFirstPlaceEquivilent,dfAllTimeWins,dfAllTimeShock,dfAllTimeBlue,dfAllTimeOwnedScore,dfPowerPoints1):
 
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

  print('<p>First Place Equivalents: ', seasonalFirstPlaceEquivilent,'</p>')

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
  print('<p>First Place Equivalents: ',  allTimeFirstPlaceEquivilent,'</p>')

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

  #page split
  print('<p style= \"page-break-after: always;\"> &nbsp; </p>')
  print('<p style= \"page-break-before: always;\"> &nbsp; </p>')

def trackMVPPage(dfSeasonScores,dfSeasonRaceCount,TrackIndex,dfAllTimeScores,dfAllTimeRaceCount):

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

def seasonalLeaderboardPage(season,TrackIndex,dfSeasonScores,dfSeasonRaceCount,dfSeasonWins,dfSeasonShock,dfSeasonBlue):

  #page split
  print('<p style= \"page-break-after: always;\"> &nbsp; </p>')
  print('<p style= \"page-break-before: always;\"> &nbsp; </p>')

  
  #header
  print('<div class =\"center\">')
  print('<h1> Seasonal Leaderboards </h1>')
  print('</div>')

  #6 stat boxes for seasonal leaderboards

  #a work around to get around the google api limit on 300 reads per minute, I do not have the current budget
  #to pay for more api calls lol

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

  #end of page bar
  print('<br>')
  print('<div class=\"bar\"> </div>')

def allTimeLeaderboardsPages(dfPowerPoints1,dfNormalizedKart1,dfKartRating1,dfMiscScore1,dfAllTimeWins1,dfAllTimeAverage1,dfAllTimeShockDodges1,
    dfAllTimeBlueShells1,dfAllTimeRaceCount1,dfAllTimeTotalPoints1):

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

  #statbox 10 points scored
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
  pdfkit.from_file(currFile, output_path=output, configuration=config)
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