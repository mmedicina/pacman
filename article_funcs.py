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
