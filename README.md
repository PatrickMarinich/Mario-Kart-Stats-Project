# Mario-Kart-Stats-Project

**News:** I have created a python version of *Mario Kart Stats* which can be run in vs code or any other python envoirnment. The majority of the code is exactly the same, but a couple of work around were needed to get ahold of the google drive authententication after moving off of their platform. This can be run using the MAIN.py file in the Kartnite_Python folder.

**Repo Contents:** This repository will contain the current and all the previous versions of the *Mario Kart Stats Project*. The highest version number will be the most recent one and will most likely located at the bottom of the repo right above the read me. In addition I will do my best to include the updated auto generated html code as well. This html code is a formatted pdf which is a condensed version of the viewable stats. The HTML fine here will be updated whenever I update, add to, or change the html pdf.

**Background:** My friends and I have been massive fans of the Mario Kart Wii game for years now. We tend to get into friendly arguments about who is the best both overall and on any given race. After these debates happened one of my friends created an excell spreadsheet to hold our race data so that we can compare our overall stats with one another to determine who is the best. The issue that we found very quickly was that it was slow and tedious to enter in and calculate all of the different things that we wanted to see. Thus the idea for a Python script of *Kartnite Stats* was born. Written in Google Collab's Python Envoirnment this script allows for us to have ease of input and access more data then we prevously thought possible. 

**Note:** This is the first larger scale project that I have undertaken. I Have learned a bunch throughout the ongoing development process, This is mainly a for fun project, some of the code may not be optimized, but it accomplishes the main goal. Overall I continue to add features overtime whenever I find both the time and the motivation to implement them. As of now this is just used by my friends and I, and it has been a great place to test new ideas and learn new things.

*The first version uploaded to github was version 2.1*

**Things I've Learned During Development**
* Pandas DataFrame Functionality
* Connecting to Google Sheets API
* Using a Pandas DataFrame object to overrite a Google Sheet File, which allows for savable data
* Statical Analysis to create metrics such as Kart Score and Kart Rating
* Python output redirection
* Python Functions and defaulting paramaters
* Basic HTML and CSS syntax
* Conversion for HTML to PDF using Python
* Using Python to send Emails via Gmail

**Below is the notes from the most recent google colab file**

**Kartnite Stats** v3.2.6

*Written by: Patrick Marinich*

**Goal:** This scripts goal is to take user inputted *Mario Kart Wii* races and other stats and save them to a database to be used for calculations and analysis when user requested. 

**Current Functionalities**

*   Take in a user inputted race, with the track, players, and scores, and adds them to the database of all scores
*   Keep track of how many times each player playes on a singular track
* Get the average score per track of all of the players
* Determine which player is the best on any specific track
* A leaderboard to display the ordering of player seeding (power rankings)
* The ability to search for all the stats of a specifc track, including total points, player averages, and the individual track leaderboards
* The ability to search of all of the stats of a individual player, including total points, track averages, Track MVPs, and total power ranking points (Kart Score)
* The ability to correct mistakes in entering race points, by having a user setting to manually edit the points of a specific player
* Ability to view the database containing all of the data
* Ability to view a players seasonal stats and their all time stats. 
* Different seasonal leaderboards to show who is on top! 
* A Player Profile which can be generated and emailed directally to a specified player given their email address.
* These profiles include all of a players seasonal stats and all time stats along with all of the leaderboards that this software can produce. It is like a snapshot of that player's stats


**Important:** Make sure to run all cells before running the main cell, the main cell is the last one.


**Patch Notes**
V3.2.6 (11/20/2022)
- Re-orginized the player profile code so that re-ordering the pages is possible if desired
- New Pages should be able to be created in thge future easier as well
- Bug fixes

V3.2.5 (11/1/2022)
- Created a full python version of this application to allow for easy collaberation in the future.
- Bug fixes

V3.2.4 (8/29/22)
- An awards list was added to player profiles.
  - Awards will be created and given on a seasonal basis
  - a voting committee will be comprised of the most active players of the season and they will vote for each award and who they think is most deserving of it
  - The winner of the award will have the award showcased on their player profile in a new section titled 'Trophy case'
  - Awards may vary from season to season
- Made adjustments in scoring in prep for the next season
  - Reduced points for point scored to 0.25 from 0.35
  - Increased GP points from 100 to 125
  - Blue shell dodge to 8 points from 9 
  - Shock dodge to 3 points from 3.5
  - Blue shell hit to 0.5 poitns from 0.25
- Adjusted the calculation of Track MVP to a more average based approach, lowered the percentage of total points, and increased the percentage of average
- Created the foundational steps in to implementing a new set of stats to be calculated, such as first place count, top 3 count, ect. (not yet live)

