**Miscellaneous Score Documentation**
Patrick Marinich

**Description** - Miscellaneous Score is a metric which tracks smaller in game events such as shock dodges, blue shells dodges, and times that a player was hit by a blue shell. 

**Motivation** - A stat which culminates all of the little in-game actions that we track with stats.

**How is it calculated?**

Misc Score is determined by the amount of “events” that happen to you per race. Typically the only main one that happens frequently is being hit by a blue shell, so a large weighting of this statistic is measured by how often a player is targeted by them. In addition this stat also includes shock dodges since they are also something that we track. This is then divided by the amount of GPs played, so it is a value where it represents how often per GP these “events” happen.

Misc Score is calculated by 

(c1*Blue Shell Dodges + c2* Blue Shells Hit + c3 * Shock Dodges) / GPs Played

Currently the values are at 
- 8 points per blue shell dodge
- 0.5 points per blue shell hit
- 2 points per shock dodge

Overall this stat just shows how often these events happen. It is highly correlated with skill as it takes being in first to be targeted with a blue shell, or timing to dodge a shock, but there is still a bit of luck and randomness involved with this stat. As it currently stats it is being used as a pseudo tie breaker among the Seading Power Points leaderboard as it has a weight of 1. It will probably stick around in this capacity as it acts as a base case of important when comparing other stats to one another. It also has a place in Kartnite Stats as currently it is the only stat which is comprised entirely of in-game item events.
