<!-----
Used the Docs to Markdown google drive extention for this!

It is not a perfect conversion as the equations did not copy perfectaly but until I find a better solution, inline formulas will work!
-Pat
----->
# Kartnite Versus Rating Documentation

Patrick Marinich




## <span style="text-decoration:underline;">Motivation</span>

The goal of the creation of Kartnite Versus Rating (KVR) is to have a player rating that changes after races depending on the KVR of both the player and their opponents. There is heavy motivation from the ELO scale in chess. The end goal for KVR is for it to be able to emulate the ELO scale in a completely different environment


## <span style="text-decoration:underline;">Notiable Challenges</span>

The first challenge is that there is an obvious difference between Chess and Mario Kart, Chess is a 2 player zero-sum game, meaning there is a winner and a loser, where as Mario Kart has 12 player races, with any player being able to get any position in any given race. Chess has 3 possible outcomes of a game, Player 1 wins, Player 2 wins, or a tie. Mario Kart has 12! (479,001,600) different outcome possibilities every given race. 

Another challenge is that Mario Kart is not a zero-sum game, a player can have 12 different score outcomes, and a ‘win’ can be defined in a multitude of different ways depending on the skill level of the player. 

The end goal of KVR is to address these challanges, and create a system like ELO which can be used as a predictive measure or skill rating in the game of Mario Kart Wii




## <span style="text-decoration:underline;">What is ELO</span>

ELO is the rating system used in chess to compare players to one another. A common misconception is that ELO is a representation of a players skill level. This is not the case although they are correlated. ELO is a predictive measurement that is created from a players game history. A players ELO can/will change based on their previous match outcomes as well as their opponents. Beating a stronger opponent will increase ELO more then beating a weaker opponent, the effect is reversed for losses, losing to a weaker player is worse then losing to a stronger player.

ELO is used a predictive measurement, a player with 200 more ELO points compared to their opponent has a 75% chance of a favorable outcome. A favoriable outcome is defined as their chance to win plus half of their chance to tie.

Change in ELO after a match is calculated by



Ra' = Ra + K(Sa - Ea)



Where 



* Ra: Current rating
* K: A factor of stability
* Sa: Scored points in a match
* Ea: Expected Points of the match

K is defined by the maximum amount that a rating can change given one individual game. This value can be changed based on how much a players skill level can change over time. In chess it is a low value as skill typically is acquired slowly.

Sa in chess is 1 for a win, 0.5 for a tie, and 0 for a loss.

Ea has a calculation of its own, and it is defined by


