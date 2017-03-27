import numpy as np


class smashdb:
    
    # FILTER
    bracket_levels = [ 'pools', 'bracket', 'top64', 'top32',
                      'top16', 'top8', 'lf', 'wf', 'gf', 'gf2']
    bracket_levels_map = {
        'pools': 0,
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
    level_limits = [0,9]
    skip_these_players = {}
    
    # ARCHIVE
    games_archive = []
    playernames = {}
    charnames = {}
    tournaments_included = {}


    """
    Determines if a game falls outside the input search criteria
    """
    def skip_this_game( comp_level, players):
        if (self.bracket_levels_map[comp_level] < self.level_limits[0]) or
            (self.bracket_levels_map[comp_level] > self.level_limits[1]):
            return True
        play1, play2 = players
        if (play1 in self.skip_these_players.keys()) or
            (play2 in self.skip_these_players.keys()):
            return True



    def load_csv():
        file = open( 'smashdata.csv' )
        self.games_archive = []
        self.playernames = {}
        self.charnames = {}
        self.tournaments_included = {}

        for line in file:
            line = line.strip()
            parts = line.split(',')

            comp_level = parts[8]
            play1 = parts[2]
            play2 = parts[3]
            if skip_this_game( comp_level, parts[2:4], filter_object) == True:
                continue

            tourn_full = parts[1] + ' ' + parts[0]
            self.tournaments_included[ tourn_full ] = 1
            self.playernames[ play1 ] = 1
            self.playernames[ play2 ] = 1
            self.charnames[ parts[4] ] = 1
            self.charnames[ parts[5] ] = 1

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

            self.games_archive.append( single_match )

        file.close()

    def __init__(self):        
        self.load_csv()
        self.print_header()
        

    """
    PRINTNIG FUNCTIONS
    """
    def print_header():
        numitems = len( self.games_archive )
        numnames = len( self.playernames )

        print("\nSMASH ARCHIVE QUERY RESULTS")
        print("\nfrom recorded games at the following events:")
        for key in self.tournaments:
            print('\t\t' + key)
        if bool(self.skip_these_players):
            print("\nSkipping these players:")
            for key in self.skip_these_players:
                print('\t\t' + key)

        lim1,lim2 = self.level_limits
        print("Includes " + self.bracket_levels[lim1] + " games through " + self.bracket_levels[lim2])

        # print("Data taken from all recorded games.")
        print( 'Number of players in query: ' + str(numnames) )
        print( 'Number of games in query: ' + str(numitems) )
        print('\n')
