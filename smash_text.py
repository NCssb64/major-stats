def print_header( numnames, numitems, tournaments, tourney_years, skip_these_players, bracket_levels, level_limits = [1,1] ):
    print("\nSmash 64 results from recorded games at the following tournaments:")
    for key in tournaments:
        print('\t\t' + key)
    print("\nDuring these years:")
    for key in tourney_years:
        print('\t\t' + key)
    print("\nSkipping these players:")
    for key in skip_these_players:
        print('\t\t' + key)
        
    lim1,lim2 = level_limits
    print("Includes " + bracket_levels[lim1] + " games through " + bracket_levels[lim2])
    
    # print("Data taken from all recorded games.")
    print( 'Number of players in data: ' + str(numnames) )
    print( 'Number of games in data: ' + str(numitems) )