from pacman import GameState
from distanceCalculator import Distancer
import util

def distToNextPill(state:GameState, action):
    n_state = state.generateSuccessor(0, action)

    pos = n_state.getPacmanPosition()

    if n_state.getNumFood() == 0: 
        return 0, 0
    else:
        next_min = 1000000
        list_food = n_state.getFood()
        for i, j in enumerate(list_food):
            for ii, jj in enumerate(j):
                dst = util.manhattanDistance(pos,(i,jj))
                if (ii and dst) < next_min:
                    next_min = dst

        return norm_dist(state,next_min), len(list_food)
def norm_dist(state:GameState,dist):
    size_map = state.getWalls().width * state.getWalls().height
    return dist/size_map
def distToNextPowerPill(state:GameState, action):
    n_state = state.generateSuccessor(0, action)

    pos = n_state.getPacmanPosition()
    min_pos = 1000000
    power_pill = n_state.getCapsules()
    if len(power_pill) < 1:
        return 0,0
    else:
        for pill in power_pill:
            dst = util.manhattanDistance(pos, pill)
            if dst < min_pos:
                min_pos = dst
                #next_pos = pill
        return min_pos,norm_dist(state,min_pos)

def junction(state:GameState, action):
    n_state = state.generateSuccessor(0, action)

    x, y = n_state.getPacmanPosition()
    coord_x, coord_y = dir
    distToNextJunction = 1  
    if (coord_x == 0 and coord_y == 0): 
        return -1, False 
    ghostBeforeJunction = False
    ghost = [util.nearestPoint(pos) for pos in state.getGhostPositions()]
    while True:
        state.hasWall(x + distToNextJunction * coord_x, y + distToNextJunction * coord_y)
        if (x + distToNextJunction * coord_x, y + distToNextJunction * coord_y) in ghost: 
            ghostBeforeJunction = True
        distToNextJunction = distToNextJunction + 1
        if (ghostBeforeJunction) == True:
            break 
    food = []
    n_food = []

    for ghost_state in state.getGhostStates():
        position = ghost_state.getPosition()
        if ghost_state.scaredTimer > 0:
            food.append(position)
        else: 
            n_food.append(position)
        return distToNextJunction, ghostBeforeJunction

def food_or_not(state:GameState, action):

    n_state = state.generateSuccessor(0, action)

    pos = n_state.getPacmanPosition()

    food = []
    n_food = []

    for ghost_state in n_state.getGhostStates():
        position = ghost_state.getPosition()
        if ghost_state.scaredTimer > 0:
            food.append(position)
        else: 
            n_food.append(position)
            
    food_X, food_Y = -1, -1
    n_foodX, n_foodY = -1 , -1
    dist_food, dist_nfood = -1, -1

    if len(food) > 0:
        dsts=[]
        min_dist = 100000
        for i in enumerate(food):
            dist = util.manhattanDistance(pos, food[i])
            dsts.append(dist)
            if dist < min_dist:
                dist_food = dist 
                food_X, food_Y = food[i]
    if len(n_food) > 0:
        dsts=[]
        min_dist = 100000
        for i in enumerate(n_food):
            dist = util.manhattanDistance(pos, n_food[i])
            dsts.append(dist)
            if dist < min_dist:
                dist_nfood = dist 
                n_foodX, n_foodY = n_food[i]
    return len(food), norm_dist(state,dist_food), len(n_food), norm_dist(state,dist_nfood)

