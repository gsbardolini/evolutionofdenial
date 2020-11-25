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

    #STRATEGY_LABELS = tuple([tuple(strategies)] * len(strategies) + [('Accept Message', 'Reject Message')] * len(strategies))
    # STRATEGY_LABELS = (tuple(strategies), ('Accept Message', 'Reject Message'))
    receiver = tuple(['Accept ' + str(state) for state in strategies] + ['Reject ' + str(state) for state in strategies])
    STRATEGY_LABELS = (tuple(strategies), receiver)
    print(STRATEGY_LABELS[1])
    # PLAYER_LABELS= tuple(['State'+ str(x+1) for x in range(len(strategies))]) + tuple([('Receiver State' + str(state+1)) for state in range(len(strategies))])
    # print(PLAYER_LABELS)
    PLAYER_LABELS = ('Sender', 'Receiver')

    EQUILIBRIA_LABELS = strategies
    # for i in EQUILIBRIA_LABELS:
    #     print(i, len(i))


    # permutations = [p for p in itertools.product(strategies, repeat=len(strategies))]
    # payoff_matrices = None

    def __init__(self, k, SPayoff, RPayoffacc, RPayoffrej, aProp, bProp, equilibrium_tolerance=0.2):


        aProp, bProp = aProp/(aProp+bProp), bProp/(aProp+bProp)
        def senderpayoff(SPayoff):
            # payoffs_sender = [[[0] * len(self.EQUILIBRIA_LABELS)] * 2] * len(self.EQUILIBRIA_LABELS)
            payoffs_sender = [[[0 for _ in range(8)] for _ in range(4)] for _ in range(len(self.EQUILIBRIA_LABELS))]
            # payoffs_sender = [[0 for _ in range(len(self.EQUILIBRIA_LABELS))] for _ in range(2)]
            #  one matrix:
            k = 1.5
            # payoffs_sender= [[0 for _ in range(2)] for _ in range(len(self.EQUILIBRIA_LABELS))]
            for state in range(len(self.EQUILIBRIA_LABELS)):
                for message in range(len(self.EQUILIBRIA_LABELS)):
                    # for strategy in range(len(self.STRATEGY_LABELS[1])):
                        # if state == message:
                    # payoffs_sender[message][0] = 2
                    # payoffs_sender[0][0][0] = 5
                    payoffs_sender[state][message][message] = 10
                    # payoffs_sender[0][0][message] = 2
                    if state == message:
                        payoffs_sender[state][message][message] *= k

                    # # # # #     payoffs_sender[state][message][message+4] = k
                    # else:
                    # # # if state != message:
                    #     payoffs_sender[state][message][message] *= -k
                    #     payoffs_sender[state][message][message+4] = 2 * -k
            return payoffs_sender

        #     # print(payoffs_sender)


        #

        payoffs_sender = senderpayoff(SPayoff)
        # print("sender", payoffs_sender)
        # print("s1", payoffs_s1)
        # payoffs_s2 = senderpayoff(SPayoff)
        # print("s2", payoffs_s2)

        # p1 = np.random.choice(states)
        # states = list(self.EQUILIBRIA_LABELS)
        # # print("states", states)

        # state = states.index(np.random.choice(states))
        # print("true state", state)
        # states.remove(state)
        # print("state", p0, p1)
        def receiver_payoff(aProp, bProp, k, RPayoffacc, RPayoffrej):
            # WHERE IS TRUE STATE CHOSEN
            # payoffs_rec = [[[0 for x in range(4)] for x in range(2)] for x in range(2)]
            # payoffs_rec = [[0 for _ in range(2)] for _ in range(len(self.EQUILIBRIA_LABELS))]
            a = 10
            b = 5
            c = 1
            payoffs_rec = [[[0 for _ in range(8)] for _ in range(4)] for _ in range(len(self.EQUILIBRIA_LABELS))]
            for state in range(len(self.EQUILIBRIA_LABELS)):
                for message in range(len(self.EQUILIBRIA_LABELS)):
                    if len(self.EQUILIBRIA_LABELS[state]) == 1:
                        if state == message:
                            print("hello receiver")
                            # payoffs_rec[message][0] = 2
                            payoffs_rec[state][message][message] = a

                        elif self.EQUILIBRIA_LABELS[state] in self.EQUILIBRIA_LABELS[message]:
                            print("HEYYYYY")
                            payoffs_rec[state][message][message] = b
                            payoffs_rec[state][message][message+4] = b
                            # payoffs_rec[message][0] = 1
                            # payoffs_rec[message][1] = 1 #???? should i??
                        elif state != message:
                            payoffs_rec[state][message][message+4] = a
                            # payoffs_rec[message][1] = 2
                    else:
                        if state == message:
                            payoffs_rec[state][message][message] = a
                            # payoffs_rec[message][0] = 2
                        elif self.EQUILIBRIA_LABELS[message] in self.EQUILIBRIA_LABELS[state]:
                            payoffs_rec[state][message][message] = b
                            payoffs_rec[state][message][message+4] = b
                            # payoffs_rec[message][0] = 1
                            # payoffs_rec[message][1] = 2 #or reward 1???
                        elif state != message and len(self.EQUILIBRIA_LABELS[state]) > 1:
                            payoffs_rec[state][message][message] = b/2
                            payoffs_rec[state][message][message+4] = (b/2)*3
                            # payoffs_rec[message][0] = 1/2
                            # payoffs_rec[message][1] = 1/2
            return payoffs_rec
        payoffs_receiver = receiver_payoff(aProp, bProp, k, RPayoffacc, RPayoffrej)
        # "receiver")
        # for i in payoffs_sender[0]:
        #     print(i)


        payoff_matrix = [payoffs_sender, payoffs_receiver]
        # print("i",i)
        print("MATRIX")
        for player in range(len(payoff_matrix)):
            print("Player: ", player)
            for state in range(len(payoff_matrix[player])):
                print("State: ", state)
                for i in payoff_matrix[player][state]:
                    print(i)
            # print(i)range(len)
            for j in i:
                print(j)
        # print(payoff_matrix)
        # print("DIST", aProp/2, bProp/2)
        # player_dist = (0.2, 0.2, 0.2, 0.4)
        # player_dist = tuple([1 / len(self.PLAYER_LABELS) for _ in range(len(self.PLAYER_LABELS))])
        # print(player_dist)
        player_dist = (1/2, 1/2)
        super(RGSmall, self).__init__(payoff_matrices=payoff_matrix,player_frequencies=player_dist, equilibrium_tolerance=equilibrium_tolerance)

    @classmethod
    def classify(cls, params, state, tolerance):
        # p = params
        threshold = 1-tolerance
        threshold = 0.5
        send = np.where(state[0] == np.amax(state[0]))
        rec = np.where(state[1] == np.amax(state[1]))

        classification = [send[0][0], rec[0][0]]
        # print("class", classification)
        return classification
        # # if state[0][0] > threshold and state[1][0] > threshold:
        # if np.amax(state[0]) == state[0][0] and np.amax(state[1]) == state[1][0]:
        #     print("state class", state[0][0], state[0][0])
        #     # A
        #     return 0
        # # elif state[0][1] > threshold and state[1][1] > threshold:
        # elif np.amax(state[0]) == state[0][1] and np.amax(state[1]) == state[1][1]:
        #     # B
        #     print("B")
        #     return 1
        # # elif state[0][2] > threshold and state[1][2] > threshold:
        # elif np.amax(state[0]) == state[0][2] and np.amax(state[1]) == state[1][2]:
        #     # B
        #     print("AB")
        #     return 2
        # # elif state[0][3] > threshold and state[1][3] > threshold:
        # elif np.amax(state[0]) == state[0][3] and np.amax(state[1]) == state[1][3]:
        #     # B
        #     print("BA")
        #     return 3
        # else:
        #     return super(RGSmall, cls).classify(params, state, tolerance)

