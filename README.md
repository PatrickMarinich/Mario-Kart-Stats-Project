# Mario-Kart-Stats-Project

**Recent Commit Changes:** Re-Orginization of ReadMe, added Documentation Folder, small bug fixes

**Background:** My friends and I have been massive fans of the Mario Kart Wii game for years now. We tend to get into friendly arguments about who is the best both overall and on any given race. After these debates happened one of my friends created an excell spreadsheet to hold our race data so that we can compare our overall stats with one another to determine who is the best. The issue that we found very quickly was that it was slow and tedious to enter in and calculate all of the different things that we wanted to see. Thus the idea for a Python script of *Kartnite Stats* was born. Written in Google Collab's Python Envoirnment this script allows for us to have ease of input and access more data then we prevously thought possible. 

**Note:** This is the first larger scale project that I have undertaken. I Have learned a bunch throughout the ongoing development process, This is mainly a for fun project, some of the code may not be optimized, but it accomplishes the main goal. Overall I continue to add features overtime whenever I find both the time and the motivation to implement them. As of now this is just used by my friends and I, and it has been a great place to test new ideas and learn new things.

**Table Of Contents:**
  - Documentation - This folder contains any and all documentation about Kartnite Stats, that I have written up
    - Patch Notes
  - Kartnite_Google_Colab - Contains the current Google Colab version, and the ones previousally uploaded to github (future developement here will be infrequent)
  - Kartnite_Python - Has all of the python files, and is where current developement will happen
    - Contants.py - Contains any programming constants used, it also contains credits and player awards
    - InputFunctions.py - Functions that Allow for user input into the google excel file
    - InputOutput.py - Contains the I/O logic for the user. Allows for user choice and different functionalities of the program
    - LeaderboardGenerators.py - Contains the functions which generate the different leaderboards
    - MAIN.py - Run this file to run the code, it calls the I/O file.
    - PlayerProfile.py - The file that contains all the code to generate the player profile pdf
    - SeasonReset.py - Contains the functions nessassary to reset the season whenever a season is over
    - StatGetters.py - The functions which generate different stats for the user to view, or to be included in the player proflie
    - wkhtmltopdf.exe - Program used to convert from html to a pdf
  - Sample_HTML_Outputs - Will contain an example of the HTML output of the player profile, so that it can be looked at over time. This will be updated with any major changes in the look of the player profile



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




