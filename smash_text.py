def print_header( numnames, numitems, tournaments, tourney_years, skip_pools = False ):
    print("\nSmash 64 results from recorded games at the following tournaments:")
    for key in tournaments:
        print('\t\t' + key)
    print("\nDuring these years:")
    for key in tourney_years:
        print('\t\t' + key)
    
    if skip_pools == 1:
        print("Includes bracket games only")
    if skip_pools != 1:
        print("Includes bracket and pools")
    # print("Data taken from all recorded games.")
    print( 'Number of players in data: ' + str(numnames) )
    print( 'Number of games in data: ' + str(numitems) )