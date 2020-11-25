from game import Game
import random
import numpy as np
import itertools

class RGSmall(Game):
    DEFAULT_PARAMS = dict(RPayoffacc=1, RPayoffrej=1, SPayoff=1, k=0, aProp = 1, bProp = 1)


    words = ['A', 'B']
    # compositions = [''.join(c) for c in itertools.combinations(words,len(words))]
    compositions = [''.join(c) for c in itertools.permutations(words, len(words))]
    strategies = tuple(words + compositions)

    STRATEGY_LABELS = tuple([tuple(strategies)] * len(strategies) + [('Accept Message', 'Reject Message')] * len(strategies))

    PLAYER_LABELS= tuple(['State'+ str(x+1) for x in range(len(strategies))]) + tuple([('Receiver State' + str(state+1)) for state in range(len(strategies))])
    # print(PLAYER_LABELS)
    # PLAYER_LABELS = ('Sender', 'Receiver')
    EQUILIBRIA_LABELS = strategies
    print(STRATEGY_LABELS)
    print(PLAYER_LABELS)
    print(EQUILIBRIA_LABELS)
    # for i in EQUILIBRIA_LABELS:
    #     print(i, len(i))


    # permutations = [p for p in itertools.product(strategies, repeat=len(strategies))]
    # payoff_matrices = None

    def __init__(self, k, SPayoff, RPayoffacc, RPayoffrej, aProp, bProp, equilibrium_tolerance=0.2):


        aProp, bProp = aProp/(aProp+bProp), bProp/(aProp+bProp)
        def senderpayoff(SPayoff):
            # payoffs_sender = [[[0] * len(self.EQUILIBRIA_LABELS)] * 2] * len(self.EQUILIBRIA_LABELS)
            payoffs_sender = [[[0 for _ in range(len(self.EQUILIBRIA_LABELS))] for _ in range(2)] for _ in range(len(self.EQUILIBRIA_LABELS))]
            for state in range(len(self.EQUILIBRIA_LABELS)):
                for message in range(len(self.EQUILIBRIA_LABELS)):
                    payoffs_sender[state][0][message] = 2
            # print(payoffs_sender)
            return payoffs_sender


        payoffs_sender = senderpayoff(SPayoff)
        # print("s1", payoffs_s1)
        # payoffs_s2 = senderpayoff(SPayoff)
        # print("s2", payoffs_s2)
        states = list(range(len(self.EQUILIBRIA_LABELS)))
        # print("states", states)

        p0 = np.random.choice(states)
        states.remove(p0)
        p1 = np.random.choice(states)
        # print("state", p0, p1)
        def receiver_payoff(aProp, bProp, k, RPayoffacc, RPayoffrej):
            # WHERE IS TRUE STATE CHOSEN
            # payoffs_rec = [[[0 for x in range(4)] for x in range(2)] for x in range(2)]
            payoffs_rec = [[[0 for _ in range(len(self.EQUILIBRIA_LABELS))] for _ in range(2)] for _ in range(len(self.EQUILIBRIA_LABELS))]
            for state in range(len(self.EQUILIBRIA_LABELS)):
                for message in range(len(self.EQUILIBRIA_LABELS)):
                    if len(self.EQUILIBRIA_LABELS[state]) == 1:
                        if state == message:
                            print("hello receiver")
                            payoffs_rec[state][0][message] = 2
                        elif self.EQUILIBRIA_LABELS[state] in self.EQUILIBRIA_LABELS[message]:
                            print("HEYYYYY")
                            payoffs_rec[state][0][message] = 1
                            payoffs_rec[state][1][message] = 1 #???? should i??
                        elif state != message:
                            payoffs_rec[state][1][message] = 2
                    else:
                        if state == message:
                            payoffs_rec[state][0][message] = 2
                        elif self.EQUILIBRIA_LABELS[message] in self.EQUILIBRIA_LABELS[state]:
                            payoffs_rec[state][0][message] = 1
                            payoffs_rec[state][1][message] = 2 #or reward 1???
                        elif state != message and len(self.EQUILIBRIA_LABELS[state]) > 1:
                            payoffs_rec[state][0][message] = 1/2
                            payoffs_rec[state][1][message] = 1/2
            return payoffs_rec

        payoffs_receiver = receiver_payoff(aProp, bProp, k, RPayoffacc, RPayoffrej)
        print("receiver", payoffs_receiver)

        payoff_matrix = []
        for state in range(len(self.EQUILIBRIA_LABELS)):
            # if state <=
            payoff_matrix.append(payoffs_sender[state])
        for state in range(len(self.EQUILIBRIA_LABELS)):
            payoff_matrix.append(payoffs_receiver[state])
        # for i in payoff_matrix:
        #     print(i)
        # print("MATRIX", payoff_matrix[0])
        # payoff_matrix = [payoffs_sender, payoffs_receiver]
        print(payoff_matrix)
        # for i in payoff_matrix:
        #     print("i",i)
        # print(payoff_matrix)
        # print("DIST", aProp/2, bProp/2)
        # player_dist = (0.2, 0.2, 0.2, 0.4)
        player_dist = tuple([1 / len(self.PLAYER_LABELS) for _ in range(len(self.PLAYER_LABELS))])
        # print(player_dist)
        # player_dist = (1/2, 1/2)
        super(RGSmall, self).__init__(payoff_matrices=payoff_matrix,player_frequencies=player_dist, equilibrium_tolerance=equilibrium_tolerance)

    @classmethod
    def classify(cls, params, state, tolerance):
        # p = params
        threshold = 0.5

        if state[0][0] > threshold and state[1][0] > threshold:
            # A
            return 0
        elif state[0][1] > threshold and state[1][1] > threshold:
            # B
            return 1
        else:
            return super(RGSmall, cls).classify(params, state, tolerance)

if __name__ == "__main__":
    x = RGSmall(0, 1, 1, 1, 0.5, 0.5)
    # print("PAY", x.senderpayoff(1))
