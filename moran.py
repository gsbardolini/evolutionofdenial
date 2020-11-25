from dynamics import StochasticDynamicsSimulator
import numpy
import statistics
import math
from decimal import Decimal

def truncate(n, decimals=0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier
def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

def round_half_away_from_zero(n, decimals=0):
    rounded_abs = round_half_up(abs(n), decimals)
    return math.copysign(rounded_abs, n)

class Moran(StochasticDynamicsSimulator):
    """
    A stochastic dynamics simulator that performs the Moran process on all player types in the population.
    See U{Moran Process<http://en.wikipedia.org/wiki/Moran_process#Selection>}
    """
    def __init__(self, num_iterations_per_time_step=1, *args, **kwargs):
        """
        The constructor for the Moran dynamics process, that the number of births/deaths to process per time step.

        @param num_iterations_per_time_step: the number of iterations of the Moran process we do per time step
        @type num_iterations_per_time_step: int
        """
        super(Moran, self).__init__(*args, **kwargs)
        assert num_iterations_per_time_step >= 1
        self.num_iterations_per_time_step = num_iterations_per_time_step

    # def next_generation(self, previous_state, prev_true_state, true_state):
    def next_generation(self, prev_true_state, previous_state, true_state):
        next_state = []

        # copy to new state
        for p in previous_state:
            next_state.append(p.copy())


        #  potential idea to get average distribution from prev_true_state and previous_state
        # for p,c in zip(prev_true_state, previous_state):
        #     # print((p+c)/2)
        #     nxt = (p+c)/2


        #     nxt = numpy.array([round_half_away_from_zero(n, 10) for n in nxt])
        #     e = (100 - nxt.sum()) / len(nxt)
        #     # print(nxt.sum())

        #     nxt[0] += float(e)
        #     next_state.append(nxt.copy())

        fitness = self.calculate_fitnesses(next_state, true_state)

        minimum_total = min(p.sum() for p in next_state)
        # make sure there are enough individuals of each type to take away 2 * num_iterations_per_time_step
        num_iterations = int(min(self.num_iterations_per_time_step * 2, minimum_total) / 2)

        for idx, (p, f) in enumerate(zip(next_state, fitness)):
            reproduce = numpy.zeros(len(p))

            for i in range(num_iterations):
                # sample from distribution to determine winner and loser (he who reproduces, he who dies)
                weighted_total = sum(n_i * f_i for n_i, f_i in zip(p, f))
                dist = numpy.array([n_i * f_i / weighted_total for n_i, f_i in zip(p, f)])
                sample = numpy.random.multinomial(1, dist)
                p -= sample
                reproduce += sample

            for i in range(num_iterations):
                # now determine who dies from what's left
                total = p.sum()
                dist = [n_i / float(total) for n_i in p]
                p -= numpy.random.multinomial(1, dist)


            next_state[idx] = p + reproduce * 2

            if idx == 1: # receiver
                other = abs(idx-1) # sender

                send_strat = numpy.where(prev_true_state[other] == numpy.amax(prev_true_state[other])) # strategy of the oponent last time same state was true
                curr_strat = numpy.where(next_state[idx] == numpy.amax(next_state[idx])) # current state of the player

                # switch the best strategy in current state with best strategy from last time same state was true
                if curr_strat[0][0] != send_strat[0][0]:
                    switch = next_state[idx][send_strat[0][0]]
                    next_state[idx][send_strat[0][0]] = next_state[idx][curr_strat[0][0]]
                    next_state[idx][curr_strat[0][0]] = switch
                    # next_state[idx][send_strat[0][0]] += 12
                    # next_state[idx][curr_strat[0][0]] -= 12

                    # print("after", next_state[idx], true_state)

        return next_state, fitness
