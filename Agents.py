from pacman import GameState, Directions
import random
import numpy as np
from time import sleep

def getWeights():
    try:
        return np.loadtxt("weights.txt", dtype=np.float64)
    except OSError:
        return np.zeros(6)

def nearestFood(state:GameState):
    pos = state.getPacmanPosition()
    node = (pos[0], pos[1])

    explored = []
    exploring = [node]
    distances = [0]

    while exploring:
        current = exploring.pop(0)
        d = distances.pop(0)

        if state.hasFood(current[0], current[1]): return d

        explored.append(current)
        
        for new in [
            (current[0], current[1]+1),
            (current[0]+1, current[1]),
            (current[0], current[1]-1),
            (current[0]-1, current[1])
        ]:
            if new[0] >= state.getWalls().width or new[0]<0 or new[1] < 0 or new[1] >= state.getWalls().height:
                continue


            if state.hasWall(new[0], new[1]) or new in explored: continue

            exploring.append(new)
            distances.append(d+1)
    
    return 1

def nearestGhost(state:GameState):
    pos = state.getPacmanPosition()
    node = (pos[0], pos[1])

    explored = []
    exploring = [node]
    distances = [0]

    while exploring:
        current = exploring.pop(0)
        d = distances.pop(0)

        for ghost in state.getGhostPositions():
            if current == ghost: return d

        explored.append(current)
        
        for new in [
            (current[0], current[1]+1),
            (current[0]+1, current[1]),
            (current[0], current[1]-1),
            (current[0]-1, current[1])
        ]:
            if new[0] >= state.getWalls().width or new[0]<0 or new[1] < 0 or new[1] >= state.getWalls().height:
                continue


            if state.hasWall(new[0], new[1]) or new in explored: continue

            exploring.append(new)
            distances.append(d+1)
    
    return 1

def getDistance(state:GameState, pos, target):
    explored = []
    exploring = [pos]
    distances = [0]

    while exploring:
        current = exploring.pop(0)
        d = distances.pop(0)

        if current == target: return d

        explored.append(current)
        
        for new in [
            (current[0], current[1]+1),
            (current[0]+1, current[1]),
            (current[0], current[1]-1),
            (current[0]-1, current[1])
        ]:
            if new[0] >= state.getWalls().width or new[0]<0 or new[1] < 0 or new[1] >= state.getWalls().height:
                continue


            if state.hasWall(new[0], new[1]) or new in explored: continue

            exploring.append(new)
            distances.append(d+1)
    
    return 1

def numGhostsNsteps(state:GameState, steps):
    counter = 0

    pos = state.getPacmanPosition()
    for ghost in state.getGhostPositions():
        if getDistance(state, pos, ghost) == steps:
            counter += 1

    return counter

def getFeatures(state:GameState, action:Directions):
    features = [1,]
    nextState = state.generateSuccessor(0, action)

    features.append(1/nearestFood(nextState))
    features.append(state.getNumFood() - nextState.getNumFood())
    features.append(1/(1 + numGhostsNsteps(nextState, 1)))
    features.append(1/(1 + numGhostsNsteps(nextState, 2)))
    features.append((nextState.getScore() - state.getScore()+500)/500)
    # features.append(nearestGhost(nextState))

    return np.array(features)

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
            #print(action, getFeatures(state, action))
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