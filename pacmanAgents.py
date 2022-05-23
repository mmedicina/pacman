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


from pacman import Directions
from game import Agent
import random
import game
from pacman import GameState
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

class GreedyAgent(Agent):
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

import article_funcs as af
class ReinforcementLearningAgent(Agent):

    def __new__(cls, discount = 0.1, learning_rate=0.4):

        object = super(ReinforcementLearningAgent, cls).__new__(cls)
        object.discount = discount
        object.learning_rate = learning_rate
        object.features = (af.distToNextPill, af.distToNextPowerPill)
        object.weights = dict(zip(object.features, np.random.rand(len(object.features))))
        object.weights["bias"] = np.random.rand()

        return object

    def reward(self, state:GameState, next_state:GameState):
        eaten = any(state.getFood() - next_state.getFood())        # Verifica se o pacman comeu
        power = state.getCapsules() != next_state.getCapsules()    # Verifica se o pacman comeu uma power pill
        score = next_state.getScore() - state.getScore()           # Leva em conta a mudança do score
        freedom = next_state.getLegalPacmanActions() - state.getLegalPacmanActions()    # Incentiva ir para lugares mais livres

        return 1*eaten + 5*power + score + 0.5*freedom

    def q_value(self, state, action):
        q = self.weights["bias"]

        for name, value in self.features.items():
            q = q + (value(state, action)*self.weights[name])

        return q

    def update_weights(self, reward, best, current, state, action):

        experience = self.learning_rate * (reward + self.discount * best - current)

        for feature in self.features:
            self.weights[feature] += experience * feature(state, action)

    def getAction(self, state):

        legal = state.getLegalPacmanActions()

        if Directions.STOP in legal: legal.remove(Directions.STOP)

        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        scored = [(self.q_value(state), action) for state, action in successors]
        bestScore = max(scored)[0]
        bestActions = [successors[i] for i in range(len(scored)) if scored[i][0] == bestScore]

        choose = random.choice(bestActions)

        self.update_weights(self.reward(state, choose[0]), bestScore, self.q_value(state, choose[1]))

        return choose[1]
        
def scoreEvaluation(state):
    return state.getScore()
