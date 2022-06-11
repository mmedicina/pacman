    

import game
import util
import random
import pandas as pd
import numpy as np
from math import nan
import article_funcs as article
from pacman import Directions, GameState
def scoreEvaluation(state:GameState, action):
    return state.generateSuccessor(0, action).getScore()

weights = {
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