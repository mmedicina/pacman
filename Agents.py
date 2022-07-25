from pacman import GameState, Directions
import random
import numpy as np
from time import sleep

NFEATURES = 7

def getWeights():
    try:
        return np.loadtxt("weights.txt", dtype=np.float64)
    except OSError:
        return np.zeros(NFEATURES)

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

def numGhosts1n2steps(state:GameState):
    pos = state.getPacmanPosition()
    node = (pos[0], pos[1])

    explored = []
    exploring = [node]
    distances = [0]
    found = [0, 0]

    while exploring:
        current = exploring.pop(0)
        d = distances.pop(0)

        if d >= 3: break

        for ghost in state.getGhostStates():
            if ghost.scaredTimer > 0: continue
            if current == ghost.getPosition(): found[d-1] += 1

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

    return found

def getFeatures(state:GameState, action:Directions, nFoods):
    nextState = state.generateSuccessor(0, action)
    maxDist = state.data.layout.width + state.data.layout.height

    features = [1,]
    features.append(nearestFood(nextState) / maxDist)
    features.append(5.0 * nextState.getNumFood() / nFoods)
    features.append(state.getNumFood() - nextState.getNumFood())

    numGhosts1step, numGhost2step = numGhosts1n2steps(nextState)
    features.append(1 - numGhosts1step)
    features.append(1 - numGhost2step)
    features.append((nextState.getScore() - state.getScore() + 500) / 500)
    #features.append(nearestGhost(nextState))

    return np.array(features)

class RLAgent_final():
    def __init__(self, **args):
        self.numTraining= args.get('numTraining',0)
        self.discount = 1.0
        self.learning_rate = float(args['learning_rate']) if 'learning_rate' in args.keys() else 0.001
        print(f'Learning Rate = {self.learning_rate}')
        self.epsilon = 0
        self.num_episodes = 0
        self.weights = getWeights()
        self._weights = getWeights()
        self._initialState = None
        self._nFoods = 0
        self.score_episodes_list=[]

    def registerInitialState(self, state):
        self._initialState = state
        self._nFoods = state.getNumFood()

    def Q(self, state:GameState, action:Directions):
        return np.inner(getFeatures(state, action, self._nFoods), self.weights)
    
    def _Q(self, state:GameState, action:Directions):
        return np.inner(getFeatures(state, action, self._nFoods), self._weights)
    def stopEpisode(self):
        self.num_episodes += 1
        if self.num_episodes >= self.numTraining:
            self.epsilon = 0.0    
            self.learning_rate = 0.0   

    def reward(self, state:GameState, action:Directions):
        score = 0

        nextState = state.generateSuccessor(0, action)

        score += nextState.getScore() - state.getScore()
    
        return score - 5.0 * state.getNumFood() / self._nFoods

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

        self._weights += self.learning_rate * (extra + sample - self._Q(state, action)) * getFeatures(state, action, self._nFoods)

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
        #print(self._weights,self.learning_rate,self.discount,self.epsilon)
        self.score_episodes_list.append(state.getScore())
        self.stopEpisode()
        '''if self.num_episodes > self.numTraining: 
            print(self._weights, self.epsilon, self.learning_rate)
        else:
            print('treino: ' , self._weights, self.epsilon, self.learning_rate)'''

        if self.num_episodes == self.numTraining:
            msg = 'Treinamento concluído!'
            print ('%s\n%s' % (msg,'-' * len(msg)))
            print ('\t%d jogos realizados. ' % (self.numTraining))
            print ('\t%d foi a média da pontuação durante o jogos.' % (sum(self.score_episodes_list)/self.numTraining))
        np.savetxt("weights_final.txt", self.weights)

class TestAgent:
    def __init__(self, *args, **kwargs):
        self.weights = getWeights()

    def Q(self, state:GameState, action:Directions):
        return np.inner(getFeatures(state, action, self._nFoods), self.weights)

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
