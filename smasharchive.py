import numpy as np


class smashdb:
    def __init__(self):
        print('initiatlizing smashdb')
        # FILTER
        self.bracket_levels = [ 'pools', 'bracket', 'top64', 'top32',
                          'top16', 'top8', 'lf', 'wf', 'gf', 'gf2']
        self.bracket_levels_map = {
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
        self.level_limits = [0,9]
        self.skip_these_players = {}

        # ARCHIVE
        self.games_archive = []
        self.playernames = {}
        self.charnames = {}
        self.tournaments_included = {}

        self.numgames = len( self.games_archive )
        self.numchars = len( self.charnames )
        self.numnames = len( self.playernames )
        
        self.load_csv()
        self.print_header()

        self.get_game_data()


    """
    Determines if a game falls outside the input search criteria
    """
    def skip_this_game( self, comp_level, players):
        if (self.bracket_levels_map[comp_level] < self.level_limits[0]) or (self.bracket_levels_map[comp_level] > self.level_limits[1]):
            return True
        play1, play2 = players
        if (play1 in self.skip_these_players.keys()) or (play2 in self.skip_these_players.keys()):
            return True



    def load_csv(self):
        print('testing')
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
            if self.skip_this_game( comp_level, parts[2:4] ) == True:
                continue

            tourn_full = parts[0] + ' ' + parts[1]
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

            self.games_archive.append( single_game )

        self.numgames = len( self.games_archive )
        self.numchars = len( self.charnames )
        self.numnames = len( self.playernames )

        file.close()


    """
    PRINTING FUNCTIONS
    """
    def print_header(self):

        print("\nSMASH ARCHIVE QUERY RESULTS")
        print("\nfrom recorded games at the following events:")
        for key in self.tournaments_included:
            print('\t\t' + key)
        if bool(self.skip_these_players):
            print("\nSkipping these players:")
            for key in self.skip_these_players:
                print('\t\t' + key)

        lim1,lim2 = self.level_limits
        print("Includes " + self.bracket_levels[lim1] + " games through " + self.bracket_levels[lim2])

        # print("Data taken from all recorded games.")
        print( 'Number of players in query: ' + str(self.numnames) )
        print( 'Number of games in query: ' + str(self.numgames) )
        print( '\n' )


    """
    Compile per-game stats
    """
    def get_game_data(self):

        self.num2pchar = []
        self.pchar2num = {}
                
        # PREPPING PER-GAME STATS
        self.number2name = {}
        self.name2number = {}
        self.number2char = {}
        self.char2number = {}

        self.mu_charnames = []
        self.mu_charnums = []
        
        self.muchar1 = []
        self.muchar2 = []
        self.muchar_tots = []
        self.mu_outcome_prct = []
        self.num_mu_matches = []
        self.num_mu_outcomes = []
        
        ''' Next construct hastables to map from name to number '''
        whichname = 0
        for item in self.playernames:
            self.name2number[ item ] = whichname
            self.number2name[ whichname ] = item
            whichname = whichname + 1

        ''' Now construct hashtables for characters '''
        self.num2pchar = []
        self.pchar2num = {}
        whichchar = 0
        for item in self.charnames:
            self.char2number[ item ] = whichchar
            self.number2char[ whichchar ] = item
            whichchar = whichchar + 1


        ''' Construct maps for player-character info '''
        which_entry = 0
        for game in self.games_archive:
            gameplayernames = [ game['player1'], game['player2'] ]
            gamecharnames = [ game['char1'], game['char2'] ]
            for j in [0,1]:
                current_playerchar = gameplayernames[j] + '-' + gamecharnames[j]
                if current_playerchar in self.pchar2num.keys():
                    continue
                else:
                    self.pchar2num[current_playerchar] = which_entry
                    self.num2pchar.append(current_playerchar)
                    which_entry = which_entry + 1
        numpchars = len(self.num2pchar)


        ''' Construct adjacency matrices for game stats ??? '''
        self.pchargamemat = np.zeros((numpchars, numpchars))
        self.pcharoutcomemat = np.zeros((numpchars, numpchars))
        self.GameMat = np.zeros((self.numnames, self.numnames))
        self.GameOutcomeMat = np.zeros((self.numnames, self.numnames))
        self.CharGameMat = np.zeros((self.numchars, self.numchars))
        self.CharOutcomeMat = np.zeros((self.numchars, self.numchars))

        self.char_wins = np.zeros((self.numchars,1))
        for game in self.games_archive:

            game_num = game['which_game']
            best_of = game['best_of_X']

            play1 = game['player1']
            play2 = game['player2']
            char1 = game['char1']
            char2 = game['char2']
            pchar1 = play1 + '-' + char1
            pchar2 = play2 + '-' + char2

            xjpchar = self.pchar2num[pchar1]
            yjpchar = self.pchar2num[pchar2]
            xj = self.name2number[ play1 ]
            yj = self.name2number[ play2 ]

            self.pchargamemat[ xjpchar, yjpchar ] += 1
            self.pchargamemat[ yjpchar, xjpchar ] += 1
            self.GameMat[ xj, yj ] += 1
            self.GameMat[ yj, xj ] += 1
            xchar = self.char2number[ char1 ]
            ychar = self.char2number[ char2 ]
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
            self.pcharoutcomemat[ winpchar, losepchar ] += 1
            self.GameOutcomeMat[ winpl, losepl ] += 1
            self.CharOutcomeMat[ losechar, winchar ] += 1
            if winchar != losechar:
                self.char_wins[ winchar, 0 ] += 1

            self.CharGameMat[ xchar, ychar ] += 1
            self.CharGameMat[ ychar, xchar ] += 1

        for i in range( len(self.char2number) ) :
            for j in range( i, len(self.char2number) ) :
                self.muchar1.append(self.number2char[i])
                self.muchar2.append(self.number2char[j])
                self.num_mu_matches.append(self.CharGameMat[ i,j ])
                self.num_mu_outcomes.append(self.CharOutcomeMat[ j,i ])
                if self.CharGameMat[i,j] != 0:
                    self.mu_outcome_prct.append(self.CharOutcomeMat[j,i]/self.CharGameMat[ i,j ])
                if self.CharGameMat[i,j] == 0:
                    self.mu_outcome_prct.append(-5)

        for i in range(len(self.char2number)):
            self.muchar_tots.append( [self.number2char[i],0] )
            for j in range( len(self.char2number) ):
                self.muchar_tots[i][1] += self.CharGameMat[ i,j ]

        for j in range(len(self.muchar_tots)):
            self.mu_charnames.append(self.muchar_tots[j][0])
            self.mu_charnums.append(self.muchar_tots[j][1])



    def print_mu_stats( self, game_threshold=20, markdown_flag=False ):

        # NOW PRINT
        print("MATCHUP PERCENTAGES \n")
        if markdown_flag == True:
            print(" | char1 | char2 | # games | % win char1 | ")
            print(" |:---|:---|---:|---:| ")
        else:
            print("char1 \tchar2 \t# games \tchar1 wins \tprct win by char 1")
        inds = list(reversed(np.argsort(self.num_mu_matches)))
        for i in inds:
            if self.num_mu_matches[i] < game_threshold:
                continue
            if markdown_flag == True:
                print( '|' + self.muchar1[i] + '|' + self.muchar2[i] + '|' + str(self.num_mu_matches[ i ] ) + '|' + ("%.2f" % self.mu_outcome_prct[i]) + '|' )
            else:
                print( self.muchar1[i] + '\t' + self.muchar2[i] + '\t' + str(self.num_mu_matches[ i ] ) + '\t\t' + str(self.num_mu_outcomes[i]) + '\t\t' + ("%.2f" % self.mu_outcome_prct[i]) )
