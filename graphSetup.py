from plot import plot_data_for_players, GraphOptions

import matplotlib.pyplot as plt
import numpy
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import math
import copy
from plotHelperFunct import *

def setupGraph(graph, game=None, dyn=None, burn=None, num_gens=None, results=None, payoffs=None, true_states = None, results_dict = None, payoffs_dict = None):  # TODO allow ordering of various lines
    if graph is True:
        graph = dict()
    graph_options = graph
    if 'options' in graph_options:
        for key in graph_options['options']:
            graph_options[key] = True
        del graph_options['options']

    yPos = 0

    if game is not None and game.STRATEGY_LABELS is not None:
        graph_options[GraphOptions.LEGEND_LABELS_KEY] = lambda p, s: game.STRATEGY_LABELS[p][s]

    if game is not None and game.PLAYER_LABELS is not None:
        graph_options[GraphOptions.TITLE_KEY] = lambda p: game.PLAYER_LABELS[p]

    if any(k in graph_options for k in ['payoffLine', 'modeStratLine', 'meanStratLine']):
        yPos = 0
        graph_options['colorLineArray'] = [[] for player in results]
        graph_options['textList'] = []

    if 'payoffLine' in graph_options:
        yPos -= 0.05
        for playerIdx, player in enumerate(payoffs):

            colorLineArray = []
            for gen in range(burn, num_gens - 1):
                maxPayoff = 0
                maxPayoffIdx = -1
                for payoffIdx, payoff in enumerate(player[gen]):
                    print("HALLO", payoffIdx, payoff)
                    if payoff > maxPayoff:
                        maxPayoff = payoff
                        maxPayoffIdx = payoffIdx

                currentGen = gen - burn
                nextGen = gen - burn + 1

                line = [currentGen, nextGen, yPos, yPos]
                colorLineArray.append([line, maxPayoffIdx])
            # colorLineArray[0][1] = colorLineArray[1][1]  # To fill in first gen
            graph_options['colorLineArray'][playerIdx].extend(colorLineArray)
            #graph_options['textList'].append(([-num_gens / 7, yPos], 'Best Strat'))  # TODO fix x positioning

    if 'modeStratLine' in graph_options:
        yPos -= 0.05
        for playerIdx, player in enumerate(results):
            colorLineArray = []
            for gen in range(burn, num_gens):
                maxStratProp = 0
                maxStratIdx = -1
                for stratIdx, stratProp in enumerate(player[gen]):
                    if stratProp > maxStratProp:
                        maxStratProp = stratProp
                        maxStratIdx = stratIdx

                currentGen = gen - burn
                nextGen = gen - burn + 1
                line = [currentGen, nextGen, yPos, yPos]
                colorLineArray.append([line, maxStratIdx])
            graph_options['colorLineArray'][playerIdx].extend(colorLineArray)
            #graph_options['textList'].append(([-num_gens / 7, yPos], 'Modal Strat'))

    if 'meanStratLine' in graph_options:
        yPos -= 0.05
        #graph_options['textList'].append(([-num_gens / 7, yPos], 'Mean Strat'))

    yPos -= 0.025

    graph_options[GraphOptions.NO_MARKERS_KEY] = True

    if results is not None:

        # for state in results_dict:
        #     print("res", len(results[state]))
        #     print(results[state][0][0])
        #     # plt.plot(x_values, data_i[:, cat_i], c=colors[cat_i % n_cats], lw=2, marker=marker)
        #     # legend = plt.legend(labels, loc=graph_options[GraphOptions.LEGEND_LOCATION_KEY], fontsize=fontsize)
        #     plot_data_for_players(results[state], results_dict, true_states, range(burn, len(results[state][0])), "Generation #", dyn.pm.num_strats,
        #                     num_players=dyn.num_players,
        #                     graph_options=graph_options, yBot=yPos)
        plot_data_for_players(results, results_dict, true_states, range(burn, num_gens), "Generation #", dyn.pm.num_strats,
                          num_players=dyn.num_players,
                          graph_options=graph_options, yBot=yPos)


    if 'graph_payoffs' in graph_options:
        if burn == 0:
            burn = 1
        plot_data_for_players(payoffs, results_dict, true_states, range(burn, num_gens), "Generation #", dyn.pm.num_strats,
                              num_players=dyn.num_players,
                              graph_options=dict(), title="Normalized Payoffs")