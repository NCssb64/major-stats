"""
    Plotting info from the smash archive
"""

#py imports
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter

#local imports
import smasharchive

labels = ['pools', 'bracket', 'top32', 'top16', 'top8', 'top4', 'grands', 'reset']

def make_single_plot(temp_char_map, temp_char_name, pltname, print_plots=False):
    # plt.figure(num=None, figsize=(8, 5), dpi=100, facecolor='w', edgecolor='k')
    fig, ax = plt.subplots()
    
    for data in temp_char_map:
        ax.plot(data)

    # Rewrite the y labels
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f '))

    plt.title('Character usage: ' + pltname)
    plt.xlabel('Stage of tournament')
    plt.ylabel('Ratio of total character usage that stage')

    end_idx = min( len(temp_char_map[0]), len(labels) )
    use_labels = labels[0:end_idx]
    plt.xticks(range(len(use_labels)), use_labels, rotation='vertical')

    ax.legend(temp_char_name, loc='center right', bbox_to_anchor=(1.25, 0.50))
    
    #plt.tight_layout()
    plt.gcf().subplots_adjust(wspace=2, hspace=2, right=0.825, bottom=0.25)
    #plt.gcf().subplots_adjust(right=None, left=None, top=None, bottom=None)

    plt.show()
    if print_plots == True:
        plt.savefig('../smasharticle/figures/{msg:>0}.eps'.format(msg=pltname), format='eps')
        plt.savefig('../smasharticle/figures/{msg:>0}.png'.format(msg=pltname))
        plt.close(fig)
    
def plot_char_use(db, plotnameroot, plot_flag=False):
    # db = smasharchive.smashdb()
    levels = [
        [0,0],
        [1,2],
        [3,3],
        [4,4],
        [5,5],
        [6,7],
        [8,9]
    ]

    num_levels = len(levels)
    char_use_map = {}
    for key in db.charnames.keys():
        char_use_map[key] =  np.zeros((num_levels,1))

    games_at_stage = np.zeros( (num_levels, 1) )
    for which_level in range(num_levels):
        db.level_limits = levels[which_level]
        db.refilter_archive()
        for j in range(len(db.muchar_tots)):
            char_use_map[db.muchar_tots[j][0]][which_level] = db.muchar_tots[j][1]
            games_at_stage[which_level] += db.muchar_tots[j][1]

    splitting_point = 0.10
    nametags = ['-hightier', '-lowtier', '-fullcast']
    intervals = [ [0, splitting_point],
                  [splitting_point, 1],
                  [0, 1]
                ]
    # ALL PLOTS
    for which_plot in range(len(nametags)):
        nametag = nametags[which_plot]
        temp_char_map = []
        temp_char_name = []
        for key in char_use_map.keys():
            data = np.divide( char_use_map[key] , games_at_stage )
            a = intervals[which_plot][0]
            b = intervals[which_plot][1]
            if max(data) < b and max(data) >= a:
                continue
            temp_char_map.append(data)
            temp_char_name.append(key)
        make_single_plot(temp_char_map, temp_char_name, plotnameroot+nametag, plot_flag)

    # Low tiers
    nametag = '-lowtier'
    temp_char_map = []
    temp_char_name = []
    for key in char_use_map.keys():
        data = np.divide( char_use_map[key] , games_at_stage )
        if max(data) >= splitting_point:
            continue
        temp_char_map.append(data)
        temp_char_name.append(key)
    make_single_plot(temp_char_map, temp_char_name, plotnameroot+nametag, plot_flag)

    # Full cast
    nametag = '-fullcast'
    temp_char_map = []
    temp_char_name = []
    for key in char_use_map.keys():
        data = np.divide( char_use_map[key] , games_at_stage )
        temp_char_map.append(data)
        temp_char_name.append(key)

    make_single_plot(temp_char_map, temp_char_name, plotnameroot+nametag, plot_flag)