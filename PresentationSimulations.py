"""
Unittest
Return graphs
"""

from wrapper import GameDynamicsWrapper, VariedGame

from moran import Moran
from wright_fisher import WrightFisher
from replicator import Replicator

# from hawk_dove import HawkDove
from rejection_game_small import RGSmall

import unittest
from io import StringIO

import logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

class TestCase(unittest.TestCase):
    def test_single_simulation(self):
        s = GameDynamicsWrapper(RGSmall, Moran)
        s.simulate(num_gens=1000, graph=dict(options=['smallFont']))#,
        # s.simulate(num_gens=500,graph=dict(options=['area', 'largeFont']))


if __name__ == '__main__':
    unittest.main()


# loader = unittest.TestLoader()
# suite = loader.loadTestsFromTestCase(TestCase)
# runner = LogCaptureRunner(verbosity=2)
# runner.run(suite)
# if False:
#     print("HALLO")
#     def test_many_simulation(self):  # Determines which equilibria result based upon several simulations, text output
#         s = GameDynamicsWrapper(CtsDisc, WrightFisher, dynamics_kwargs=dict(selection_strength=0.3))
#         #print(s.simulate_many(num_iterations=100, num_gens=190, graph=dict(shading='redblue', options=['area', 'noLegend', 'largeFont']), start_state=state))

#     def test_wireFrame(self):  # 3d graph of equilibrium found when varying two variables
#         s = VariedGame(CostlySignaling, Moran)
#         s.vary_2params('v', (0, 5, 1), 'c', (1, 5, 1), num_iterations=1, num_gens=200)
