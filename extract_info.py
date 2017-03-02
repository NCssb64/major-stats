import numpy as np

def initial_counting( bracket_levels_map, level_chosen, skip_these_players ):
    file = open( 'smashdata.csv' )
    numitems = 0
    playernames = {}
    charnames = {}
    game_outcomes = []
    tournaments = {}
    tourney_years = {}
    for line in file:
        line = line.strip()
        parts = line.split(',')
        comp_level = parts[8]
        if (bracket_levels_map[comp_level] < level_chosen[0]) or (bracket_levels_map[comp_level] > level_chosen[1]):
            continue
        play1, play2 = parts[2:4]
        if (play1 in skip_these_players.keys()) or (play2 in skip_these_players.keys()):
            continue
        
        tournament_year = parts[0]
        tournament_title = parts[1]
        tourn_full = tournament_title + '\t\t' + tournament_year
        tourney_years[ tourn_full ] = 1
        tournaments[ tournament_title ] = 1
        numitems = numitems + 1
        playernames[ play1 ] = 1
        playernames[ play2 ] = 1
        charnames[ parts[4] ] = 1
        charnames[ parts[5] ] = 1
        game_outcomes.append(parts[6])

    file.close()
    return {
            'numitems':numitems,
            'playernames':playernames,
            'charnames':charnames,
            'game_outcomes':game_outcomes,
            'tournaments':tournaments,
            'tourney_years':tourney_years
            }



def get_game_data(smash_data, bracket_levels_map, level_chosen, skip_these_players ):

    numitems = smash_data['numitems']
    playernames = smash_data['playernames']
    charnames = smash_data['charnames']
    game_outcomes = smash_data['game_outcomes']
    tournaments = smash_data['tournaments']
    tourney_years = smash_data['tourney_years']

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

    ''' Construct adjacency matrices for game stats ??? '''
    # GameMat gives number of games played between players.
    # CharGameMat[x,y] gives number of games played between characters x and y
    # CharOutcomeMat[x,y] gives number of wins of char y over char x
    GameMat = np.zeros((numnames, numnames))
    CharGameMat = np.zeros((numchars, numchars))
    CharOutcomeMat = np.zeros((numchars, numchars))

    file = open( 'smashdata.csv' )
    line_number = 0

    char_wins = np.zeros((numchars,1))
    for line in file:
        line = line.strip()
        parts = line.split(',')
        
        comp_level = parts[8]
        if (bracket_levels_map[comp_level] < level_chosen[0]) or (bracket_levels_map[comp_level] > level_chosen[1]):
            continue
        play1, play2 = parts[2:4]
        if (play1 in skip_these_players.keys()) or (play2 in skip_these_players.keys()):
            continue
            
        xj = name2number[ parts[2] ]
        yj = name2number[ parts[3] ]
        GameMat[ xj, yj ] = GameMat[ xj, yj ] + 1
        GameMat[ yj, xj ] = GameMat[ yj, xj ] + 1
        xchar = char2number[ parts[4] ]
        ychar = char2number[ parts[5] ]
        winchar = xchar
        losechar = ychar
        if int(parts[6]) == 2:
            winchar = ychar
            losechar = xchar
        #if int(parts[6]) == 1:
        CharOutcomeMat[ losechar, winchar ] = CharOutcomeMat[ losechar, winchar ] + 1
        if winchar != losechar:
            char_wins[ winchar, 0 ] = char_wins[ winchar, 0 ] + 1

        CharGameMat[ xchar, ychar ] = CharGameMat[ xchar, ychar ] + 1
        CharGameMat[ ychar, xchar ] = CharGameMat[ ychar, xchar ] + 1
        line_number = line_number + 1

    '''
    These data structures contain actual tournament game/match data:
        GameMat
        CharGameMat

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

    char_tots
    charnames = []
    charnums = []
    for j in range(len(char_tots)):
        charnames.append(char_tots[j][0])
        charnums.append(char_tots[j][1])

    file.close()
    return {
        'charnames':charnames,
        'charnums':charnums,
        'char_tots':char_tots,
        'CharGameMat':CharGameMat,
        'CharOutcomeMat':CharOutcomeMat,
        'GameMat':GameMat,
        'outcome_prct':outcome_prct,
        'num_matches':num_matches,
        'num_outcomes':num_outcomes,
        'char1':char1,
        'char2':char2,
        'char_wins':char_wins
        }

def get_player_data(bracket_levels_map, level_limits, skip_these_players):
    file = open( 'smashdata.csv' )
    numitems = 0
    playerchargames = {}
    playercharwins = {}
    for line in file:
        line = line.strip()
        parts = line.split(',')
        
        comp_level = parts[8]
        if (bracket_levels_map[comp_level] < level_limits[0]) or (bracket_levels_map[comp_level] > level_limits[1]):
            continue
        play1, play2 = parts[2:4]
        if (play1 in skip_these_players.keys()) or (play2 in skip_these_players.keys()):
            continue
            
        gameplayernames = [ parts[2], parts[3] ]
        gamecharnames = [ parts[4], parts[5] ]
        for j in [0,1]:
            current_playerchar = gameplayernames[j] + '-' + gamecharnames[j]
            playerchargames[ current_playerchar ] = 0
            playercharwins[ current_playerchar ] = 0
    file.close()
    return {
        'playerchargames':playerchargames,
        'playercharwins':playercharwins
        }