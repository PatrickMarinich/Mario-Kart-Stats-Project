# Mario-Kart-Stats-Project

**Recent Commit Changes:** Version 3.3.1!!! Version updates are in the patch notes file in the documentation folder

**Background:** My friends and I have been massive fans of the Mario Kart Wii game for years now. We tend to get into friendly arguments about who is the best both overall and on any given race. After these debates happened one of my friends created an excell spreadsheet to hold our race data so that we can compare our overall stats with one another to determine who is the best. The issue that we found very quickly was that it was slow and tedious to enter in and calculate all of the different things that we wanted to see. Thus the idea for a Python script of *Kartnite Stats* was born. Written in Google Collab's Python Envoirnment this script allows for us to have ease of input and access more data then we prevously thought possible. 

**Note:** This is the first larger scale project that I have undertaken. I Have learned a bunch throughout the ongoing development process, This is mainly a for fun project, some of the code may not be optimized, but it accomplishes the main goal. Overall I continue to add features over time whenever I find both the time and the motivation to implement them. As of now this is just used by my friends and I, and it has been a great place to test new ideas and learn new things.

**Table Of Contents:**
  - Documentation - This folder contains any and all documentation about Kartnite Stats, that I have written up
    - Patch Notes - Version Updates go here!
    - KartRating - A custom stat and its documentation -> An Average Based Stat
    - KartSore - A custom stat and its documentation -> A Cumulative Stat
    - KartVersusRating - A custom stat and its documentation -> A Stat similar to chess ELO, aimed to taking into account both your outcomes and opponets strength overtime.
    - MiscellenousScore - A custom stat and its documentation -> A Stat for Item Usuage
    - SeedingPowerPoints - A custom stat and its documentation  -> A Stat to Determine the Best Overall Player
  - Kartnite_Python - Kartnite_Python is responsible for the generation of the Player Profiles
    - Contants.py - Contains any programming constants used, it also contains credits and player awards
    - InputOutput.py - Contains the I/O logic for the user. Allows for user choice and different functionalities of the program
    - LeaderboardGenerators.py - Contains the functions which generate the different leaderboards
    - MAIN.py - Run this file to run the code, it calls the I/O file.
    - PlayerProfile.py - The file that contains all the code to generate the player profile pdf
    - StatGetters.py - The functions which generate different stats for the user to view, or to be included in the player proflie
    - wkhtmltopdf.exe - Program used to convert from html to a pdf (did not create this it is found here https://github.com/wkhtmltopdf/wkhtmltopdf)
  - Sample_HTML_Outputs - Will contain an example of the HTML output of the player profile, so that it can be looked at over time. This will be updated with any major changes in the look of the player profile
  - Kartnite_Stats_Input.ipynb - The file used to input stats to the data base, it was origionally the full program, but it was condensed for simplicity to only have the functionality of inputting data.



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
* Working with The Google Sheets API

**Goal:** This scripts goal is to take user inputted *Mario Kart Wii* races and other stats and save them to a "database" to be used for calculations and analysis when user requested. 

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
* Includes Custom statical metrics that I have created to help show our comparative skill levels
* Player awards are voted on by us at the end of a season, and they can be added to the player profiles!




