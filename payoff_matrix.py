__author__ = 'elubin'
import numpy
import logging


class PayoffMatrix(object):
    """
    A class that encapsulates the notion of a set of payoff matrices for a game (one for each player), and provides
    convenience methods for getting the payoff for each player given a strategy set, as well as calculating the
    expected payoff given a distribution of players playing each strategy.
    """

    def __init__(self, num_players, payoff_matrices):
        print("num", num_players)
        self.num_player_types = num_players
        self.payoff_matrices = payoff_matrices
        self.num_strats = []

        states = list(range(4))
        state = numpy.random.choice(states)
        self.true_state = 0
        self.state = state
        self.i = 0
        # root = self.payoff_matrices[0]
        # print("hallo art")
        # for i in range(self.num_player_types):
        #     # print("var", i)
        #     # print("num_strats", self.num_strats)
        #     self.num_strats.append(len(root))
        #     root = root[0]
        # print("num_strats", self.num_strats)
        self.num_strats = [4,8]
        # if num_players != 1:  # Allows for single population games
        #     self.verify_payoff_matrix_dimensions()
        self.compute_dominated_strategies()

    def verify_payoff_matrix_dimensions(self):
        """
        Verify that "depth" of each payoff matrix matches number of elements in player_dist
        """
        # print("num", self.num_strats)

        for m in self.payoff_matrices:
            # print("VERIFY", m, self.num_strats[:])
            self._verify_dimensions(m, self.num_strats[:])

    def _verify_dimensions(self, m, num_strats):
        """
        Recursive helper function to verify the dimensions of the payoff matrix
        """
        if len(num_strats) == 0:
            assert isinstance(m, (int, float))
            return
        n = num_strats.pop(0)
        assert n == len(m)
        for i in m:
            self._verify_dimensions(i, num_strats[:])

    def get_payoff(self, recipient, *strats):
        """
        Get the payoff for the player index recipient, by specifying the strategies that everyone plays in increasing
        player order.

        @param recipient: the index of the player for which to get the payoff, 0-indexed
        @type recipient: int
        @param strats: the iterable of strategies played by each player, in the order of their indices
        @type strats: list(int)
        @return: the payoff that the recipient gets from all playres playing the given strategy
        @rtype: float
        """
        # print("rec", recipient)
        # print(self.state)
        matrix = self.payoff_matrices[recipient][self.true_state]
        # print( matrix[self.state])
        # # print("strats", strats, matrix)
        # print("mmmm", strats)
        # matrix = self.payoff_matrices[recipient][strats[0]][strats[1]]
        # print("mmmm", matrix, strats)
        # strats = list(strats)
        # strats.reverse()
        # print("rev", strats.reverse())
        # self.i+=1
        # print("MATRIX", matrix)
        for idx in strats:
            matrix = matrix[idx]
        # print("MATRIX", matrix)
        # print(self.i)
        return matrix

    def get_expected_payoff(self, player_idx, strategy, current_state, true_state):
        """
        Get the expected payoff if the player at idx player_idx plays indexed by strategy given the current state.
        @param player_idx: the index of the player for which to get the expected payoff
        @type player_idx: int
        @param strategy: the index that the player will play
        @type strategy: int
        @param current_state: The state of the population(s). Each entry in the parent array refers to a player type, each entry in each sublist refers to the number or
            frequency of players playing that strategy.
        @type current_state: list
        @return: the expected payoff
        @rtype: float
        """
        return self._iterate_through_players(player_idx, 0, {player_idx: strategy}, 1.0, current_state, true_state)

    def _iterate_through_players(self, target_player_idx, current_player_idx, other_player_strategies, probability, current_state, true_state):
        self.true_state = true_state
        if (len(other_player_strategies) == self.num_player_types and self.num_player_types != 1) or (len(other_player_strategies) == 2 and self.num_player_types == 1):
            # Second portion accounts for single player, TODO change (2) to dependent upon matrix depth
            # print("other", other_player_strategies)
            if self.num_player_types == 1:
                strats = [0] * 2  # TODO generalize based on payoff matrix depth
            else:
                strats = [0] * self.num_player_types
            for i in range(len(strats)):#range(self.num_player_types):
                strats[i] = other_player_strategies[i]

            payoff = self.get_payoff(target_player_idx, *strats)
            # print("Payoff", payoff)
            # print("??", payoff, probability)
            return payoff * probability

        elif current_player_idx in other_player_strategies:
            # skip it, we already picked the strategy
            return self._iterate_through_players(target_player_idx, current_player_idx + 1, other_player_strategies, probability, current_state, true_state)
        else:
            # iterate over the current player idx dimension, recursively calling yourself on every iteration
            if len(current_state) == 1:  # Single population game
                payoff = 0
                for strat in range(self.num_strats[0]):
                    n = current_state[0][strat]
                    print(n)
                    p = float(n) / current_state[0].sum()
                    dict_copy = other_player_strategies.copy()
                    dict_copy[current_player_idx] = strat
                    payoff += self._iterate_through_players(target_player_idx, current_player_idx + 1, dict_copy, probability * p, current_state)
                return payoff
            else:
                payoff = 0
                for strat in range(self.num_strats[current_player_idx]):
                    n = current_state[current_player_idx][strat]
                    p = float(n) / current_state[current_player_idx].sum()
                    dict_copy = other_player_strategies.copy()
                    dict_copy[current_player_idx] = strat
                    # print("payoff1", self._iterate_through_players(target_player_idx, current_player_idx + 1, dict_copy, probability * p, current_state))
                    payoff += self._iterate_through_players(target_player_idx, current_player_idx + 1, dict_copy, probability * p, current_state, true_state)
                return payoff
    # def _iterate_through_players(self, target_player_idx, current_player_idx, other_player_strategies, probability, current_state, true_state):
    #     # strats =
    #     # self.get_payoff(target_player_idx, strats)
    #     self.true_state = true_state
    #     # print("true_state", true_state)
    #     if (len(other_player_strategies) == self.num_player_types and self.num_player_types != 1) or (len(other_player_strategies) == 2 and self.num_player_types == 1):
    #         # Second portion accounts for single player, TODO change (2) to dependent upon matrix depth
    #         # if self.num_player_types == 1:
    #         #     strats = [0] * 2  # TODO generalize based on payoff matrix depth
    #         # else:
    #         # print("other", other_player_strategies)
    #         # print("hello")
    #         if self.num_player_types == 1:
    #             strats = [0] * 2  # TODO generalize based on payoff matrix depth
    #         else:
    #             strats = [0] * self.num_player_types
    #         # strats = [0] * self.num_player_types
    #         payoff = self.get_payoff(target_player_idx, *strats)
    #         for i in range(len(strats)):#range(self.num_player_types):
    #             # print("hallo", other_player_strategies[i])
    #             strats[i] = other_player_strategies[i]
    #         # print("STRATS", strats)

    #         # print("??", payoff, probability)
    #         return payoff * int(probability)

    #     elif current_player_idx in other_player_strategies:
    #         # skip it, we already picked the strategy
    #         return self._iterate_through_players(target_player_idx, current_player_idx + 1, other_player_strategies, probability, current_state, true_state)
    #     else:
    #         # iterate over the current player idx dimension, recursively calling yourself on every iteration
    #         if len(current_state) == 1:  # Single population game
    #             payoff = 0
    #             for strat in range(self.num_strats[0]):
    #                 n = current_state[0][strat]
    #                 p = float(n) / current_state[0].sum()
    #                 dict_copy = other_player_strategies.copy()
    #                 dict_copy[current_player_idx] = strat
    #                 payoff += self._iterate_through_players(target_player_idx, current_player_idx + 1, dict_copy, probability * p, current_state, true_state)
    #             print(payoff)
    #             return payoff
    #         else:
    #             payoff = 0
    #             for strat in range(self.num_strats[current_player_idx]):
    #             # for strat in range(self.num_strats[current_player_idx]):
    #                 n = current_state[current_player_idx][strat]
    #                 p = float(n) / current_state[current_player_idx].sum()
    #                 dict_copy = other_player_strategies.copy()
    #                 dict_copy[current_player_idx] = strat
    #                 # print("payoff1", self._iterate_through_players(target_player_idx, current_player_idx + 1, dict_copy, probability * p, current_state))
    #                 payoff += self._iterate_through_players(target_player_idx, current_player_idx + 1, dict_copy, probability * p, current_state,true_state)
    #             # print(payoff)
    #             return payoff


    def get_all_strategy_tuples(self):
        """
        @return: a generator of all strategy tuples representing non-mixed strategies for all players
        @rtype: generator
        """
        return self._strategy_tuple_helper(0, ())

    def _strategy_tuple_helper(self, p, s):
        if p == self.num_player_types:
            yield s
            return

        for s_i in range(self.num_strats[p]):
            for r in self._strategy_tuple_helper(p + 1, s + (s_i, )):
                yield r

    def compute_dominated_strategies(self):
        # for every strategy for every player, iterate through all strategies for all other players and see if there are
        # any strategies that are completely dominated by other strategies
        # dominated is a dictionary of sets

        # we have a loop to simulate the iterated elimination of dominated strategies
        continue_iterating = True
        dominated_strategies = set()

        while continue_iterating:
            continue_iterating = False
            for p_i in range(self.num_player_types):
                payoffs = []
                for s_i in range(self.num_strats[p_i]):
                    payoffs.append(numpy.array(self._get_all_payoffs(p_i, s_i, dominated_strategies)))


                for s_1 in range(self.num_strats[p_i]):
                    if (p_i, s_1) in dominated_strategies:
                        continue
                    # consider s_1 as a dominated strategy
                    for s_2 in range(self.num_strats[p_i]):
                        # if s_2 is dominated, we can ignore it. can't both be be dominated and dominate another one
                        if (p_i, s_2) in dominated_strategies:
                            continue

                        if (payoffs[s_2] > payoffs[s_1]).all():
                            dominated_strategies.add((p_i, s_1))
                            continue_iterating = True
                            break
        # (player index, strategy) index set of tuples of dominated strategies
        self.dominated_strategies = set()




    def _get_all_payoffs(self, p, s, dominated):
        # get a list of all possible payoffs a given player can get for playing a given strategy
        # the list is computed in order, by iterating through all the other strategy pairs for all the other players
        # TODO need to ignore payoffs for dominated strategies
        return list(self._get_all_payoffs_helper(p, s, 0, (), dominated))

    def _get_all_payoffs_helper(self, p, s, cur_p, cur_s, dominated):
        if cur_p == self.num_player_types:
            yield self.get_payoff(p, *cur_s)
            return
        elif cur_p == p:
            for r in self._get_all_payoffs_helper(p, s, cur_p + 1, cur_s + (s, ), dominated):
                yield r
            return
        else:
            for s_i in range(self.num_strats[cur_p]):
                if (cur_p, s_i) in dominated:
                    continue
                for r in self._get_all_payoffs_helper(p, s, cur_p + 1, cur_s + (s_i, ), dominated):
                    yield r

    def is_pure_equilibrium(self, s):

        assert self.num_player_types == len(s)
        strategies = list(s)
        for n_i in range(self.num_player_types):

            best_payoff = self.get_payoff(n_i, *s)
            for s_i in range(self.num_strats[n_i]):
                if s_i == s[n_i]:
                    continue
                strategies[n_i] = s_i
                p = self.get_payoff(n_i, *strategies)
                if p > best_payoff:
                    return False, n_i, s_i  # profitable deviation for player n_i to play s_i instead of s[n_i]

            strategies[n_i] = s[n_i]

        return True

    def is_mixed_equilibrium(self, s):
        assert self.num_player_types == len(s)
        logging.debug("testing %s", s)
        for n_i in range(self.num_player_types):
            logging.debug("player %d", n_i)
            payoffs = []
            for i, s_i in enumerate(s[n_i]):
                if s_i > 0:
                    # get expected payoff of mixing this strategy
                    payoffs.append((i, self.get_expected_payoff(n_i, i, s)))
            logging.debug("payoffs %s", payoffs)
            if len(payoffs) > 1:
                for i, (idx_i, p) in enumerate(payoffs):
                    for j, (idx_j, q) in enumerate(payoffs[i:]):
                        if abs(q - p) > (1e-08 + 1e-05 * abs(p)):
                            return True, n_i, ((idx_i, p), (idx_j, q))

            else:
                # only one strategy, this is pure equilibrium
                # check to make sure there's no incentive of switching strategies

                # get index of pure strategy
                s_idx = [i for i, x in enumerate(s[n_i]) if s[n_i][i] > 0][0]

                best_payoff = self.get_expected_payoff(n_i, s_idx, s)
                logging.debug("Best payoff %f", best_payoff)
                for s_i in range(self.num_strats[n_i]):
                    if s_i == s_idx:
                        continue
                    p = self.get_expected_payoff(n_i, s_i, s)
                    logging.debug("Strategy %d payoff %f", s_i, p)
                    if p > best_payoff:
                        return False, n_i, s_i  # profitable deviation for player n_i to play s_i instead of s[n_i]

        return True

if __name__ == '__main__':
    x = PayoffMatrix(2, [[[[2, 2, 2, 2], [0, 0, 0, 0]], [[2, 2, 2, 2], [0, 0, 0, 0]], [[2, 2, 2, 2], [0, 0, 0, 0]], [[2, 2, 2, 2], [0, 0, 0, 0]]], [[[2, 0, 1, 1], [0, 2, 1, 1]], [[0, 2, 1, 1], [2, 0, 1, 1]], [[1, 1, 2, 0.5], [2, 2, 0, 0.5]], [[1, 1, 0.5, 2], [2, 2, 0.5, 0]]]])