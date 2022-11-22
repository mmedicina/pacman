from pacman import GameState, Directions
import random
import numpy as np
from time import sleep
from features import getFeatures

def getWeights():
    try:
        return np.loadtxt("weights.txt", dtype=np.float64)
    except OSError:
        return np.zeros(8)

def printFeatures(state, action):
    features = getFeatures(state, action)

    for feature in features:
        print(" %.2f " % feature, end='')

    print()

class RLAgent():
    def __init__(self, **args):
        self.discount = 0.95
        self.learning_rate = 0.001
        self.epsilon = 0
        self.weights = getWeights()
        self._weights = getWeights()

    def Q(self, state:GameState, action:Directions):
        return np.inner(getFeatures(state, action), self.weights)
    
    def _Q(self, state:GameState, action:Directions):
        return np.inner(getFeatures(state, action), self._weights)

    def reward(self, state:GameState, action:Directions):
        score = 0

        nextState = state.generateSuccessor(0, action)

        score += nextState.getScore() - state.getScore()
      
        return score

    def Qstar(self, state:GameState):
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)

        if len(legal) == 0: return (0, Directions.STOP)

        best = (-np.inf, None)
        for action in legal:
            q = self.Q(state, action)
            if q >= best[0]: best = (q, action)

        return best

    def _Qstar(self, state:GameState):
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)

        if len(legal) == 0: return (0, Directions.STOP)

        best = (-np.inf, None)
        for action in legal:
            q = self._Q(state, action)
            #print(action, end='')
            #printFeatures(state, action)
            if q >= best[0]: best = (q, action)

        #print()
        #sleep(1)

        return best

    def _update(self, state:GameState, action:Directions, extra = 0):
        nextState = state.generateSuccessor(0, action)
        sample = self.reward(state, action) + self.discount * self.Qstar(nextState)[0]

        self._weights += self.learning_rate * (extra + sample - self._Q(state, action)) * getFeatures(state, action)

    def getAction(self, state:GameState):
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)

        self.epsilon *= self.discount

        if random.random() < self.epsilon: return random.choice(legal)

        q, action = self._Qstar(state)
        self._update(state, action)

        #print(state.getGhostPositions())
        #print(predictPositions(state))
        #sleep(0.3)

        return action

    def final(self, state:GameState):
        pass
        self.weights = self._weights
        np.savetxt("weights.txt", self.weights)

class TestAgent:
    def __init__(self, *args, **kwargs):
        self.weights = getWeights()

    def Q(self, state:GameState, action:Directions):
        return np.inner(getFeatures(state, action), self.weights)

    def Qstar(self, state:GameState):
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)

        if len(legal) == 0: return (0, Directions.STOP)

        best = (-np.inf, None)
        for action in legal:
            q = self.Q(state, action)
            if q >= best[0]: best = (q, action)

        return best

    def getAction(self, state:GameState):
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)
    
        q, action = self.Qstar(state)

        return action