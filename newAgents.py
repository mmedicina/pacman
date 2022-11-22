from pacman import GameState, Directions
import random
import numpy as np
from time import sleep
from features import getFeatures
from game import Agent

def getWeights():
    try:
        return np.loadtxt("weights.txt", dtype=np.float64)
    except OSError:
        return np.zeros(8)

class LookaheadAgent(Agent):
    def __init__(self, **args):
        self.weights = getWeights()
        self.depth = 2

    def Qvalue(self, state:GameState, action:Directions):
        return np.inner(getFeatures(state, action), self.weights)

    def Qstar(self, state:GameState):
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)

        if len(legal) == 0: return (0, Directions.STOP)

        best = (-np.inf, None)
        for action in legal:
            q = self.Qvalue(state, action)
            if q >= best[0]: best = (q, action)

        return best

    def reward(self, state:GameState, action:Directions):
        score = 0

        nextState = state.generateSuccessor(0, action)

        score += nextState.getScore() - state.getScore()
      
        return score

    def Lookahead(self, state, depth=None):
        if depth is None: depth = self.depth

        if depth == 1:
            return self.Qstar(state)

        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)

        best = (-np.inf, None)
        for action in legal:
            q = self.reward(state, action) + self.Lookahead(state.generateSuccessor(0, action), depth-1)[0]
            if q >= best[0]: best = (q, action)

        return best
    
    def getAction(self, state):
        return self.Lookahead(state)[1]