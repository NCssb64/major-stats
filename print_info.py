import numpy as np
import extract_info as exinf


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
    

def print_header( smash_data, stat_object ):

    tournaments = smash_data['tournaments_included']
    numitems = len( smash_data['games_archive'] )
    numnames = len(smash_data['playernames'])
    
    level_limits = stat_object['limits']
    skip_these_players = stat_object['skips']
    bracket_levels_map = stat_object['bracket_map']
    bracket_levels = stat_object['bracket_levels']

    print("\nSMASH ARCHIVE QUERY RESULTS")
    print("\nfrom recorded games at the following events:")
    for key in tournaments:
        print('\t\t' + key)
    if bool(skip_these_players):
        print("\nSkipping these players:")
        for key in skip_these_players:
            print('\t\t' + key)
        
    lim1,lim2 = level_limits
    print("Includes " + bracket_levels[lim1] + " games through " + bracket_levels[lim2])
    
    # print("Data taken from all recorded games.")
    print( 'Number of players in query: ' + str(numnames) )
    print( 'Number of games in query: ' + str(numitems) )
    print('\n')


    
    
"""
    Print player-char rankings
    
    print_plchar_ranks(level_limits, skip_these_players, individual_stats, which_rankings=='pchar')
    
        set 'which_rankings' to 'pchar' to see rankings on player-characters; any other value will instead print rankings for players
"""
def print_plchar_ranks(level_limits, skip_these_players, individual_stats, which_rankings='pchar'):
    # EXTRACT DATA FROM TABLES
    stat_object = {
    'limits':  level_limits,
    'skips': skip_these_players,
    'individuals': individual_stats,
    'bracket_levels': bracket_levels,
    'bracket_map': bracket_levels_map
    }
    smash_data = exinf.db_load_csv( stat_object )
    smash_char_data = exinf.get_game_data( smash_data, stat_object )
    
    if which_rankings == 'pchar':
        gamemat = smash_char_data['pchargamemat']
        outcomemat = smash_char_data['pcharoutcomemat']
        pname2num = smash_char_data['pchar2num']
        num2pname = smash_char_data['num2pchar']
    else:
        gamemat = smash_char_data['GameMat']
        outcomemat = smash_char_data['GameOutcomeMat']
        pname2num = smash_char_data['pname2num']
        num2pname = smash_char_data['num2pname']

    """ Begin PageRank computation """
    # Options
    normalize = True
    handle_dangling = False
    alpha = 0.99
    
    pmat = np.zeros( gamemat.shape )
    rows,cols = pmat.shape
    for row in range(rows):
        for col in range(cols):
            if gamemat[row,col] != 0:
                entry_val = outcomemat[row,col]/gamemat[row,col]
                pmat[row,col] = entry_val
    empty_cols = []

    for col in range(cols):
        weight = sum(pmat[:,col])
        if weight == 0:
            empty_cols.append(col)
            continue
        if normalize==True:
            for row in range(rows):
                pmat[row,col] = pmat[row,col]/weight
        else:
            alpha = 1/max( 1/alpha, weight )

    # handle dangling nodes -- players with no recorded losses
    filled_pmat = pmat
    if handle_dangling==True:
        for col in empty_cols:
            for row in range(rows):
                filled_pmat[row,col] = 1/cols
    
    sysmat = np.eye(cols) - alpha*filled_pmat
    righthandvec = ((1-alpha)/cols) *np.ones((rows,1))

    rankings_vec = np.linalg.solve(sysmat, righthandvec)

    """ PageRank computed; now sort and print """
    ranks = rankings_vec[:,0]
    idx = np.flipud(np.argsort( ranks ))

    print("Rank", '\t', "Name".ljust(30), "Rating" )
    for j in range( min(50, len(ranks)) ):
        print( str(j+1), '\t',  num2pname[idx[j]].ljust(30), ranks[idx[j]] )



"""
    Convert game data into player rankings
"""
def print_player_rankings(level_limits, skip_these_players, individual_stats):
    # EXTRACT DATA FROM TABLES
    stat_object = {
    'limits':  level_limits,
    'skips': skip_these_players,
    'individuals': individual_stats,
    'bracket_levels': bracket_levels,
    'bracket_map': bracket_levels_map
    }
        
    smash_data = exinf.db_load_csv( stat_object )
    
    playernames = smash_data['playernames']
    charnames = smash_data['charnames']
    tournaments = smash_data['tournaments_included']

    numitems = len( smash_data['games_archive'] )
    numchars = len(charnames)
    numnames = len(playernames)

    print_header( smash_data, stat_object )


    # Next retrieve character-based results

    smash_char_data = exinf.get_game_data( smash_data, stat_object )

    return {
        'all_data':smash_char_data,
        'pname2num':smash_char_data['pname2num'],
        'num2pname':smash_char_data['num2pname'],
        'gamemat':smash_char_data['GameMat'],
        'outcomemat':smash_char_data['GameOutcomeMat']
    }
    
    
    
"""
    PRINT char based stats, player-char based stats
"""
def print_smash_stats( level_limits, skip_these_players, individual_stats ):
    
    stat_object = {
        'limits':  level_limits,
        'skips': skip_these_players,
        'individuals': individual_stats,
        'bracket_levels': bracket_levels,
        'bracket_map': bracket_levels_map
        }
    
    # EXTRACT DATA FROM TABLES
    ''' First get number of datapoints and number of player names '''

    smash_data = exinf.db_load_csv( stat_object )
    
    playernames = smash_data['playernames']
    charnames = smash_data['charnames']
    tournaments = smash_data['tournaments_included']

    numitems = len( smash_data['games_archive'] )
    numchars = len(charnames)
    numnames = len(playernames)

    print_header( smash_data, stat_object )


    # Next retrieve character-based results

    smash_char_data = exinf.get_game_data( smash_data, stat_object )
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

    pldata = exinf.get_player_data(smash_data, stat_object)
    playerchargames = pldata['playerchargames']
    playercharwins = pldata['playercharwins']

    for game in smash_data['games_archive']:
        
        play1 = game['player1']
        play2 = game['player2']
        char1 = game['char1']
        char2 = game['char2']
        
        gameplayernames = [ play1, play2 ]        
        gamecharnames = [ char1, char2 ]
        for j in [0,1]:
            current_playerchar = gameplayernames[j] + '-' + gamecharnames[j]
            playerchargames[ current_playerchar ] = playerchargames[ current_playerchar ] + 1
        whichwin = int(game['game_outcome']) - 1
        winningplayer = gameplayernames[whichwin] + '-' + gamecharnames[whichwin]
        playercharwins[winningplayer] = playercharwins[winningplayer] + 1

    # Re-organize to sort alphabetically
    playchar2num = {}
    num2playchar = []
    num2wins = []
    numitems = 0
    for key, val in playerchargames.items():
        playchar2num[key] = numitems
        num2playchar.append(key)
        num2wins.append(val)
        numitems = numitems + 1

    inds = list(np.argsort(num2playchar))
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
            if (val == 0):
                print("No games for " + PLAYER_NAME)
            else:
                print( key.ljust(25) + '\t\t' + str(val) + '\t\t' + str(valwins) + '\t\t' +  ("%.2f" % (valwins/val) ) )
        if (total_games == 0):
            print("No games for " + PLAYER_NAME)
        else:
            print( '\n' + "TOTALS".ljust(25) + '\t\t' + str(total_games) + '\t\t' + str(total_wins) + '\t\t' +  ("%.2f" % (total_wins/total_games) ) )
