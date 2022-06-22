
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

class WinnerAgent(game.Agent):

    def __init__(self, **args):
        super()
        self.numTraining= args.get('numTraining',0)
        #self.num_games = args.get('numGames',2)
        self.weights_register = []
        self.discount = 0.0
        self.epsilon = 0.4
        self.learning_rate = 0.0
        self.last_state, self.last_action = None, None
        self.score=0
        self.weights={
        'min_dist_power':8.521925468053692e+170,
        'has_power_pill':0.0,
        'has_pill':2.2371535685460698e+151,
        'num_pill':1.0364640676444163e+166,
        'min_dist_pill': 1.7000912193588016e+164,
        'num_ghosts':2.380116286652504e+166,
        'edibleGhost':1.9861045661439615e+125,
        'dist_edibleGhost':-8.500415309473229e+163,
        'dist_next_ghosts':5.956760146604153e+164,
        'bias':1.190058143326252e+166
        }


    def reward(self, state:GameState, next_state:GameState):
        pos_next= next_state.getPacmanPosition()
        pos =  state.getPacmanPosition()
        features = self.get_features(self.last_state,self.last_action)
        
        if article.ghost_pos(next_state):
            self.score = self.score - 200
        '''if features['has_pill'] == 1:
            self.score = self.score + 80'''
        action_score = next_state.getScore() - state.getScore()
        self.score= self.score + action_score

        '''eaten = np.bitwise_xor(np.array(state.getFood().data), np.array(next_state.getFood().data)).any()    # Verifica se o pacman comeu
        if eaten == True:
            self.score = self.score + 100'''
        #power = state.getCapsules() != next_state.getCapsules()    # Verifica se o pacman comeu uma power pill
        if features['has_power_pill'] == 1:
            self.score = self.score + 120
        #score = next_state.getScore() - state.getScore()           # Leva em conta a mudança do score
        score = self.score
        return score
    def q_max(self, state:GameState, next_pos):
        q_values = []

        for pos in next_pos:
            features=self.get_features(state, pos)
            q_values.append(self.approximate_q(features))
        if (len(q_values) == 0):
            return 0
        else:
            return max(q_values)

    def update_weights(self, next_state:GameState):
        legal_next = next_state.getLegalPacmanActions()
        if Directions.STOP in legal_next: legal_next.remove(Directions.STOP)
        features = self.get_features(self.last_state, self.last_action)
        Qvalues = self.approximate_q(features)      
        Qvalues_next = self.q_max(next_state,legal_next)
        r = self.reward(self.last_state, next_state)
        for feature in features.keys():
            self.weights[feature] = self.weights[feature] + self.learning_rate*(r + self.discount*Qvalues_next - Qvalues)*features[feature]

    def get_features(self, state:GameState, action):
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
            min_dis,num_pill,has_pill = article.distToNextPill(state, action)
            features['has_pill']=has_pill
            features['num_pill']=num_pill
            features['min_dist_pill']=min_dis
            min_dis,has_power= article.distToNextPowerPill(state,action)
            features['has_power_pill']=has_power
            features['min_dist_power']=min_dis
            food, dist_food, n_food, dist_nfood=article.food_or_not(state, action)
            features['num_ghosts']=n_food
            features['dist_next_ghosts']=dist_nfood
            features['edibleGhost']=food
            features['dist_edibleGhost']=dist_food
            features['bias'] = 1
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
                features=self.get_features(state,action)
                Qvalues.append(self.approximate_q(features))
            Qvalues = np.array(Qvalues)
            best=np.argmax(Qvalues)
            bestAction = legal[best]
            successor = state.generateSuccessor(0, bestAction)
            self.last_action = bestAction
            self.last_state = state
            features = self.get_features(self.last_state,self.last_action)
            #self.update_weights(successor)
            return bestAction

    def final(self, state:GameState):
        self.update_weights(state)
        game_weights.append(list(self.weights.values()))
        #df = pd.DataFrame(game_weights)
        #df.columns=self.weights.keys()
        #df.to_csv('scores.csv')
        #self.num_games = self.num_games + 1
        with open(r'./pesos.txt', 'w') as fp:
            for item in game_weights:
                fp.write("%s\n" % item)