if __name__ == "__main__":
    x = RGSmall(0, 1, 1, 1, 0.5, 0.5)
    # print("PAY", x.senderpayoff(1))
# def senderpayoff(SPayoff):
        #     # payoffs_sender = [[[0] * len(self.EQUILIBRIA_LABELS)] * 2] * len(self.EQUILIBRIA_LABELS)
        #     payoffs_sender = [[[0 for _ in range(2)] for _ in range(4)] for _ in range(len(self.EQUILIBRIA_LABELS))]
        #     # payoffs_sender = [[0 for _ in range(len(self.EQUILIBRIA_LABELS))] for _ in range(2)]
        #     #  one matrix:
        #     k = 4
        #     # payoffs_sender= [[0 for _ in range(2)] for _ in range(len(self.EQUILIBRIA_LABELS))]
        #     for state in range(len(self.EQUILIBRIA_LABELS)):
        #         for message in range(len(self.EQUILIBRIA_LABELS)):
        #             # for strategy in range(len(self.STRATEGY_LABELS[1])):
        #                 # if state == message:
        #             payoffs_sender[state][message][0] = 4
        #             # payoffs_sender[0][0][0] = 5
        #             # payoffs_sender[state][message] = 4
        #             # payoffs_sender[0][0][message] = 2
        #             if state == message:
        #                 payoffs_sender[state][message][0] += 4 * k

        #             #     payoffs_sender[state][message][message+4] = k
        #             # else:
        #             #     payoffs_sender[state][message][message] = 2 -k
        #             #     payoffs_sender[state][message][message+4] = 2 * -k


        # #     # print(payoffs_sender)
        #     return payoffs_sender
        # def receiver_payoff(aProp, bProp, k, RPayoffacc, RPayoffrej):
        #     # WHERE IS TRUE STATE CHOSEN
        #     # payoffs_rec = [[[0 for x in range(4)] for x in range(2)] for x in range(2)]
        #     payoffs_rec = [[[0 for _ in range(2)] for _ in range(4)] for _ in range(len(self.EQUILIBRIA_LABELS))]
        #     for state in range(len(self.EQUILIBRIA_LABELS)):
        #         for message in range(len(self.EQUILIBRIA_LABELS)):
        #             if len(self.EQUILIBRIA_LABELS[state]) == 1:
        #                 if state == message:
        #                     print("hello receiver")
        #                     payoffs_rec[state][message][0] = 2
        #                 elif self.EQUILIBRIA_LABELS[state] in self.EQUILIBRIA_LABELS[message]:
        #                     print("HEYYYYY")
        #                     payoffs_rec[state][message][0] = 1
        #                     payoffs_rec[state][message][1] = 1 #???? should i??
        #                 elif state != message:
        #                     payoffs_rec[state][message][1] = 2
        #             else:
        #                 if state == message:
        #                     payoffs_rec[state][message][0]= 2
        #                 elif self.EQUILIBRIA_LABELS[message] in self.EQUILIBRIA_LABELS[state]:
        #                     payoffs_rec[state][message][0] = 1
        #                     payoffs_rec[state][1][message] = 2 #or reward 1???
        #                 elif state != message and len(self.EQUILIBRIA_LABELS[state]) > 1:
        #                     payoffs_rec[state][message][0] = 1/2
        #                     payoffs_rec[state][message][1] = 1/2
        #     return payoffs_rec

        # payoffs_receiver = receiver_payoff(aProp, bProp, k, RPayoffacc, RPayoffrej)
