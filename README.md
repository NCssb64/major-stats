# major-stats
Compiling basic match statistics from majors.

If you want to help: look at "How To Help" section below, and contact widdy

Raw data available here:
https://docs.google.com/spreadsheets/d/1zpuTBg0k5njPZfxUNXf7VUhsi9F1QSBYcaeE1i7PKNE/edit?usp=sharing

To analyze the data (e.g. "how many games between fox and puff at G3?") look at `generate_table.ipynb`.

So far archives count recorded matches only. Because the goal is to include character info (dk, samus, etc) for each match, we don't have a reliable way of getting info for non-recorded matchs.

## Current status (2017-02-27)
  * the archive contains all pools and bracket matches recorded at the following tournaments:
    * BEAST7
    * SSC 2016
    * G3
    * GOML 2016
    * Pound 2016
    * Snosa 2
  
  * Slowly updating archives to include info like "top 8, top 16, WF, GF" etc
    
  * the code `generate_table.ipynb` reads from the spreadsheet:
    * number of matches between characters
    * win % each character has over each other
    * can restrict these results to just bracket matches (or just pools matches)

## To do
  * When listing number of games each character appears in, list 2 players with most games logged as that char
  * get info for non-recorded matches
    * if brackets on smash.gg or challonge, e.g., contained character info, this would be possible for future tournaments.
  * add data from:
    * Shine 2016
    * ODS 2
    * SuperBoomed
    * BossBattle 2
    * DOPTG
    * G4
    * Do people really want to see info from matches before 2016? THE YEAR OF 64?
  * add ability to look up stats for specific player, e.g. "how many games has lord_narwhal played in bracket?"; "what is bacorn's career match % against kirby?"
  * compute ELO?
  
  
## How To Help
If you want to contribute info to the archive, there are a few ways:

1. contributing new archive info (by entering info into spreadsheets, nothing too complicated)
2. checking existing archives for accuracy (please let us know if you find any mistakes)
3. writing code to perform better / more interesting queries

How to contribute archive info:

1. enter your info in a spreadsheet using the same format as this project
  * year | tournament name | player1 | player2 | char1 | char2 | number of winning player | bracket or pool
  * every row is one game
  * **Please** make sure your info is accurate. We'll spot-check contributions -- if a single piece of info is found to be inaccurate from a contributor, we'll throw out their whole contribution.
2. send the spreadsheet to widdy at wdyhssm@gmail.com
