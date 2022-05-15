from util import *
from game import *
from pacman import * 
from random import choice 
def distToNextPill(state, pos):
    if state.getNumFood() == 0: 
        return -1, -1 
    else:
        next_min = 1000000
        list_food = state.getFood()
        for i, j in enumerate(list_food):
            for ii, jj in enumerate(j):
                dst = manhattanDistance(pos,(i,jj))
                if (ii and dst) < next_min:
                    next_min = dst
                    x = i
                    y = jj
        return dst, x, y

def distToNextPowerPill(state, pos):
    min_pos = 1000000
    power_pill = state.getCapsules()
    if len(power_pill) < 1:
        return -1,-1,-1
    else:
        for pill in power_pill:
            dst = manhattanDistance(pos, pill)
            if dst < min_pos:
                min_pos = dst
                next_pos = pill
        x, y = next_pos
        return dst, x, y

def junction(state, pos, dir):
    x, y = pos
    coord_x, coord_y = dir
    distToNextJunction = 1  
    if (coord_x == 0 and coord_y == 0): 
        return -1, False 
    ghostBeforeJunction = False
    ghost = [nearestPoint(pos) for pos in state.getGhostPositions()]
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

def food_or_not(state, pos):
    food = []
    n_food = []

    for ghost_state in state.getGhostStates():
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
            dist = manhattanDistance(pos, food[i])
            dsts.append(dist)
            if dist < min_dist:
                dist_food = dist 
                food_X, food_Y = food[i]
    if len(n_food) > 0:
        dsts=[]
        min_dist = 100000
        for i in enumerate(n_food):
            dist = manhattanDistance(pos, n_food[i])
            dsts.append(dist)
            if dist < min_dist:
                dist_nfood = dist 
                n_foodX, n_foodY = n_food[i]
    return len(food), food_X, food_Y, dist_food, len(n_food), n_foodX, n_foodY, dist_nfood

