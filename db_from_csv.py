import numpy as np


def skip_this_game( comp_level, players, query_specs):
    """Determines if a game falls outside the input search criteria

    Parameters
    ----------
    comp_level -- int; level of a competition (bracket or pools) of input game

    players -- list; players involved in input game

    query_specs -- dict; contains the specifications of the query:
            which level of competition to include,
            whether to not to skip any specific players

    Returns
    -------
    bool -- true or false, whether or not the input game should be skipped

    """
    level_limits = query_specs['limits']
    skip_these_players = query_specs['skips']
    bracket_levels_map = query_specs['bracket_map']

    if (bracket_levels_map[comp_level] < level_limits[0]) or (bracket_levels_map[comp_level] > level_limits[1]):
        return True
    play1, play2 = players
    if (play1 in skip_these_players.keys()) or (play2 in skip_these_players.keys()):
        return True


def load_csv( query_specs ):
    """Builds dictionary of games satisfying query specifications from csv archive

    Parameters
    ----------
    query_specs -- dict; contains specifications on what games to use in archive

    Returns
    -------
    list; each entry is a dict representing a game. The dict contains all info for that game.

    """

    level_limits = query_specs['limits']
    skip_these_players = query_specs['skips']
    bracket_levels_map = query_specs['bracket_map']

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
        if skip_this_game( comp_level, parts[2:4], query_specs) == True:
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
            'tournaments_included':tournaments,
            'query_specs':query_specs
            }
