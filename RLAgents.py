
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

class RLAgent():

    def __init__(self, learning_rate = 0.000001, epsilon=0.3, discount=0.7,**args):
        #super()
        self.numTraining= args.get('numTraining',0)
        self.num_episodes = 0
        self.learning_rate = float(learning_rate)
        self.discount = float(discount)
        self.epsilon=float(epsilon)
        self.weights_register = []
        self.q = None
        self.action = None
        self.score=0
        self.state=None
        self.game_score=0
        self.weights={
            'min_dist_pill': 0,
            'bias':0,
            'score':0,
            '1_step':0,
            '2_step':0,
            'has_pill':0,
            '1_scared':0,
            '2_scared':0,
            'dist_ghost':0}
        self.score_episodes_list=[]
    
    def stopEpisode(self):
        self.num_episodes += 1
        if self.num_episodes >= self.numTraining:
            self.epsilon = 0.0    
            self.learning_rate = 0.0     

    def reward(self, state:GameState, next_state:GameState):

        if state.isWin() == False:
            self.score = self.score - 1
            _,_,has_pill = article.distToNextPill(state)
            if has_pill == 1:
                self.score = self.score + 3
        if self.state != None:
            pos= state.getPacmanPosition()
            pos=(float(pos[0]), float(pos[1]))

            last_pos=self.state.getPacmanPosition()
            last_pos=(float(last_pos[0]), float(last_pos[1]))
            if last_pos == pos:
                self.score = self.score - 10
        return self.score

    def update_weights(self, features, Qvalues, Qvalues_next,r):
        for feature in features.keys():
            self.weights[feature] = self.weights[feature] + self.learning_rate*(r + self.discount*Qvalues_next - Qvalues)*features[feature]
    def get_features(self, state:GameState):
        features={}
        if state != None:
            if state.isWin() == True:
                min_dis=0
                has_pill = 1
                num_pill = 0
            else:
                min_dis,num_pill,has_pill = article.distToNextPill(state)
            features['min_dist_pill']=min_dis
            features['1_step'],features['2_step'],features['dist_ghost']=article.one_two_steps(state)
            features['1_scared'],features['2_scared']=article.scared_steps(state)
            features['bias'] = 1
            features['has_pill']=has_pill
            features['score'] = state.getScore() - self.game_score
        return features
    
    def approximate_q(self,features):
        q_values=0.0
        for item in self.weights.keys():
            if item in features.keys():
                q_values = q_values + self.weights[item]*features[item]
        return q_values
    def getAction(self, state:GameState):
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)
        if len(legal)==0:
            return None 
        if (util.flipCoin(self.epsilon)):
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

    def registerInitialState(self,state:GameState):
        self.state = None
        self.action = None
        if self.num_episodes == 0:
            print('Começando o treinamento. Serão realizados %d jogos' % (self.numTraining))

    def final(self, state:GameState):
        if state.isWin() == True:
            self.score = self.score + 40
        else: 
            self.score = self.score - 120
        features = self.get_features(self.state)
        self.update_weights(features,self.q,0,self.score)
        game_weights.append(list(self.weights.values()))
        self.score_episodes_list.append(state.getScore())
        self.stopEpisode()
        if self.num_episodes % 100 == 99: 
            print(self.weights, self.epsilon, self.learning_rate)
        if self.num_episodes == self.numTraining:
            msg = 'Treinamento concluído!'
            print ('%s\n%s' % (msg,'-' * len(msg)))
            print ('\t%d jogos realizados. ' % (self.numTraining))
            print ('\t%d foi a média da pontuação durante o jogos.' % (sum(self.score_episodes_list)/self.numTraining))
            print('-----------------------------')
            print(self.weights)
            print('-----------------------------')
            #df=pd.DataFrame(self.score_episodes_list,columns=['scores'])
            #df.to_csv('./scores.csv',index=False)

        if self.num_episodes < self.numTraining:
            print(self.weights)

