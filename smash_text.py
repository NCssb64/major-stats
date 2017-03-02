def print_header( numnames, numitems, tournaments, tourney_years, skip_these_players, bracket_levels, level_limits = [1,1] ):
    print("\nSMASH ARCHIVE QUERY RESULTS")
    print("\nfrom recorded games at the following events:")
    for key in tourney_years:
        print('\t\t' + key)
    print("\nSkipping these players:")
    for key in skip_these_players:
        print('\t\t' + key)
        
    lim1,lim2 = level_limits
    print("Includes " + bracket_levels[lim1] + " games through " + bracket_levels[lim2])
    
    # print("Data taken from all recorded games.")
    print( 'Number of players in query: ' + str(numnames) )
    print( 'Number of games in query: ' + str(numitems) )
    print('\n')