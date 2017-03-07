import numpy as np


"""
    Determines if a game falls outside the input search criteria
"""
def skip_this_game( comp_level, players, stat_object):
    level_limits = stat_object['limits']
    skip_these_players = stat_object['skips']
    bracket_levels_map = stat_object['bracket_map']
    
    if (bracket_levels_map[comp_level] < level_limits[0]) or (bracket_levels_map[comp_level] > level_limits[1]):
        return True
    play1, play2 = players
    if (play1 in skip_these_players.keys()) or (play2 in skip_these_players.keys()):
        return True

    
"""
    Loads all games that meet search criteria
"""
def db_load_csv( stat_object ):

    level_limits = stat_object['limits']
    skip_these_players = stat_object['skips']
    bracket_levels_map = stat_object['bracket_map']
            
    file = open( 'smashdata.csv' )
    games_archive = []
    playernames = {}
    charnames = {}
    tournaments_included = {}

    for line in file:
        line = line.strip()
        parts = line.split(',')

        comp_level = parts[8]
        play1 = parts[2]
        play2 = parts[3]
        if skip_this_game( comp_level, parts[2:4], stat_object) == True:
            continue

        tourn_full = parts[0] + ' ' + parts[1]
        tournaments_included[ tourn_full ] = 1
        playernames[ play1 ] = 1
        playernames[ play2 ] = 1
        charnames[ parts[4] ] = 1
        charnames[ parts[5] ] = 1
        
        single_game = {
            'tourney_name': tourn_full,
            'player1': play1,
            'player2': play2,
            'char1': parts[4],
            'char2': parts[5],
            'game_outcome': parts[6],
            'pools_bracket': parts[7],
            'bracket_level': comp_level,
            'which_game': parts[9],
            'best_of_X': parts[10]
            }
        
        games_archive.append( single_game )
    file.close()
    return {
            'games_archive':games_archive,
            'playernames':playernames,
            'charnames':charnames,
            'tournaments_included':tournaments_included
            }


