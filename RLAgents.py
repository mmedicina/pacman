
import game
import util
import random
import pandas as pd
import numpy as np
from math import nan
import article_funcs as article
from pacman import Directions, GameState
game_weights =[]
def scoreEvaluation(state:GameState, action):
    return state.generateSuccessor(0, action).getScore()

class RLAgent(game.Agent):

    def __init__(self, **args):
        super()
        self.numTraining= args.get('numTraining',0)
        #self.num_games = args.get('numGames',2)
        self.weights_register = []
        self.discount = 0.8
        self.epsilon = 0.1
        self.learning_rate = 0.00001
        self.q = None
        self.action = None
        self.score=0
        self.state=None
        self.game_score=0
        self.weights={'bias':0,'min_dist_pill': 0,'score':0}
        '''    'min_dist_power':0,
        'has_power_pill':0,
        'has_pill':0,
        'num_pill':0,
        ,
        'num_ghosts':0,
        'edibleGhost':0,
        'dist_edibleGhost':0,
        'dist_next_ghosts':0,'''


    def reward(self, state:GameState, next_state:GameState):

        if state.isWin() == False:
            self.score = self.score - 1
        #self.score = self.score + next_state.getScore() - state.getScore()

        score = self.score
        return score

    def update_weights(self, features, Qvalues, Qvalues_next,r):
        for feature in features.keys():
            self.weights[feature] = self.weights[feature] + self.learning_rate*(r + self.discount*Qvalues_next - Qvalues)*features[feature]
    def get_features(self, state:GameState):
        features={}
        '''
        'min_dist_power':0,
        'has_power_pill':0,
        'has_pill':0,
        'num_pill':0,
        'min_dist_pill': 0,
        'num_ghosts':0,
        'edibleGhost':0,
        'dist_edibleGhost':0,
        'dist_next_ghosts':0,
        'bias':0
        '''
        if state != None:
            if state.isWin() == True:
                min_dis=0
            else:
                min_dis,num_pill,has_pill = article.distToNextPill(state)
            features['min_dist_pill']=min_dis
            '''features['has_pill']=has_pill
            features['num_pill']=num_pill
            features['min_dist_pill']=min_dis
            min_dis,has_power= article.distToNextPowerPill(state,action)
            features['has_power_pill']=has_power
            features['min_dist_power']=min_dis
            food, dist_food, n_food, dist_nfood=article.food_or_not(state, action)
            features['num_ghosts']=n_food
            features['dist_next_ghosts']=dist_nfood
            features['edibleGhost']=food
            features['dist_edibleGhost']=dist_food  '''
            features['bias'] = 1
            features['score'] = state.getScore() - self.game_score
        return features
    
    def approximate_q(self,features):
        q_values=0
        for item in self.weights.keys():
            if item in features.keys():
                q_values = q_values + self.weights[item]*features[item]
        return q_values
    def getAction(self, state:GameState):
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)
        if len(legal)==0:
            return None 
        if self.epsilon > random.random():
            return random.choice(legal)
        else:
            Qvalues = []
            for action in legal:
                features=self.get_features(state.generateSuccessor(0, action))
                Qvalues.append(self.approximate_q(features))
            Qvalues = np.array(Qvalues)
            best=np.argmax(Qvalues)
            bestAction = legal[best]
            successor = state.generateSuccessor(0, bestAction)
            q_current=self.approximate_q(features)
            q_next=max(Qvalues)
            features = self.get_features(state)
            self.score = self.reward(state, successor)
            self.update_weights(features,q_current,q_next,self.score)
            self.q = q_next
            self.game_score = state.getScore()
            self.action = bestAction
            self.state = successor
            return bestAction
    def final(self, state:GameState):
        if state.isWin() == True:
            self.score = self.score + 40
        else: 
            self.score = self.score - 20
        features = self.get_features(self.state)
        self.update_weights(features,self.q,0,self.score)
        game_weights.append(list(self.weights.values()))
        with open(r'./pesos.txt', 'w') as fp:
            for item in game_weights:
                fp.write("%s\n" % item)
