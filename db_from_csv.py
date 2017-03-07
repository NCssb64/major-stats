def load_csv( stat_object ):

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

        tourn_full = parts[1] + ' ' + parts[0]
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
        
        games_archive.append( single_match )
    file.close()
    return {
            'games_archive':games_archive,
            'playernames':playernames,
            'charnames':charnames,
            'tournaments_included':tournaments
            }