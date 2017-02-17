# major-stats
Compiling basic match statistics from majors.


Raw data available here:
https://docs.google.com/spreadsheets/d/1zzXHuM-5LYCkfolMJtZg0ycAlJvGzFhXAHNaKwwqA-I/edit?usp=sharing

To analyze the data (e.g. "how many games between fox and puff at G3?") look at `generate_table.ipynb`.

So far all archived match data is from recorded matches only.

## Current status (2017-02-16)
  * the data contains all matches recorded from the following tournaments:
    * G3
    * GOML 2016
    * Pound 2016
    
  * the code tabulates
    * number of matches between characters
    * win % each character has over each other
    * can restrict these results to just bracket matches (or just pools matches)

## To do
  * Most important: get data from non-recorded matches
  * add data from:
    * SNOSA 2
    * SSC 2016
    * Shine 2016
    * ODS 2
    * SuperBoomed
    * BossBattle 2
    * DOPTG
    * G4

  * add ability to look up specific player stats
  * compute ELO?
