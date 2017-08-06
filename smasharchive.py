import numpy as np


class smashdb:
    def __init__(self):
        print('initiatlizing smashdb')

        # FILTERING OPTIONS
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

        self.tournament_year_skip = {}
        self.tournament_name_skip = {}

        self.ranking_threshold = 10
        self.ranking_filter = False

        self.character_set = set()

        # ARCHIVE

        self.load_csv()
        self.get_game_data()


    """
    Determines if a game falls outside the input search criteria
    """
    def skip_this_game( self, comp_level, players, tournament_year, tournament_name, outcome, chars ):
        if (self.bracket_levels_map[comp_level] < self.level_limits[0]):
            return True
        if (self.bracket_levels_map[comp_level] > self.level_limits[1]):
            return True
        play1, play2 = players
        if (play1 in self.skip_these_players.keys()):
            return True
        if (play2 in self.skip_these_players.keys()):
            return True
        if tournament_year in self.tournament_year_skip.keys():
            return True
        if tournament_name in self.tournament_name_skip.keys():
            return True

        if self.ranking_filter:
            if players[0] in self.player_rankings and players[1] in self.player_rankings:
                wini = (int(outcome) + 1) % 2
                losei = (wini + 1) % 2
                winningplayer = players[wini]
                losingplayer = players[losei]
                winningplayerrank = float(self.player_rankings[winningplayer])
                losingplayerrank = float(self.player_rankings[losingplayer])
                if winningplayerrank < losingplayerrank + self.ranking_threshold:
                    """
                    print("{} beats {}; {} vs {} gap = {} ".format(winningplayer, losingplayer,
                                                                   chars[wini], chars[losei],
                                                                   winningplayerrank - losingplayerrank))
                    """
                    return False
                else:
                    return True
        return False


    def load_csv(self):
        file = open( 'smashdata-tournaments.csv' )
        self.tournament_archive = {}
        for line in file:
            line = line.strip()
            parts = line.split(',')
            tourn_full = parts[0] + ' ' + parts[1]
            self.tournament_archive[tourn_full] = {
                'year': parts[0],
                'name': parts[1],
                'attendance': parts[2],
                'version': parts[3],
                'region': parts[4],
                'games': 0
            }
        file.close()

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
            tournament_year = parts[0]
            tournament_name = parts[1]
            if self.skip_this_game( comp_level, parts[2:4], tournament_year, tournament_name, parts[6], parts[4:6] ) == True:
                continue

            tourn_full = tournament_year + ' ' + tournament_name
            self.tournaments_included[ tourn_full ] = 1
            self.playernames[ play1 ] = 1
            self.playernames[ play2 ] = 1
            self.charnames[ parts[4] ] = 1
            self.charnames[ parts[5] ] = 1

            self.tournament_archive[tourn_full]['games'] += 1

            single_game = {
                'tourney_name': tournament_name,
                'tourney_year': tournament_year,
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

        file = open( 'ssbcentral-rankings.tsv' )
        self.player_rankings = {}
        self.player_names_map = {}
        for line in file:
            line = line.strip()
            parts = line.split()
            if len(parts) < 2:
                print(line)
                continue
            self.player_rankings[parts[0]] = parts[1]
            if len(parts) > 2:
                for new_name in parts[2::]:
                    self.player_names_map[parts[0]] = parts[0]
                    self.player_names_map[new_name] = parts[0]
                    self.player_rankings[new_name] = parts[1]
        file.close()


    """
    PRINTING FUNCTIONS
    """
    def print_header(self):
        namesp = 17
        playsp = 8
        datasp = 12
        regsp = 8
        versp = 9
        print('\nSMASH ARCHIVE QUERY RESULTS\n')
        print('| ' + '{: <{sp}}'.format('Name',sp=namesp) + '|' + '{: >{sp}}'.format('Players',sp=playsp) + ' |' + '{: >{sp}}'.format('data-points',sp=datasp) + ' |' + '{: >{sp}}'.format('Region',sp=regsp) + ' |' + '{: >{sp}}'.format('Version',sp=versp) + ' |')

        print('|:' + '{:->{sp}}'.format('',sp=namesp) + '|' + '{:->{sp}}'.format('',sp=playsp) + ':|' + '{:->{sp}}'.format('',sp=datasp) + ':|' + '{:->{sp}}'.format('',sp=regsp) + ':|' + '{:->{sp}}'.format('',sp=versp) + ':|')

        for key in self.tournaments_included:
            tourn_dict = self.tournament_archive[key]
            print('| ' + '{: <{sp}}'.format(key,sp=namesp) + '|' + '{: >{sp}}'.format(tourn_dict['attendance'],sp=playsp) + ' |' + '{: >{sp}}'.format(str(tourn_dict['games']),sp=datasp) + ' |' + '{: >{sp}}'.format(tourn_dict['region'],sp=regsp) + ' |' + '{: >{sp}}'.format(tourn_dict['version'],sp=versp) + ' |')


        """
        if bool(self.skip_these_players):
            print("\nSkipping these players:")
            for key in self.skip_these_players:
                    print(' * ' + key)
        """

        lim1,lim2 = self.level_limits
        print("\n* Includes " + self.bracket_levels[lim1] + " games through " + self.bracket_levels[lim2])

        print( '* Number of players in query: ' + str(self.numnames) )
        print( '* Number of games in query: ' + str(self.numgames) + '\n')




    """
    Compile per-game stats
    """
    def get_game_data(self):

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
            winpchar = xjpchar
            losepchar = yjpchar
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

    """
    Retrieve player-character stats
    """
    def get_playerchar_data(self):

        self.playerchargames = {}
        self.playercharwins = {}

        # Make sure they're all in the dictionary
        for game in self.games_archive:
            play1 = game['player1']
            play2 = game['player2']
            char1 = game['char1']
            char2 = game['char2']
            gameplayernames = [ play1, play2 ]
            gamecharnames = [ char1, char2 ]
            for j in [0,1]:
                current_playerchar = gameplayernames[j] + '-' + gamecharnames[j]
                self.playerchargames[ current_playerchar ] = 0
                self.playercharwins[ current_playerchar ] = 0

        # Now tally the games and wins
        for game in self.games_archive:
            play1 = game['player1']
            play2 = game['player2']
            char1 = game['char1']
            char2 = game['char2']
            gameplayernames = [ play1, play2 ]
            gamecharnames = [ char1, char2 ]
            for j in [0,1]:
                current_playerchar = gameplayernames[j] + '-' + gamecharnames[j]
                self.playerchargames[ current_playerchar ] += 1

            whichwin = int(game['game_outcome']) - 1
            winningplayer = gameplayernames[whichwin] + '-' + gamecharnames[whichwin]
            self.playercharwins[winningplayer] += 1



    """
    Print stats for all player-chars
    """
    def print_playerchar(self):
        self.get_playerchar_data()
        # Re-organize to sort alphabetically
        playchar2num = {}
        num2playchar = []
        num2wins = []
        numitems = 0
        for key, val in self.playerchargames.items():
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
            val = int(self.playerchargames[key])
            valwins = int(self.playercharwins[key])
            print( key.ljust(20) + '\t\t' + str(val) + '\t\t' + str(valwins) + '\t\t' +  ("%.2f" % (valwins/val) ) )


    """
    Re-compile the smash archive
    """
    def refilter_archive(self):
        self.load_csv()
        self.get_game_data()


    """
    Re-compile the smash archive
    """
    def refilter_archive_for_ssbcentral(self, threshold=10):
        self.ranking_threshold = threshold
        self.ranking_filter = True
        self.load_csv()
        for player_name in self.playernames.keys():
            self.skip_these_players[player_name] = 1
        for player_name in self.player_rankings:
            self.skip_these_players.pop(player_name, None)
        self.load_csv()
        self.get_game_data()



    """
        PRINT MATCH UP STATS
    """
    def print_mu_stats( self, game_threshold=20):
        charspace = 12
        gamenumspace = 8
        percspace = 12

        print("MATCHUP PERCENTAGES \n")
        print("| {: <{sp}}| {: <{sp}}| {: <{spg}}| {: >{spp}}|".format('char1', 'char2', '# games', '% win char1',
                                                                    sp=charspace, spg=gamenumspace, spp=percspace) )
        print("|:{:->{sp}}|:{:->{sp}}|{:->{spg}}:|{:->{spp}}:|".format('', '', '', '', sp=charspace, spg=gamenumspace,
                                                                       spp=percspace))
        inds = list(reversed(np.argsort(self.num_mu_matches)))
        for i in inds:
            if self.num_mu_matches[i] < game_threshold:
                continue

            winningchar = self.muchar1[i]
            losingchar = self.muchar2[i]
            prct = self.mu_outcome_prct[i]
            if winningchar == losingchar:
                continue
            if prct < 0.5:
                prct = 1-prct
                winningchar = losingchar
                losingchar = self.muchar1[i]
            print( '| ' + '{: <{sp}}'.format(winningchar,sp=charspace)
                  + '| ' + '{: <{sp}}'.format(losingchar,sp=charspace)
                  + '| ' + '{: <{sp}}'.format(str(self.num_mu_matches[ i ] ), sp=gamenumspace)
                  + '| ' + '{: >{sp}.2f}'.format(prct, sp=percspace) + '|' )
                  #+ '| ' + ("%.2f" % self.mu_outcome_prct[i]) + '|' )



    """
        PRINT CHAR STATS
    """
    def print_chargames_stats( self ):
        # Print just character appearances
        # (including dittos)

        # Set spacing values for output
        charspacing = 12
        countspacing = 13
        prctspacing = 10

        tempcharnames = []
        charappearances = []
        for j in range(len(self.muchar_tots)):
            tempcharnames.append( self.muchar_tots[j][0] )
            charappearances.append( self.muchar_tots[j][1] )

        inds = list(np.argsort(charappearances)[::-1])

        print("\n* Total games " + str(sum(sum(self.CharGameMat))/2 ) + " (two characters appear per game)")
        print( '* Number of players in query: ' + str(self.numnames) )
        print( '* Number of games in query: ' + str(self.numgames) + '\n')

        print('| ' + '{: ^{sp}}'.format('char',sp=charspacing) + ' | ' + '{: ^{sp}}'.format('# appearances',sp=countspacing) + ' | ' + '{: >{sp}}'.format('% of total',sp=prctspacing) + ' |')
        print('|:' + '{:-<{sp}}'.format('',sp=charspacing) + '-|-' + '{:->{sp}}'.format('',sp=countspacing) + ':|-' + '{:->{sp}}'.format('',sp=prctspacing) + ':|' )

        for idx in range(len(inds)):
            i = inds[idx]
            prctchr = "%.2f" % (int(charappearances[i])/(sum(sum(self.CharGameMat))) )
            print( '| ' + '{msg: <{sp}}'.format(msg=tempcharnames[i],sp=charspacing) + ' | ' + '{msg: >{sp}}'.format(msg=str(charappearances[i]),sp=countspacing) + ' | ' + '{msg: >{sp}}'.format(msg=prctchr,sp=prctspacing) + ' |')

    def print_char_mu(self, char_set):

        def get_rankings(winplayer, losplayer):
            winrank = -1.0
            losrank = -1.0
            if winplayer in self.player_rankings.keys():
                winrank = float(self.player_rankings[winplayer])
            if losplayer in self.player_rankings.keys():
                losrank = float(self.player_rankings[losplayer])
            return winrank, losrank

        if type(char_set) != set:
            print("Input char_set is of wrong type.")
        data_matrix = []
        print("{: <12} {: <5} {: <5} {: <18} {: <18} {: <8} {: <8} {: >4} {: >4}".format('Tournament',
                      'Year',
                      'Round',
                      'Winner', 'Loser',
                      'Winner', 'Loser',
                      'W-rating', 'L-rating'))

        for single_game in self.games_archive:
            chars = [single_game['char1'], single_game['char2']]
            if set([chars[0], chars[1]]) != char_set:
                continue

            wini = (int(single_game['game_outcome']) + 1) % 2
            losei = (wini + 1) % 2
            players = [single_game['player1'], single_game['player2']]
            winningplayer = players[wini]
            losingplayer = players[losei]
            winrank, losrank = get_rankings(winningplayer, losingplayer)
            winchar = chars[wini]
            losechar = chars[losei]
            # if winningplayerrank < losingplayerrank + self.ranking_threshold:
            line = [single_game['tourney_name'],
                      single_game['tourney_year'],
                      single_game['bracket_level'],
                      winningplayer, losingplayer,
                      winchar, losechar,
                      winrank, losrank]
            data_matrix.append(line)
            print("{: <12} {: <5} {: <5} {: <18} {: <18} {: <8} {: <8} {: 8.3f} {: 8.3f}".format(single_game['tourney_name'],
                      single_game['tourney_year'],
                      single_game['bracket_level'],
                      winningplayer, losingplayer,
                      winchar, losechar,
                      winrank, losrank))

        return data_matrix


    """
    Print player-char rankings
        set 'which_rankings' to 'pchar' to see rankings on player-characters;
        any other value will instead print rankings for players
    """
    def print_plchar_ranks(self, num_to_print=50, which_rankings='pchar', centered_player=None, degree_scale=False,
                          transpose_flag=True):
        # EXTRACT DATA FROM TABLES

        if which_rankings == 'pchar':
            gamemat = self.pchargamemat.copy()
            outcomemat = self.pcharoutcomemat.copy()
            pname2num = self.pchar2num.copy()
            num2pname = self.num2pchar.copy()
        else:
            gamemat = self.GameMat.copy()
            outcomemat = self.GameOutcomeMat.copy()
            pname2num = self.name2number.copy()
            num2pname = self.number2name.copy()

        """ Begin PageRank computation """
        # First extract from gamemat the connected network that contains NA
        rows,cols = gamemat.shape
        if num_to_print <= 0:
            num_to_print = rows
        M = gamemat
        if transpose_flag:
            M += gamemat.T
        degree_weights = []
        for col in range(cols):
            weight = sum(M[:,col])
            degree_weights.append(weight)
            if weight != 0:
                M[:,col] = M[:,col]/weight

        if which_rankings == 'pchar':
            index = pname2num['superboomfan-kirby']
        else:
            index = pname2num['superboomfan']
        dummyvec = np.zeros( (rows,1) )
        dummyvec[index] = 1
        temp_mat = np.eye(cols) - 0.5*M
        connected_vec = np.linalg.solve(temp_mat, dummyvec)
        for row in range(len(connected_vec)):
            val = connected_vec[row]
            if val==0:
                gamemat[:,row] = np.squeeze(np.zeros((rows,1)))
                gamemat[row,:] = np.squeeze(np.zeros((1,rows)))
        # this simply removes players with too few games in NA tournaments

        # Options
        normalize = True
        handle_dangling = False
        alpha = 0.99

        pmat = np.zeros( gamemat.shape )
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
        righthandvec = ((1-alpha)/cols) * np.ones((rows,1))
        if bool(centered_player):
            if centered_player in pname2num.keys():
                index = pname2num[centered_player]
                righthandvec = np.zeros( (rows,1) )
                righthandvec[index] = ((1-alpha)/cols)


        rankings_vec = np.linalg.solve(sysmat, righthandvec)

        # Scale by degree?
        if degree_scale == True:
            for j in range(len(rankings_vec)):
                deg_weight = degree_weights[j]
                if deg_weight != 0:
                    rankings_vec[j] *= 1/deg_weight

        """ PageRank computed; now sort and print """
        ranks = rankings_vec[:,0]
        rank2pnum = np.flipud(np.argsort( ranks ))
        pnum2rank = {}
        for idx_j, rank in enumerate(rank2pnum):
            pnum2rank[idx_j] = rank
        # Get each player's top game win
        bestwins = {}
        worstlosses = {}
        for idxj in range(pmat.shape[0]):
            getwins = [ (int(col_j), ranks[col_j]) for col_j, val_j in enumerate(pmat[idxj, :]) if val_j != 0.0 ]
            if len(getwins) == 0:
                bestwins[idxj] = 'NONE-XXX'
            else:
                bestwins[idxj] = num2pname[ int(max(getwins, key = lambda t: t[1])[0]) ]

            getlosses = [ (int(row_j), ranks[row_j]) for row_j, val_j in enumerate(pmat[:,idxj]) if val_j != 0.0]
            if len(getlosses) == 0:
                worstlosses[idxj] = 'NONE-XXX'
            else:
                worstlosses[idxj] = num2pname[ int(min(getlosses, key = lambda t: t[1])[0]) ]

        print("Rank", '\t', "Name".ljust(25), "Rating".ljust(8), '# Games played', '\t best game win', '\t worst game loss' )
        for j in range( 0, min(num_to_print, len(ranks)) ):
            print("{:<} \t {:<21} {:>10.7f}"
            " {:>16d} {:>20} {:>20}".format(str(j+1), num2pname[rank2pnum[j]],
            ranks[rank2pnum[j]], int(degree_weights[rank2pnum[j]]),
            bestwins[rank2pnum[j]], worstlosses[rank2pnum[j]] ) )
