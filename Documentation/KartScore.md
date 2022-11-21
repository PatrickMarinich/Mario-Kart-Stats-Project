**Documentation for Kart Score**
Patrick Marinich


**Motivation** - Kart Score is a general scoring metric that allows for players to compare themselves to one another to see who is preforming better during the current season. I created Kart Score in effort to measure the skill level of Mario kart Players over the course of a given season.

**Notes** - This was the first custom metric that I created to attempt to measure our Mario Kart skill levels. It is far from perfect, however layed the ground work for future metrics, and does still give a partial picture of how each player is performing. 

What is Kart Score - Kart Score is a culmination of points that are awared during a variety of game events. There are six components that go into Kart Score, which overall effect the total.

Kart Score is calculated by c1*GP Wins + c2*Track MVP Points + c3*Race Points + c4 * Track Average Points + c5*Shock Dodge Points + c6*Blue Shell Points, where c1-c6 are constants that may be changed at the start of any given season.

The coefficients can be changed at the end of any given season since at the end of each season the scores are normalized, so that in the all-time rankings the exact kart score values are not taken into account. The normlization of Kart Score takes the percentage of points that a player score compared to the total amount acculmliated so that no matter the scoring breakdown in an individual season the scoring can be compared across seasons.

**Kart Score Breakdown**

c1*GP Wins - GP wins are included as they are a great way to access who the current best player is, the winner of an 8 race GP is given bonus points to their Kart Score (denoted by c1) Typically this has been set to around 100 points but has changed from season to season

c2*Track MVP Points - This is the trickiest of the terms to describe, but as a group we have determined that if you are the best player on one of the 33 tracks that we play, you should get a Kart Score Bonus for those tracks. Track MVP Points is a metric that takes into account how often we play those tracks, as it should be weighted more strongly if you are the current leader of a track that we play often. So Track MVP Points are given every time a track is played that you as a player own. The amount of Kart Score per Point has changed drastically as finding a balance was difficult. However A common value used has been 0.5, or half of a point for each player who plays the track. (A standard 4 player race nets the MVP 2 points)

c3*Race Points - These are the total in game points scored by the player. If a player scores 98 points in a GP they will get some amount of Kart Score. Typically this value (c3) has been 1, but we have been experimenting with new values

c4*Track Average Points - Since Kart Score was the earliest of the custom statistics created for Kartnite Stats, there was very little all-time data available to us to use (All-Time Stats werent being tracked yet) and thus the best way I thought to incorporate some type of longer lasting stat was to include points for your current track average on every track. When developed Kart Score gave 4 points to each point of Track average that you had on the track. I.e If a player had a perfect average of 15 points they would be awarded 60 Kart Score Points. 

c5*Shock Dodge Points and c6*Blue Shell Points - These were small points that were awared for doing in game things such as dodging a shock or getting hit with a blue shell. These points never amounted to too much over the course of the season as they were mostly luck based, however dodging a blue shell (i.e with a mushroom) did award significant points since that was a more skill based action. 

Conclusion - This is how Kart Score is calculated. Kart Score is still used within Kartnite Stats as it is still a good metric to determine how players are playing during a season. However there are downsides with this metric, which is why other metrics have been and are being created to try and address the imperfections had with this statistic. The biggest flaw is that somebody with more races by nature is going to have a higher Kart Score due to its cumulative nature, because of this the next custom stat that will be created will be one that takes all time stats more into account. 

