import io
import numpy as np
import sys
from gym.envs.toy_text import discrete
import mdptoolbox.example

WAIT = 0
CUT = 1


class ForestEnv(discrete.DiscreteEnv):
    """
    Generate a MDP example based on a simple forest management scenario
    Reference: https://pymdptoolbox.readthedocs.io/en/latest/api/example.html#mdptoolbox.example.forest
    """

    metadata = {'render.modes': ['human', 'ansi']}

    def __init__(self, num_states=3):
        _, R = mdptoolbox.example.forest(S=num_states)
        p = 0.1  # The probability that a fire burns the forest

        nS = num_states
        nA = 2
        
        P = {}
        
        for s in range(nS):
            # P[s][a] = (prob, next_state, reward, is_done)
            P[s] = {a : [] for a in range(nA)}
            reward_on_wait = R[s, WAIT]
            reward_on_cut = R[s, CUT]
            P[s][WAIT] = [(p, 0, reward_on_wait, None), (1.0 - p, min(s + 1, nS - 1), reward_on_wait, None)]
            P[s][CUT] = [(1.0, 0, reward_on_cut, None)]

        # Initial state distribution is uniform
        isd = np.ones(nS) / nS

        # We expose the model of the environment for educational purposes
        # This should not be used in any model-free learning algorithm
        self.P = P

        super(ForestEnv, self).__init__(nS, nA, P, isd)
