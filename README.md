# Mario-Kart-Stats-Project

**Background:** My friends and I have been massive fans of the Mario Kart Wii game for years now. We tend to get into friendly arguments about who is the best both overall and on any given race. After these debates happened one of my friends created an excell spreadsheet to hold our race data so that we can compare our overall stats with one another to determine who is the best. The issue that we found very quickly was that it was slow and tedious to enter in and calculate all of the different things that we wanted to see. Thus the idea for a Python script of *Kartnite Stats* was born. Written in Google Collab's Python Envoirnment this script allows for us to have ease of input and access more data then we prevously thought possible. 

**Info:** The Google Collab Files have documentation written on them with functionality and patch notes written on them, so listed below will be a summary.

*The first version uploaded to github was version 2.1*


**Below is the notes from the most recent google colab file**

**Kartnite Stats** v3.2

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


**Important:** Make sure to run all cells before running the main cell, the main cell is the last one.


**Patch Notes**

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