"""
    From games archive, compile per-game stats
"""
def get_game_data(smash_data, stat_object ):

    level_limits = stat_object['limits']
    skip_these_players = stat_object['skips']
    bracket_levels_map = stat_object['bracket_map']
    
    games_archive = smash_data['games_archive'] 
    numitems = len(games_archive)
    playernames = smash_data['playernames']
    charnames = smash_data['charnames']
    tournaments = smash_data['tournaments_included']

    numchars = len(charnames)
    numnames = len(playernames)

    ''' Next construct hastables to map from name to number '''
    number2name = {}
    name2number = {}
    whichname = 0
    for item in playernames:
        name2number[ item ] = whichname
        number2name[ whichname ] = item
        whichname = whichname + 1

    ''' Now construct hashtables for characters '''
    number2char = {}
    char2number = {}
    whichchar = 0
    for item in charnames:
        char2number[ item ] = whichchar
        number2char[ whichchar ] = item
        whichchar = whichchar + 1

        
    ''' Construct maps for player-character info '''
    num2pchar = []
    pchar2num = {}
    which_entry = 0
    for game in games_archive:
        '''
            'game_outcome': parts[6],
            'best_of_X': parts[10]
            }
        '''
        gameplayernames = [ game['player1'], game['player2'] ]
        gamecharnames = [ game['char1'], game['char2'] ]
        for j in [0,1]:
            current_playerchar = gameplayernames[j] + '-' + gamecharnames[j]
            if current_playerchar in pchar2num.keys():
                continue
            else:
                pchar2num[current_playerchar] = which_entry
                num2pchar.append(current_playerchar)
                which_entry = which_entry + 1
    numpchars = len(num2pchar)
    

    ''' Construct adjacency matrices for game stats ??? '''
    # GameMat gives number of games played between players.
    # CharGameMat[x,y] gives number of games played between characters x and y
    # CharOutcomeMat[x,y] gives number of wins of char y over char x
    pchargamemat = np.zeros((numpchars, numpchars))
    pcharoutcomemat = np.zeros((numpchars, numpchars))
    GameMat = np.zeros((numnames, numnames))
    GameOutcomeMat = np.zeros((numnames, numnames))
    CharGameMat = np.zeros((numchars, numchars))
    CharOutcomeMat = np.zeros((numchars, numchars))

    char_wins = np.zeros((numchars,1))
    for game in games_archive:
        
        game_num = game['which_game']
        best_of = game['best_of_X']
            
        play1 = game['player1']
        play2 = game['player2']
        char1 = game['char1']
        char2 = game['char2']
        pchar1 = play1 + '-' + char1
        pchar2 = play2 + '-' + char2
        
        xjpchar = pchar2num[pchar1]
        yjpchar = pchar2num[pchar2]
        xj = name2number[ play1 ]
        yj = name2number[ play2 ]
        
        pchargamemat[ xjpchar, yjpchar ] = pchargamemat[ xjpchar, yjpchar ] + 1
        pchargamemat[ yjpchar, xjpchar ] = pchargamemat[ yjpchar, xjpchar ] + 1
        GameMat[ xj, yj ] = GameMat[ xj, yj ] + 1
        GameMat[ yj, xj ] = GameMat[ yj, xj ] + 1
        xchar = char2number[ char1 ]
        ychar = char2number[ char2 ]
        winchar = xchar
        losechar = ychar
        winpl = xj
        losepl = yj
        if int( game['game_outcome'] ) == 2:
            winchar = ychar
            losechar = xchar
            winpl = yj
            losepl = xj
            winpchar = yjpchar
            losepchar = xjpchar
        pcharoutcomemat[ winpchar, losepchar ] = pcharoutcomemat[ winpchar, losepchar ] + 1
        GameOutcomeMat[ winpl, losepl ] = GameOutcomeMat[ winpl, losepl ] + 1
        CharOutcomeMat[ losechar, winchar ] = CharOutcomeMat[ losechar, winchar ] + 1
        if winchar != losechar:
            char_wins[ winchar, 0 ] = char_wins[ winchar, 0 ] + 1

        CharGameMat[ xchar, ychar ] = CharGameMat[ xchar, ychar ] + 1
        CharGameMat[ ychar, xchar ] = CharGameMat[ ychar, xchar ] + 1

    '''
    These data structures contain actual tournament game/match data:
        GameMat
        CharGameMat
        pchargamemat
        pcharoutcomemat

    These contain maps from data structures indices to player/character names:
        char2number
        number2char
        name2number
        number2name

    '''
    char1 = []
    char2 = []
    char_tots = []
    outcome_prct = []
    num_matches = []
    num_outcomes = []
    for i in range( len(char2number) ) :
        for j in range( i, len(char2number) ) :
            char1.append(number2char[i])
            char2.append(number2char[j])
            num_matches.append(CharGameMat[ i,j ])
            num_outcomes.append(CharOutcomeMat[ j,i ])
            if CharGameMat[i,j] != 0:
                outcome_prct.append(CharOutcomeMat[j,i]/CharGameMat[ i,j ])
            if CharGameMat[i,j] == 0:
                outcome_prct.append(-5)

    for i in range(len(char2number)):
        char_tots.append( [number2char[i],0] )
        for j in range( len(char2number) ):
            char_tots[i][1] = char_tots[i][1] + CharGameMat[ i,j ]

    charnames = []
    charnums = []
    for j in range(len(char_tots)):
        charnames.append(char_tots[j][0])
        charnums.append(char_tots[j][1])

    return {
        'pname2num':name2number,
        'num2pname':number2name,
        'pchar2num':pchar2num,
        'num2pchar':num2pchar,
        'charnames':charnames,
        'charnums':charnums,
        'char_tots':char_tots,
        'CharGameMat':CharGameMat,
        'CharOutcomeMat':CharOutcomeMat,
        'GameMat':GameMat,
        'GameOutcomeMat':GameOutcomeMat,
        'pchargamemat':pchargamemat,
        'pcharoutcomemat':pcharoutcomemat,
        'outcome_prct':outcome_prct,
        'num_matches':num_matches,
        'num_outcomes':num_outcomes,
        'char1':char1,
        'char2':char2,
        'char_wins':char_wins
        }

def get_player_data( smash_data, stat_object):
    level_limits = stat_object['limits']
    skip_these_players = stat_object['skips']
    bracket_levels_map = stat_object['bracket_map']
    
    playerchargames = {}
    playercharwins = {}
    
    for game in smash_data['games_archive']:
        
        comp_level = game['bracket_level']
        play1 = game['player1']
        play2 = game['player2']
        char1 = game['char1']
        char2 = game['char2']
        
        if skip_this_game( comp_level, (play1, play2) , stat_object) == True:
            continue
            
        gameplayernames = [ play1, play2 ]
        gamecharnames = [ char1, char2 ]
        for j in [0,1]:
            current_playerchar = gameplayernames[j] + '-' + gamecharnames[j]
            playerchargames[ current_playerchar ] = 0
            playercharwins[ current_playerchar ] = 0

            
    return {
        'playerchargames':playerchargames,
        'playercharwins':playercharwins
        }