V3.2.3 (7/11/22)
- All seasonal and all-time leaderboards were added to the player-profile PDF
- This is using the same dataFrame features as the Track MVPs, however expanded to include leaderboards in inline boxes.
- New Additions
  - 10 All Time Leaderboards
  - 6 Seasonal Leaderboards
  - A header on page one showing the players All-Time Power Seed

v3.2.2 (7/9/22)
  - An update to the PDF Player Profile
  - Uses the pandas df.to_html to include the lists of all of the seasonal and all-time track MVPs
  -Further additions to the PDF are to follow soon!

v3.2.1 (7/1/22)
- All Time Leaderboards are finished!

v3.2 (6/28/22)
 - Kart Rating
  - A new way to rate the players, it is similar to QBR in football where players are ranked out of a specific number, and compared to one another
  - The catigories are:
    - GP win %
    - Average GP Points
    - Tracks Owned Percentage
    - All Time Track Owners
    - Determined 100% by average, as our sample size is large
    - There is a 5 race minimum to qualifiy

- Player Profiles
    - A generated PDF using HTML/CSS formatting
    - This PDF displays both seasonal and all-time stats
    - Inludes progress triangles, to indcate if the player is playing well this current season
    - The PDF is directally emailed to the player onces it is generated

- All Time Leaderboards and other stats (Currently WIP)
  - All Time Power Points
    - Found by looking at placements on other metric leaderboards
    - 4 points per Kart Rating placement
    - 3 points per Normalized Kart Score placement
    - 2 points per Misc Score placement 
  - All Time Normalized Kart Score
  - All Time Kart Rating
  - All Time Misc Score
    - 8 points per blue dodge
    - 0.5 points per blue hit
    - 2 points per shock dodge
  - All Time Average
  - Other fun all Time stats!


v3.1 (6/20/22)
  - A new input (11) which allows the user to view all time stats
  - This feature combines all of the current seasons stats with those in the perminate all time file to get all kinds of total statics about a players performance over time. 
 
  Current stats include:
    1. Total Points
    2. Total Races
    3. Average Placement Points
    4. An estimation on GPs played
    5. GP Wins
    6. GP Win %
    7. Shock Dodges, Blue shells, and other misc stats

v3.0 (5/19/22)

- Seasons Update!
  - Seasons reset every couple of months to allow for play to be broken up during our time at college, currently there will be a summer and winter season
  - This allows for balances changes to be made each season and create a more fair ranking system overtime as rules change
  - An all time ranking will be determined by normializing each seasons points as a precent of their total, thus no matter the scoring system, the maximum possible points achieveavle is 100, before bonuses.
  -To incentivize placement there will be multipliers to the 1st, 2nd, and 3rd highest scorers. 1.25, 1.125, 1.075 respectivley. Thus the maximum possible amount of all-time points to get in a season is 125.
  -Each previous season will have their points reduced by 15% to ensure that the most recent season is the one with the most weight.
- Whats New?
  - A second database was created in google sheets to store all-time data
  - A user option to end the current season and start a new one
    - This function wipes the old season stats to zero and updates the all-time standings instead
  - A new algorythem for determining the best all time player
  - Balance Changes to the scoring system
    - Reducing Points for Track MVP from 2 to 0.25
    - Blue Shell Dodges 2 points
    - Blue Shell Hit .25 points
    - Shock Dodges Increased from 2 to 4 points


v2.3 (5/13/22)
- Blue Shells hit and Blue Shells Dodges implementation 
- Updated Kart Score and Seeding to include these metrics
- New Leaderboards for Blue Shells
- Added New Selection option for user entering Blue Shell Data
- Updated the Display Player Stats Function to include Blue Shells
- Re-orginized Kart Score using Constant variables to allow for quick balance adjustments in the future.
- Added Headings and sections so that the google collab Table of Contents was usuable
- Re-orginized code into these sections so that similar functions are in the same grouping, allows for ease of access


v2.2 (Jan 7 2022)
- Re-design of player stats output
- Re-orginization of code execution order for determining when the database is updated compared to finding track MVPs
-Points Per Race Leaderbaord
-A Feature to view all track MVPs at once
-Re-design of user input options
-Track Nickname functionality for user inputs (currently 77 working track nicknames)


v2.1 (Jan 4 2022)
- Optimization
- Changes to 'Kart Score' 
- MVP Leaderboards Per Track

v2.0 (Jan 3 2022)
 - Adds Shock Dodges 
 - Adds GP Wins
 - Adds Total Race Count
 - Leaderboards

v1.1 (Jan 2nd 2022)
 - Moved the Main Method into a private method, this reduced the need for scrolling

v1.0 (December 27 2021 - December 31st 2021)
 - Importing and Saving Race Data
 - Editing singular race scores incase of mistakes
 - Viewing Track Records + Best Player on the Track
 - Viewing Player Records

 - Editing singular race scores incase of mistakes
 - Viewing Track Records + Best Player on the Track
 - Viewing Player Records

