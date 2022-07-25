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


from math import nan
from pacman import Directions, GameState
import random
import game
import util
import numpy as np
import article_funcs as article

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

    def __init__(self, **args):
        super()
        #object = super(ReinforcementLearningAgent, cls,**args).__new__(cls)
        self.numTraining= args.get('numTraining',0)
        self.discount = 0.9
        self.learning_rate = 0.1
        self.features = (scoreEvaluation,)
        '''object.weights={
            'has_scared_ghost':0,
            'number_scared_ghost': 0,
            'min_dist_scare_ghost':0,
            'power_pill':0,
            'has_power_pill':0,
            'has_pill':0,
            'min_dist_pill': 0,
            'num_ghosts':0,
            'dist_next_ghosts':0,
            'has_food':0,
            'min_dist_food': 0,
        }'''
        self.weights = np.random.rand(1 + len(self.features))

        #return object
    '''
    def get_features(self, state:GameState, action):
        min_dis,has_pill = article.distToNextPill(state, action)
        object.weights['has_pill']=has_pill
        object.weights['min_dist_food']=min_dis
        min_dis,has_power= article.distToNextPowerPill(state,action)
        object.weights['has_power_pill']=has_power
        object.weights['power_pill']=min_dis
        food, dist_food, n_food, dist_nfood=article.food_or_not(state, action)
        object.weights['num_ghosts']=n_food
        object.weights['dist_next_ghosts']=dist_nfood
        object.weights['has_food']=food
        object.weights['min_dist_food']=dist_food
    '''
    def reward(self, state:GameState, next_state:GameState):
        pacman_pos_next= next_state.getPacmanPosition()
        pacman_pos_current=  state.getPacmanPosition()
        eaten = np.bitwise_xor(np.array(state.getFood().data), np.array(next_state.getFood().data)).any()    # Verifica se o pacman comeu
        power = state.getCapsules() != next_state.getCapsules()    # Verifica se o pacman comeu uma power pill
        score = next_state.getScore() - state.getScore()           # Leva em conta a mudança do score
        freedom = len(next_state.getLegalPacmanActions()) - len(state.getLegalPacmanActions())    # Incentiva ir para lugares mais livres
        #_, pill =article.distToNextPill(state, state.getLegalPacmanActions())
        #if(pill!=0)
        change_pos = 1
        if pacman_pos_current == pacman_pos_next:
            change_pos= -0.5*freedom

        #print(eaten,power,change_pos,freedom)
        return 0.3*eaten + 0.2*power + change_pos + 0.2*freedom

    def feature_vector(self, state, action):
        return np.array([1] + [feature(state, action ) for feature in self.features])

    def q_value(self, state, action):
        #return np.inner(self.weights, self.feature_vector(state, action))
        q = 0
        for weight, feature in self.weights, self.feature_vector(state, action):
            #print(weight,feature)
            if weight == float("NAN") or feature == float("NAN"):
                weight = 0
                feature = 0
            q = q + weight*feature 
            if q==-float('inf'):
                q = 0
            #print(q)
        return q
    '''def update(self, state, next_state, action):
            legal = state.getLegalPacmanActions()
            q = [self.q_value(state, action) for action in legal]
            next_action, next_max_q, next_features = self.chooseActionGreedy(next_state)
            reward=self.reward(state, next_state, current_features)
            self.acumulate_reward_episode=self.acumulate_reward_episode + reward_action
            for feature_name, value_feature in current_features.items():
                self.weights[feature_name] = self.weights[feature_name]  + self.alpha * ((reward_action + (self.discount * next_max_q) - current_q) * value_feature)
    '''
    def getAction(self, state:GameState):

        legal = state.getLegalPacmanActions()

        if Directions.STOP in legal: legal.remove(Directions.STOP)

        Qvalues = [self.q_value(state, action) for action in legal]
        #print(Qvalues)
        try:
            best = random.choice(np.flatnonzero(Qvalues == np.max(Qvalues)))
            
        except:
            best = random.choice(np.flatnonzero(Qvalues))

        bestAction = legal[best]
        print('best ',bestAction)
        successor = state.generateSuccessor(0, bestAction)
        try: 
            Qmax = max([self.q_value(successor, move) for move in successor.getLegalPacmanActions()])
        except:
            Qmax = 0

        self.weights += self.learning_rate * (self.reward(state, successor) + self.discount * Qmax - Qvalues[best]) * self.feature_vector(state, bestAction)

        #print(self.feature_vector(state, bestAction))

        return bestAction