Ea = 1 / (1+10 ^ ((Ra-Rb)/400) 

 

Where Ra is your current rating and Rb is your opponents current rating. 


## KVR Thought Process

To keep KVR similar in spirit to the ELO rating, the change in KVR will be defined in the exact same way as the ELO rating.


KVRa' = KVRa + F(Sa - EVa)


Where



* KVRa’: The change in KVR
* KVRa: Current KVR
* F: The maximum amount a score can change after a singular race
* Sa: Score points in a race
* EVa: Expected score 

Mario Kart Wii races are typically 4 people and 8 computers. For our play sessions we play with the computers on normal difficulty. For simplicities purposes all of the 8 computer players will have the same VR for calculations. 

**Note:** In development I will include a randomness factor in the computers VR so that it more accurately reflects the variations in computer’s skill over each race.

The calculation for EVa is what will have to change in regards to the ELO scale. Chess is a two player game with basically a binary output (disregarding the tie), Mario Kart has a very different set-up and outcome space, which will have to be accounted for in its expected value calculation.




## <span style="text-decoration:underline;">Math behind EVa</span>

I chose to use EVa as the label for this variable as the calculation will represent more of an expected value rather then a perfect decimal answer. Mario Kart scores range from 0-15, where 0 points are scored for 12th and 15 for 1st place. 

This is not a linear scoring scale, below is the table of points compared to final race standings


<table>
  <tr>
   <td>Placement
   </td>
   <td>1
   </td>
   <td>2
   </td>
   <td>3
   </td>
   <td>4
   </td>
   <td>5
   </td>
   <td>6
   </td>
   <td>7
   </td>
   <td>8
   </td>
   <td>9
   </td>
   <td>10
   </td>
   <td>11
   </td>
   <td>12
   </td>
  </tr>
  <tr>
   <td>Score
   </td>
   <td>15
   </td>
   <td>12
   </td>
   <td>10
   </td>
   <td>8
   </td>
   <td>7
   </td>
   <td>6
   </td>
   <td>5
   </td>
   <td>4
   </td>
   <td>3
   </td>
   <td>2
   </td>
   <td>1
   </td>
   <td>0
   </td>
  </tr>
</table>


The goal will be to determine what place each player is expected to get, and then plugging that value into the peicewise function defined by the table above. 



f(x) = -3x+18 ; 1<= x <= 2
         -2x+16; 2 < x <= 4
         -x + 12 ; 4 < x <= 12




<span style="text-decoration:underline;">Determining the Expected Placement of a Player</span>

Imagine viewing each race from the prospective of an individual player. To get first that player must beat all 11 other competitors. To get second, they must beat 10 others and lose to one. This pattern can be continued all the way down to 12th place, where to get 12th the player must lose to all 11 opponents.

This means that a race can be boiled down to a comparision of 11 different events, and determining and outcome based on those 11 events. (This will further be examined in the scenarios below) Lets consider a win of one of these 11 comparisons to be worth 1, and a loss to be worth 0. In effect this is converting a race of Mario Kart to 11 zero-sum events that can be used to calculate a score

KVR of a normal computer will be defined at 5000 KVR, 5000 is chosen as homage to the MKOnline starting VR rating of 5000. In addition to this fact, a human player with zero race history will also be defined to have a KVR of 5000. 

Senerio 1 (Base case) - Imagine a scenario where all 12 racers have the same KVR going into the race. It would make intuative sense that each player will have an identical chance of getting each position.


<table>
  <tr>
   <td>Players
   </td>
   <td>Human 1
   </td>
   <td>Human 2
   </td>
   <td>Human 3
   </td>
   <td>Human 4
   </td>
   <td>Com1
   </td>
   <td>Com 2
   </td>
   <td>Com3
   </td>
   <td>Com 4
   </td>
   <td>Com5
   </td>
   <td>Com 6
   </td>
   <td>Com7
   </td>
   <td>Com 8
   </td>
  </tr>
  <tr>
   <td>KVR
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
  </tr>
</table>


Position Analysis of Human 1 in this scenario


<table>
  <tr>
   <td>Placement
   </td>
   <td>1
   </td>
   <td>2
   </td>
   <td>3
   </td>
   <td>4
   </td>
   <td>5
   </td>
   <td>6
   </td>
   <td>7
   </td>
   <td>8
   </td>
   <td>9
   </td>
   <td>10
   </td>
   <td>11
   </td>
   <td>12
   </td>
  </tr>
  <tr>
   <td>Percentage
   </td>
   <td>8.33%
   </td>
   <td>8.33%
   </td>
   <td>8.33%
   </td>
   <td>8.33%
   </td>
   <td>8.33%
   </td>
   <td>8.33%
   </td>
   <td>8.33%
   </td>
   <td>8.33%
   </td>
   <td>8.33%
   </td>
   <td>8.33%
   </td>
   <td>8.33%
   </td>
   <td>8.33%
   </td>
  </tr>
</table>


In this scenario, the expected placement of Player A would be 6.5th place, this can be found by using a standard expected value calculation to prove this idea.


    12
n = SUMMATION((.0833)(n)) ~= 6.5
    n = 1



However this same calculation using the zero-sum method mentioned shows the same results

Position of Analysis of Human 1, using the zero sum method


<table>
  <tr>
   <td>Event (Winning against player x)
   </td>
   <td>Human 2
   </td>
   <td>Human 3
   </td>
   <td>Human 4
   </td>
   <td>Com 1
   </td>
   <td>Com 2
   </td>
   <td>Com 3
   </td>
   <td>Com 4
   </td>
   <td>Com 5
   </td>
   <td>Com 6
   </td>
   <td>Com 7
   </td>
   <td>Com 8
   </td>
  </tr>
  <tr>
   <td>Odds of Success
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
  </tr>
</table>


Since a success is defined by 1, and a loss by 0, the total amount of expected wins comes out to be 5.5 (11*0.5). Now since this is the number of expected wins, take this value and then subtract from the total racers.  12 - 5.5 = 6.5, which matches the expected value when done with the percentage calculations

Senerio 2 - Human 1 has 500 KVR more then everybody else. In KVR standards I define a KVR of 500 points difference to be a 10% increase in probability of a favoriable outcome. 

How would this make an impact on the probabilities?


<table>
  <tr>
   <td>Players
   </td>
   <td>Human 1
   </td>
   <td>Human 2
   </td>
   <td>Human 3
   </td>
   <td>Human 4
   </td>
   <td>Com1
   </td>
   <td>Com 2
   </td>
   <td>Com3
   </td>
   <td>Com 4
   </td>
   <td>Com5
   </td>
   <td>Com 6
   </td>
   <td>Com7
   </td>
   <td>Com 8
   </td>
  </tr>
  <tr>
   <td>KVR
   </td>
   <td>5500
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
   <td>5000
   </td>
  </tr>
</table>


With every KVR being the same, then the probabilities of any player beating any other player are exactly the same, and the placement positions all have the same probabilities. However as defined above, a 500 Point difference is defined as a 10% increase in the probability to beat a player. A 50/50 race from above goes to a 60/40 race when comparing every individual match up.

By doing the same analysis for Human 1 as in scenario 1, we can determine their expected placement value


<table>
  <tr>
   <td>Event (Winning against player x)
   </td>
   <td>Human 2
   </td>
   <td>Human 3
   </td>
   <td>Human 4
   </td>
   <td>Com 1
   </td>
   <td>Com 2
   </td>
   <td>Com 3
   </td>
   <td>Com 4
   </td>
   <td>Com 5
   </td>
   <td>Com 6
   </td>
   <td>Com 7
   </td>
   <td>Com 8
   </td>
  </tr>
  <tr>
   <td>Odds of Success
   </td>
   <td>0.6
   </td>
   <td>0.6
   </td>
   <td>0.6
   </td>
   <td>0.6
   </td>
   <td>0.6
   </td>
   <td>0.6
   </td>
   <td>0.6
   </td>
   <td>0.6
   </td>
   <td>0.6
   </td>
   <td>0.6
   </td>
   <td>0.6
   </td>
  </tr>
</table>


Human 1’s expected win count rises to 6.6 (from 5.5 in scenario 1) and thus their new expected placement is 5.4

This same calculation can be done for Human 2, to see how their placement is projected to change when a player of 10% higher skill enters the race


<table>
  <tr>
   <td>Event (Winning against player x)
   </td>
   <td>Human 1
   </td>
   <td>Human 3
   </td>
   <td>Human 4
   </td>
   <td>Com 1
   </td>
   <td>Com 2
   </td>
   <td>Com 3
   </td>
   <td>Com 4
   </td>
   <td>Com 5
   </td>
   <td>Com 6
   </td>
   <td>Com 7
   </td>
   <td>Com 8
   </td>
  </tr>
  <tr>
   <td>Odds of Success
   </td>
   <td>0.4
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
   <td>0.5
   </td>
  </tr>
</table>


Human 2’s expected win count fell from 5.5 to 5.4 when comparing from scenario 1, and this makes sense as one player entering that is only marginally better should not lower the expected race placement by all that much Human 2’s expected placement fell from 6.5 to 6.6.

Scenario 3 - Something more complex and realistic

Here are the sample KVRs for this scenario.


<table>
  <tr>
   <td>Players
   </td>
   <td>Human 1
   </td>
   <td>Human 2
   </td>
   <td>Human 3
   </td>
   <td>Human 4
   </td>
   <td>Com1
   </td>
   <td>Com 2
   </td>
   <td>Com3
   </td>
   <td>Com 4
   </td>
   <td>Com5
   </td>
   <td>Com 6
   </td>
   <td>Com7
   </td>
   <td>Com 8
   </td>
  </tr>
  <tr>
   <td>KVR
   </td>
   <td>8500
   </td>
   <td>5200
   </td>
   <td>4500
   </td>
   <td>7250
   </td>
   <td>5200
   </td>
   <td>4600
   </td>
   <td>5800
   </td>
   <td>4300
   </td>
   <td>5000
   </td>
   <td>5500
   </td>
   <td>5750
   </td>
   <td>4700
   </td>
  </tr>
</table>


**Note: **During code implementation, the COMs will have a range of KVRs that they can have, from 4750-5250 This range will help account for the varying skills levels between the COMs any given race. Since it will be impossible to predict which com places where before a race happens, this will be randomized as to which COM had which KVR.

Using Senerio 2 as a guild. 500 points difference equates to a .1 change in probability of success.

Thus success probability of any given event can be calculated by 


P(success) = 0.5 + ((KVRa - KVRb) / 5000)

However this formula poses an issue, Probability can never be over 1, what if the difference is so large that it says that there is a 120% probability of success. This in practice is impossible, so instead of doing a linear model, an exponential model should be used for this calculation

Here is a table of point differences and probabilities of success, increasing by 10% every 500 points


<table>
  <tr>
   <td>Difference
   </td>
   <td>0
   </td>
   <td>500
   </td>
   <td>1000
   </td>
   <td>1500
   </td>
   <td>2000
   </td>
   <td>2500
   </td>
   <td>3000
   </td>
   <td>3500
   </td>
  </tr>
  <tr>
   <td>Win %
   </td>
   <td>0.5
   </td>
   <td>0.6
   </td>
   <td>0.66
   </td>
   <td>.726
   </td>
   <td>.7986
   </td>
   <td>.87846
   </td>
   <td>.966306
   </td>
   <td>1.09
   </td>
  </tr>
</table>


This again will cross over 1, but the first few values can be approximated very well by the exponential model below

Win % = 0.5 +- 0.5 * (1-exp((-1/2500) * x))   
(+- is plus/minus depending on which player is favored or not favored to win)


* When x >= 0
* Where x is the absolute value of the points difference,
* + is used for the player with higher KVR
* - is used for the player with the lower KVR.

Here is a new table, where that equation is representing win%


<table>
  <tr>
   <td>Difference
   </td>
   <td>0
   </td>
   <td>500
   </td>
   <td>1000
   </td>
   <td>1500
   </td>
   <td>2000
   </td>
   <td>2500
   </td>
   <td>3000
   </td>
   <td>3500
   </td>
  </tr>
  <tr>
   <td>Win %
   </td>
   <td>0.5
   </td>
   <td>0.5906
   </td>
   <td>0.66484
   </td>
   <td>.72559
   </td>
   <td>.775335
   </td>
   <td>0.81606
   </td>
   <td>0.84940
   </td>
   <td>0.8767
   </td>
  </tr>
</table>


By using this function to determin the win probability, the value will never get over 1 and thus will satisfy the rules of probability. This will be the function used to determine the probability of a win when comparing two players for EVa purposes.

Lets use this function to analyize Human 1’s  expected win counts and expected placements.


<table>
  <tr>
   <td>Event (Winning against player x)
   </td>
   <td>Human 2
   </td>
   <td>Human 3
   </td>
   <td>Human 4
   </td>
   <td>Com 1
   </td>
   <td>Com 2
   </td>
   <td>Com 3
   </td>
   <td>Com 4
   </td>
   <td>Com 5
   </td>
   <td>Com 6
   </td>
   <td>Com 7
   </td>
   <td>Com 8
   </td>
  </tr>
  <tr>
   <td>Difference in KVR
   </td>
   <td>3300
   </td>
   <td>4000
   </td>
   <td>1250
   </td>
   <td>3300
   </td>
   <td>3900
   </td>
   <td>2700
   </td>
   <td>4200
   </td>
   <td>3500
   </td>
   <td>3000
   </td>
   <td>2750
   </td>
   <td>3800
   </td>
  </tr>
  <tr>
   <td>% win expected
   </td>
   <td>0.866
   </td>
   <td>0.899
   </td>
   <td>0.696
   </td>
   <td>0.866
   </td>
   <td>0.8949
   </td>
   <td>0.830
   </td>
   <td>0.9068
   </td>
   <td>0.876
   </td>
   <td>0.849
   </td>
   <td>0.833
   </td>
   <td>0.89
   </td>
  </tr>
</table>


When summing up all of the expected win counts, Human 1 is expected to get 9.405 wins or get 2.5th place in this race. This would mean only getting 1st or 2nd would raise their KVR, any other placement will lower it.


## <span style="text-decoration:underline;"> Overall Final Calculation of KVR</span>

Variable Definitions:



* KVRa - Player’s Current KVR
* KVRA- player’s new KVR after a race
* F - A scaling factor (KVR will have it set to 20)
* Sa - Points Scored in a race
* EVa - Expected amount of points scored given the opponets
* x - Wins Expected, when compared to each racer individually

KVRa' = KVRa + F(Sa - EVa)

EVa =    -3x+18 ; 1<= x <= 2  OR
         -2x+16; 2 < x <= 4   OR
         -x + 12 ; 4 < x <= 12

x = 0.5 +- 0.5 * (1-exp((-1/2500) * x))   
(where +- is plus/minus)
 
