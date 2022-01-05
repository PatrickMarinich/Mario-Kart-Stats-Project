# Mario-Kart-Stats-Project

**Background:** My friends and I have been massive fans of the Mario Kart Wii game for years now. We tend to get into friendly arguments about who is the best both overall and on any given race. After these debates happened one of my friends created an excell spreadsheet to hold our race data so that we can compare our overall stats with one another to determine who is the best. The issue that we found very quickly was that it was slow and tedious to enter in and calculate all of the different things that we wanted to see. Thus the idea for a Python script of *Kartnite* stats was born. Written in Google Collab's Python Envoirnment this script allows for us to have ease of input, and access more data then we prevously thought as possible. 

**Info:** The Google Collab Files have documentation written on them with functionality and patch notes written on them, so listed below will be a summary.

*The first version uploaded to github was version 2.1*

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

**How it works:** The majority of the code revolves around the idea of updating a google sheet file with 5 different sheets on it. The sheets contain: Total Points, Race Counts, Wins, Shock Dodges, and a partial "kart score" which is used for the implemented power ranking system. The google sheet file acts as a database that saves over different iterations of the program being ran, and thus will keep all of our previous race data saved. When the program is run it will read all of the sheets into a Pandas DataFrame object which is what is used for computation throughout the program. Depending on what the user wants to do, either input some type of data or view the data, the program will either save the inputs to the database or display the desired data to the user. 


**Math Used For Rankings:**
Each Track has its own indivudal leaderboard to determine who is the best player on any given track, and the program also has a built in power rankings system which ranks all of the players by their "Kart Score"

The track leaderboard is determined by - ((Players Points/Sum of All Players Points) x 100) + Players Average points per race.

The kart score is determined by the following:
* 100 Points for winning a Grad Prix
* 1 Point for each point scored during a race
* 2 points for each race played on a track that a player is the MVP on
* 2 points for dodging a shock
* 4 races worth of points for a players average track score for each track
The sum of all of these different point methods is a player's "Kart Score"

The power rankings are the "Seeding Leaderboards" which is ordered by "Kart Score"
