import numpy as np
import smash_text as smt
import extract_info as exinf


def skip_this_game( comp_level, bracket_levels_map, level_limits, players, skip_these_players):
        if (bracket_levels_map[comp_level] < level_limits[0]) or (bracket_levels_map[comp_level] > level_limits[1]):
            return True
        play1, play2 = players
        if (play1 in skip_these_players.keys()) or (play2 in skip_these_players.keys()):
            return True


def print_smash_stats( level_limits, skip_these_players, individual_stats ):

    # These help determine which data to use to build the table for the current query
    bracket_levels = [ 'pools', 'bracket', 'top64', 'top32', 'top16', 'top8', 'lf', 'wf', 'gf', 'gf2']
    bracket_levels_map = {'pools': 0,
                'bracket':1,
                'top64':2,
                'top32':3,
                'lq': 3,
                'top16':4,
                'wq': 4,
                'top8':5,
                'ws':5,
                'ls':5,
                'lf':6,
                'wf': 7,
                'gf':8,
                'gf2':9
               }

    # EXTRACT DATA FROM TABLES
    ''' First get number of datapoints and number of player names '''
    smash_data = exinf.initial_counting( bracket_levels_map, level_limits, skip_these_players )

    numitems = smash_data['numitems']
    playernames = smash_data['playernames']
    charnames = smash_data['charnames']
    game_outcomes = smash_data['game_outcomes']
    tournaments = smash_data['tournaments']
    tourney_years = smash_data['tourney_years']

    numchars = len(charnames)
    numnames = len(playernames)

    smt.print_header( numnames, numitems, tournaments, tourney_years, skip_these_players, bracket_levels, level_limits )



    # Next retrieve character-based results

    smash_char_data = exinf.get_game_data(smash_data, bracket_levels_map, level_limits, skip_these_players )
    charnames = smash_char_data['charnames']
    charnums = smash_char_data['charnums']
    char_tots = smash_char_data['char_tots']
    CharGameMat = smash_char_data['CharGameMat']
    CharOutcomeMat = smash_char_data['CharOutcomeMat']
    GameMat = smash_char_data['GameMat']
    outcome_prct = smash_char_data['outcome_prct']
    num_matches = smash_char_data['num_matches']
    num_outcomes = smash_char_data['num_outcomes']
    char1 = smash_char_data['char1']
    char2 = smash_char_data['char2']
    char_wins = smash_char_data['char_wins']

    # NOW PRINT
    print("MATCHUP PERCENTAGES \n")
    print("char1\tchar2 \t# games \tchar1 wins \tprct win by char 1")
    inds = list(reversed(np.argsort(num_matches)))
    for i in inds:
        if num_matches[i] < 1:
            continue
        print( char1[i] + '\t' + char2[i] + '\t' + str(num_matches[ i ] ) + '\t\t' + str(num_outcomes[i]) + '\t\t' + ("%.2f" % outcome_prct[i]) )

    inds = list(reversed(np.argsort(charnums)))
    sorted_data = []
    for j in inds:
        sorted_data.append(char_tots[j])

    # This time without dittos
    charnames = []
    charnums = []
    charwins = char_wins
    for j in range(len(char_tots)):
        charnames.append(char_tots[j][0])
        charnums.append(char_tots[j][1] - CharGameMat[j,j])

    inds = list(reversed(np.argsort(charnums)))

    print("\nCHARACTER-BASED GAMES\n(excludes dittos)")
    print("char\t\t# games\t\t% wins")
    for i in inds:
        print( charnames[i] + '\t\t' + str(charnums[ i ] ) + '\t\t' + ("%.2f" % (charwins[i][0]/charnums[i]) ) )

    # Print just character appearances
    # (including dittos)
    charappearances = sum(CharGameMat)
    inds = list(reversed(np.argsort(charappearances)))
    print("\nTotal games " + str(sum(sum(CharGameMat))/2 ) + " (two characters appear per game)")
    print("char\t\t# appearances" + '\t' + "% of total")
    for i in inds:
        print( charnames[i] + '\t\t' + str(charappearances[ i ]) + '\t\t' + ("%.2f" % (charappearances[i]/(sum(sum(CharGameMat))) ) ) )



    # GET PLAYER DATA
    ''' Get player game totals, and char totals '''


    pldata = exinf.get_player_data(bracket_levels_map, level_limits, skip_these_players)
    playerchargames = pldata['playerchargames']
    playercharwins = pldata['playercharwins']

    file = open( 'smashdata.csv' )
    for line in file:
        line = line.strip()
        parts = line.split(',')

        comp_level = parts[8]
        if skip_this_game( comp_level, bracket_levels_map, level_limits, parts[2:4], skip_these_players) == True:
            continue

        gameplayernames = [ parts[2], parts[3] ]        
        gamecharnames = [ parts[4], parts[5] ]
        for j in [0,1]:
            current_playerchar = gameplayernames[j] + '-' + gamecharnames[j]
            playerchargames[ current_playerchar ] = playerchargames[ current_playerchar ] + 1
        whichwin = int(parts[6]) - 1
        winningplayer = gameplayernames[whichwin] + '-' + gamecharnames[whichwin]
        playercharwins[winningplayer] = playercharwins[winningplayer] + 1
    file.close()

    # Re-organize to sort by wins
    playchar2num = {}
    num2playchar = []
    num2wins = []
    numitems = 0
    for key, val in playerchargames.items():
        playchar2num[key] = numitems
        num2playchar.append(key)
        num2wins.append(val)
        numitems = numitems + 1

    inds = list(reversed(np.argsort(num2wins)))
    print("\nPlayer-character game data")
    print("\nplayer-character" + '\t\t' + "# games" + '\t\t' + "# wins" + '\t\t' + "% win")
    for j in range(len(playchar2num)):
        idx = inds[j]
        key = num2playchar[idx]
        val = int(playerchargames[key])
        valwins = int(playercharwins[key])
        print( key.ljust(20) + '\t\t' + str(val) + '\t\t' + str(valwins) + '\t\t' +  ("%.2f" % (valwins/val) ) )



    # INDIVIDUAL STATS
    
    print("\n\nINDIVIDUAL STATS")

    for PLAYER_NAME in individual_stats:

        print("\nplayer-character" + '\t\t' + "# games" + '\t\t' + "# wins" + '\t\t' + "% win")
        inds = list(reversed(np.argsort(num2wins)))
        total_games = 0
        total_wins = 0
        for j in range(len(playchar2num)):
            idx = inds[j]
            key = num2playchar[idx]
            ply_nm_len = len(PLAYER_NAME)
            if key[0:ply_nm_len] != PLAYER_NAME:
                continue
            val = int(playerchargames[key])
            valwins = int(playercharwins[key])
            total_games = total_games + val
            total_wins = total_wins + valwins
            print( key.ljust(20) + '\t\t' + str(val) + '\t\t' + str(valwins) + '\t\t' +  ("%.2f" % (valwins/val) ) )
        print( '\n' + "TOTALS".ljust(20) + '\t\t' + str(total_games) + '\t\t' + str(total_wins) + '\t\t' +  ("%.2f" % (total_wins/total_games) ) )