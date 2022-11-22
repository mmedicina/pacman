from game import Actions
from pacman import GameState, Directions
import numpy as np

def nearestFood(state:GameState):
    pos = state.getPacmanPosition()
    node = (pos[0], pos[1])

    explored = []
    exploring = [node]
    distances = [0]

    while exploring:
        current = exploring.pop(0)
        d = distances.pop(0)

        if state.hasFood(current[0], current[1]): return d

        explored.append(current)

        for new in Actions.getLegalNeighbors(current, state.getWalls()):
            if state.hasWall(new[0], new[1]) or new in explored: continue

            exploring.append(new)
            distances.append(d+1)

    return 1

def getDistance(state:GameState, pos, target, cap = np.inf):
    explored = []
    exploring = [pos]
    distances = [0]

    while exploring:
        current = exploring.pop(0)
        d = distances.pop(0)

        if d > cap: return d

        if current == target: return d

        explored.append(current)

        for new in Actions.getLegalNeighbors(current, state.getWalls()):
            if state.hasWall(new[0], new[1]) or new in explored: continue

            exploring.append(new)
            distances.append(d+1)

    return 1

dir2tuple = {
    'North': ( 0,  1),
    'South': ( 0, -1),
    'East' : ( 1,  0),
    'West' : (-1,  0),
    'Stop' : ( 0,  0)
}

def predictPositions(state:GameState):
    ghostPositions = []
    pacmanPostition = state.getPacmanPosition()

    for ghost in state.getGhostStates():
        if ghost.scaredTimer > 0: continue
        position = ghost.getPosition()
        nextPositions = Actions.getLegalNeighbors(position, state.getWalls())

        bestPos = None
        best = np.inf

        for pos in nextPositions:
            distance = getDistance(state, pos, pacmanPostition, cap=4)
            if distance < best:
                best = distance
                bestPos = pos

        ghostPositions.append(bestPos)

    return ghostPositions

def predictVulnerablePositions(state:GameState):
    ghostPositions = []
    pacmanPostition = state.getPacmanPosition()

    for ghost in state.getGhostStates():
        if ghost.scaredTimer == 0: continue
        position = ghost.getPosition()
        nextPositions = Actions.getLegalNeighbors(position, state.getWalls())

        bestPos = None
        best = np.inf

        for pos in nextPositions:
            distance = getDistance(state, pos, pacmanPostition, cap=4)
            if distance < best:
                best = distance
                bestPos = pos

        ghostPositions.append(bestPos)

    return ghostPositions

def numGhosts1n2steps(state:GameState):
    pos = state.getPacmanPosition()
    node = (pos[0], pos[1])

    explored = []
    exploring = [node]
    distances = [0]
    found = [0, 0]

    while exploring:
        current = exploring.pop(0)
        d = distances.pop(0)

        if d >= 3: break

        for ghostPosition in predictPositions(state):
            if current == ghostPosition: found[d-1] += 1

        explored.append(current)
        
        for new in Actions.getLegalNeighbors(current, state.getWalls()):
            if state.hasWall(new[0], new[1]) or new in explored: continue

            exploring.append(new)
            distances.append(d+1)

    return found

def numVulnerableGhosts1n2steps(state:GameState):
    pos = state.getPacmanPosition()
    node = (pos[0], pos[1])

    explored = []
    exploring = [node]
    distances = [0]
    found = [0, 0]

    while exploring:
        current = exploring.pop(0)
        d = distances.pop(0)

        if d >= 3: break

        for ghostPosition in predictVulnerablePositions(state):
            if current == ghostPosition: found[d-1] += 1

        explored.append(current)
        
        for new in Actions.getLegalNeighbors(current, state.getWalls()):
            if state.hasWall(new[0], new[1]) or new in explored: continue

            exploring.append(new)
            distances.append(d+1)

    return found

def getFeatures(state:GameState, action:Directions):
    features = [1,]
    nextState = state.generateSuccessor(0, action)

    features.append(1/nearestFood(nextState))
    features.append(state.getNumFood() - nextState.getNumFood())

    numGhosts1step,  numGhost2step = numGhosts1n2steps(nextState)
    numVGhosts1step, numVGhosts2step = numVulnerableGhosts1n2steps(nextState)

    features.append(state.getNumAgents() - numGhosts1step - 1)
    features.append(state.getNumAgents() - numGhost2step - 1)
    features.append(numVGhosts1step)
    features.append(numVGhosts2step)
    features.append((nextState.getScore() - state.getScore() + 500)/509)

    #features.append(nearestGhost(nextState))

    return np.array(features)
