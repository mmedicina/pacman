from pacman import GameState, Actions
from distanceCalculator import Distancer
import util
def distancer(state:GameState):
    distance_calculator = Distancer(state.data.layout)
    distance_calculator.getMazeDistances()
    return distance_calculator
def distToNextPill(state:GameState):
    distance = distancer(state)
    pacman_pos= state.getPacmanPosition()
    pos=(float(pacman_pos[0]), float(pacman_pos[1]))
    num_food = state.getNumFood()
    has_pill = 0
    if num_food != 0: 
        next_min = 1000000
        capsules=state.getFood().asList() 
        for capsule in capsules:

                dist = distance.getDistance(pos, capsule)
                if dist < next_min and dist != 0:
                    next_min = dist
                if dist == 0:
                    has_pill = 1
        return norm_dist(state,next_min), num_food, has_pill
def norm_dist(state:GameState,dist):
    size_map = state.getWalls().width * state.getWalls().height
    return dist/size_map
def distToNextPowerPill(state:GameState):
    distance = distancer(state)
    pacman_pos= state.getPacmanPosition()
    pos=(float(pacman_pos[0]), float(pacman_pos[1]))
    has_pill = 0
    next_min = 10000000
    capsules=state.getCapsules()
    for capsule in capsules:
            dist = distance.getDistance(pos, capsule)
            if dist < next_min and dist != 0:
                next_min = dist
            if dist == 0:
                has_pill = 1
    return norm_dist(state,next_min), has_pill

def junction(state:GameState):
    pacman_pos= state.getPacmanPosition()
    ghostBeforeJunction = 0
    ghost = [util.nearestPoint(pos) for pos in state.getGhostPositions()]
    while True:
        state.hasWall(float(pacman_pos[0]) + 1.0, float(pacman_pos[1])+2.0)
        if (x + distToNextJunction * coord_x, y + distToNextJunction * coord_y) in ghost: 
            ghostBeforeJunction = True
        distToNextJunction = distToNextJunction + 1
        if (ghostBeforeJunction) == True:
            break 
        return distToNextJunction, ghostBeforeJunction

def food_or_not(state:GameState):
    distance = distancer(state)
    pacman_pos= state.getPacmanPosition()
    pos=(float(pacman_pos[0]), float(pacman_pos[1]))

    food = []
    n_food = []

    for ghost_state in state.getGhostStates():
        position = ghost_state.getPosition()
        if ghost_state.scaredTimer > 0:
            food.append(position)
        else: 
            n_food.append(position)
            
    dist_food, dist_nfood = -1, -1

    if len(food) > 0:
        dsts=[]
        min_dist = 100000
        for i in range(len(food)):
            dist = distance.getDistance(pos, food[i])
            dsts.append(dist)
            if dist < min_dist:
                dist_food = dist 
    if len(n_food) > 0:
        dsts=[]
        min_dist = 100000
        for i in range(len(n_food)):
            dist = distance.getDistance(pos, n_food[i])
            dsts.append(dist)
            if dist < min_dist:
                dist_nfood = dist 
    return len(food), norm_dist(state,dist_food), len(n_food), norm_dist(state,dist_nfood)


def ghost_pos(state:GameState):

    pos = state.getPacmanPosition()
    pacman_pos= state.getPacmanPosition()
    pos=(float(pacman_pos[0]), float(pacman_pos[1]))
    food = []
    n_food = []
    died = False
    for ghost_state in state.getGhostStates():
        position = ghost_state.getPosition()
        if ghost_state.scaredTimer > 0:
            food.append(position)
        else: 
            if position == pos:
                died = True
            n_food.append(position)
    return died 


def one_two_steps(state:GameState):
    distance = distancer(state)
    pacman_pos= state.getPacmanPosition()
    pos=(float(pacman_pos[0]), float(pacman_pos[1]))
    n_food = []
    for ghost_state in state.getGhostStates():
        position = ghost_state.getPosition()
        if ghost_state.scaredTimer <= 0:
            n_food.append(position)            
    one_step, two_step = 0, 0
    if len(n_food) > 0:
        dsts=[]
        for i in range(len(n_food)):
            dist = distance.getDistance(pos, n_food[i])
            dsts.append(dist)
            if dist ==1:
                one_step+=1
            if dist == 2:
                two_step+=1
        #print(min(dsts))
        
    else:
        return one_step, two_step,-1

    return one_step, two_step, norm_dist(state,min(dsts))

def scared_steps(state:GameState):
    distance = distancer(state)
    pacman_pos= state.getPacmanPosition()
    pos=(float(pacman_pos[0]), float(pacman_pos[1]))
    food = []
    for ghost_state in state.getGhostStates():
        position = ghost_state.getPosition()
        if ghost_state.scaredTimer > 0:
            food.append(position)            
    one_step, two_step = 0, 0
    if len(food) > 0:
        dsts=[]
        for i in range(len(food)):
            dist = distance.getDistance(pos, food[i])
            dsts.append(dist)
            if dist ==1:
                one_step+=1
            if dist == 2:
                two_step+=1
    return one_step, two_step
