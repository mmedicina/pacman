# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions, GameState
import random
import game
import util
import numpy as np

class LeftTurnAgent(game.Agent):
    "An agent that turns left at every opportunity"

    def getAction(self, state):
        legal = state.getLegalPacmanActions()
        current = state.getPacmanState().configuration.direction
        if current == Directions.STOP: current = Directions.NORTH
        left = Directions.LEFT[current]
        if left in legal: return left
        if current in legal: return current
        if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
        if Directions.LEFT[left] in legal: return Directions.LEFT[left]
        return Directions.STOP

class GreedyAgent(game.Agent):
    def __init__(self, evalFn="scoreEvaluation"):
        self.evaluationFunction = util.lookup(evalFn, globals())
        assert self.evaluationFunction != None

    def getAction(self, state):
        # Generate candidate actions
        legal = state.getLegalPacmanActions()

        if Directions.STOP in legal: legal.remove(Directions.STOP)

        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        scored = [(self.evaluationFunction(state), action) for state, action in successors]
        bestScore = max(scored)[0]
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        return random.choice(bestActions)

def scoreEvaluation(state:GameState, action):
    return state.generateSuccessor(0, action).getScore()


import article_funcs as af
class ReinforcementLearningAgent(game.Agent):

    def __new__(cls, discount = 0.1, learning_rate=0.001):

        object = super(ReinforcementLearningAgent, cls).__new__(cls)
        object.discount = discount
        object.learning_rate = learning_rate
        object.features = (scoreEvaluation,)
        object.weights = np.random.rand(1 + len(object.features))

        return object

    def reward(self, state:GameState, next_state:GameState):
        eaten = np.bitwise_xor(np.array(state.getFood().data), np.array(next_state.getFood().data)).any()    # Verifica se o pacman comeu
        power = state.getCapsules() != next_state.getCapsules()    # Verifica se o pacman comeu uma power pill
        score = next_state.getScore() - state.getScore()           # Leva em conta a mudança do score
        freedom = len(next_state.getLegalPacmanActions()) - len(state.getLegalPacmanActions())    # Incentiva ir para lugares mais livres

        return 0.1*eaten + power + 0.5*freedom

    def feature_vector(self, state, action):
        return np.array([1] + [feature(state, action ) for feature in self.features])

    def q_value(self, state, action):
        return np.inner(self.weights, self.feature_vector(state, action))

    def getAction(self, state:GameState):

        legal = state.getLegalPacmanActions()

        if Directions.STOP in legal: legal.remove(Directions.STOP)

        Qvalues = [self.q_value(state, action) for action in legal]

        best = random.choice(np.flatnonzero(Qvalues == np.max(Qvalues)))

        bestAction = legal[best]

        successor = state.generateSuccessor(0, bestAction)

        Qmax = max([self.q_value(successor, move) for move in successor.getLegalPacmanActions()])

        #self.weights += self.learning_rate * (self.reward(state, successor) + self.discount * Qmax - Qvalues[best]) * self.feature_vector(state, bestAction)

        print(self.feature_vector(state, bestAction))

        return bestAction
