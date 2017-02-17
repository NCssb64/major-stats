# major-stats
Compiling basic match statistics from majors.


Raw data available here:
https://docs.google.com/spreadsheets/d/1zzXHuM-5LYCkfolMJtZg0ycAlJvGzFhXAHNaKwwqA-I/edit?usp=sharing

To analyze the data (e.g. "how many games between fox and puff at G3?") look at `generate_table.ipynb`.

So far archives count recorded matches only. Because the goal is to include character info (dk, samus, etc) for each match, we don't have a reliable way of getting info for non-recorded matchs.

## Current status (2017-02-16)
  * the archive contains all pools and bracket matches recorded at the following tournaments:
    * G3
    * GOML 2016
    * Pound 2016
    
  * the code `generate_table.ipynb` tabulates:
    * number of matches between characters
    * win % each character has over each other
    * can restrict these results to just bracket matches (or just pools matches)

## To do
  * get info for non-recorded matches
    * if brackets on smash.gg or challonge, e.g., contained character info, this would be possible for future tournaments.
  * add data from:
    * SNOSA 2
    * SSC 2016
    * Shine 2016
    * ODS 2
    * SuperBoomed
    * BossBattle 2
    * DOPTG
    * G4
    * Do people really want to see info from matches before 2016? THE YEAR OF 64?
  * add ability to look up stats for specific player, e.g. "how many games has lord_narwhal played in bracket?"; "what is bacorn's career match % against kirby?"
  * compute ELO?
