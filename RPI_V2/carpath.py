# prevactions:
# 'q' = left forward
# 'w' = forward
# 'e' = right forward
# 'a' = left backward
# 's' = backward
# 'd' = right backward

from itertools import permutations
import sys
import numpy as np
import math
import time
from map import *

YDIS = 5
XDIS = 5

class Node:
    def __init__(self, row, col, direction):
        self.parent = None
        self.prevaction = 'z'
        self.row = row
        self.col = col
        self.direction = direction

        self.f = 0
        self.g = 0
        self.h = 0

    def updatef(self):
        self.f = self.g + 5*self.h # TODO: attempt heuristic value set to 5 - need to determine whether optimal path provided

    def getcoord(self):
        return (self.row, self.col)
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col and self.direction == other.direction

def manhattanDistance(cur, end):
    return abs(cur.row - end.row) + abs(cur.col - end.col)

def euclideanDistance(cur, end):
    return ((cur.row - end.row)**2 + (cur.col - end.col)**2)**0.5

def carwithinArea(row, col):
    return row > 2 and row < 38 and col > 2 and col < 38

def getnextLoc(map, node):
    nextloc = []
    checkfwd(map, node, nextloc)
    checkrev(map, node, nextloc)
    checkTPTLeft(node, nextloc)
    checkTPTRight(node, nextloc)
    '''
    checkrightfwd(node, nextloc)
    checkleftfwd(node, nextloc)
    checkrightrev(node, nextloc)
    checkleftrev(node, nextloc)
    '''
    # if (node.row % 5 != 0 or node.col % 5 != 0):
    #     adjust(node, nextloc)
    return nextloc

'''
def adjust(node, nextloc):
    if node.direction == 'n':
        nextloc.append((node.row - 1, node.col, 'n', 'W001'))
    elif node.direction == 'e':
        nextloc.append((node.row, node.col + 1, 'e', 'W001'))
    elif node.direction == 's':
        nextloc.append((node.row + 1, node.col, 's', 'W001'))
    elif node.direction == 'w':
        nextloc.append((node.row, node.col - 1, 'w', 'W001'))
'''

def checkTPTRight(node, nextloc):
    if node.prevaction[0] == 'K':
        return
    elif node.direction == 'n':
        nextloc.append((node.row, node.col, 'e', 'L'))
    elif node.direction == 'e':
        nextloc.append((node.row, node.col, 's', 'L'))
    elif node.direction == 's':
        nextloc.append((node.row, node.col, 'w', 'L'))
    elif node.direction == 'w':
        nextloc.append((node.row, node.col, 'n', 'L'))
        
        
def checkTPTLeft(node, nextloc):
    if node.prevaction[0] == 'L':
        return
    elif node.direction == 'n':
        nextloc.append((node.row, node.col, 'w', 'K'))
    elif node.direction == 'e':
        nextloc.append((node.row, node.col, 'n', 'K'))
    elif node.direction == 's':
        nextloc.append((node.row, node.col, 'e', 'K'))
    elif node.direction == 'w':
        nextloc.append((node.row, node.col, 's', 'K'))
    
def checkfwd(map, node, nextloc):
    if node.prevaction[0] in ['W', 'S']:
        return

    elif node.direction == 'n':
        for i in range(1, 38 - node.row):
            if map.grid[node.row + i][node.col] >=5:
                return
            nextloc.append((node.row + i, node.col, 'n', "W{:03d}".format(i*5)))

    elif node.direction == 'e':
        for i in range(1, 38 - node.col):
            if map.grid[node.row][node.col + i] >=5:
                return
            nextloc.append((node.row, node.col + i, 'e', "W{:03d}".format(i*5)))

    elif node.direction == 's':
        for i in range(1, node.row - 2):
            if map.grid[node.row - i][node.col] >=5:
                return
            nextloc.append((node.row - i, node.col, 's', "W{:03d}".format(i*5)))

    elif node.direction == 'w':
        for i in range(1, node.col - 2):
            if map.grid[node.row][node.col - i] >=5:
                return
            nextloc.append((node.row, node.col - i, 'w', "W{:03d}".format(i*5)))

def checkrev(map, node, nextloc):
    if node.prevaction[0] in ['W', 'S']:
        return

    elif node.direction == 'n':
        for i in range(1, node.row - 2):
            if map.grid[node.row - i][node.col] >=5:
                return
            nextloc.append((node.row - i, node.col, 'n', "S{:03d}".format(i*5)))

    elif node.direction == 'e':
        for i in range(1, node.col - 2):
            if map.grid[node.row][node.col - i] >=5:
                return
            nextloc.append((node.row, node.col - i, 'e', "S{:03d}".format(i*5)))

    elif node.direction == 's':
        for i in range(1, 38 - node.row):
            if map.grid[node.row + i][node.col] >=5:
                return
            nextloc.append((node.row + i, node.col, 's', "S{:03d}".format(i*5)))

    elif node.direction == 'w':
        for i in range(1, 38 - node.col):
            if map.grid[node.row][node.col + i] >=5:
                return
            nextloc.append((node.row, node.col + i, 'w', "S{:03d}".format(i*5)))

'''
def checkleftrev(node, nextloc): # a
    if node.prevaction == 'Q':
        return
    elif node.direction == 'n':
        nextloc.append((node.row - YDIS, node.col - XDIS, 'e', 'A'))
    elif node.direction == 'e':
        nextloc.append((node.row + XDIS, node.col - YDIS, 's', 'A'))
    elif node.direction == 's':
        nextloc.append((node.row + YDIS, node.col + XDIS, 'w', 'A'))
    elif node.direction == 'w':
        nextloc.append((node.row - XDIS, node.col + YDIS, 'n', 'A'))

def checkrightrev(node, nextloc): # d
    if node.prevaction == 'E':
        return
    elif node.direction == 'n':
        nextloc.append((node.row - YDIS, node.col + XDIS, 'w', 'D'))
    elif node.direction == 'e':
        nextloc.append((node.row - XDIS, node.col - YDIS, 'n', 'D'))
    elif node.direction == 's':
        nextloc.append((node.row + YDIS, node.col - XDIS, 'e', 'D'))
    elif node.direction == 'w':
        nextloc.append((node.row + XDIS, node.col + YDIS, 's', 'D'))

def checkleftfwd(node, nextloc): # q
    if node.prevaction == 'A':
        return
    elif node.direction == 'n':
        nextloc.append((node.row + YDIS, node.col - XDIS, 'w', 'Q'))
    elif node.direction == 'e':
        nextloc.append((node.row + XDIS, node.col + YDIS, 'n', 'Q'))
    elif node.direction == 's':
        nextloc.append((node.row - YDIS, node.col + XDIS, 'e', 'Q'))
    elif node.direction == 'w':
        nextloc.append((node.row - XDIS, node.col - YDIS, 's', 'Q'))

def checkrightfwd(node, nextloc): # e
    if node.prevaction == 'D':
        return
    elif node.direction == 'n':
        nextloc.append((node.row + YDIS, node.col + XDIS, 'e', 'E'))
    elif node.direction == 'e':
        nextloc.append((node.row - XDIS, node.col + YDIS, 's', 'E'))
    elif node.direction == 's':
        nextloc.append((node.row - YDIS, node.col - XDIS, 'w', 'E'))
    elif node.direction == 'w':
        nextloc.append((node.row + XDIS, node.col - YDIS, 'n', 'E'))
'''

def checkTurningCollision(map, currentNode, endNode):
    if (endNode[3][0] == 'W' or endNode[3][0] == 'S'): # if going forward/reverse
        return False

    if map.grid[endNode[0]][endNode[1]] == 5:
        return True
    
    return False


def getDestination(obstacle):
    direction = obstacle[2]
    if direction == 'n':
        return (obstacle[0]-20, obstacle[1], 's')
    elif direction == 's':
        return (obstacle[0]+20, obstacle[1], 'n')
    elif direction == 'e':
        return (obstacle[0], obstacle[1]+20, 'w')
    elif direction == 'w':
        return (obstacle[0], obstacle[1]-20, 'e')

# sent from android : id, direction, x, y
def convert(obstaclesFromAndroid):
    obstacles = []
    temp = obstaclesFromAndroid.split(":") # temp[1] = x temp[2] = y
    if temp[0] == "beginImgRec":
        for i in range (1, len(temp)-1):
            obstacles.append(parseCoord(temp[i]))
        return obstacles
    else:
        return

def parseCoord(obstacleString):
    temp = obstacleString.split(",")
    id = int(temp[0])
    direction = temp[1]
    x = int(temp[2])
    y = int(temp[3])
    row = 200-(10*y)-5
    col = 10*x+5
    return (row,col,direction)

def exhaustiveSearch(n,obstacles):
        start = obstacles[0]
        tempObstacles = obstacles
        obstacles = obstacles[1:]
        lenObstacles = len(obstacles)
        
        connectGraph = [[[[]] for i in range(lenObstacles)] for i in range(lenObstacles)]
        for i in range(lenObstacles):
            for j in range(lenObstacles):
                if i != j:
                    connectGraph[i][j] = getDist(obstacles[i],obstacles[j])
        
        maxBit = 1<<lenObstacles
        matrix = [[(float("inf"),[])]*lenObstacles for i in range(maxBit)]
        for i in range(lenObstacles): 
            matrix[1<<i][i] = (getDist(start,obstacles[i]), [start,obstacles[i]])
        
        for bits in range(maxBit):
            present = []
            for i in range(lenObstacles):
                if (1<<i) & bits:
                    present.append(i)
                    
            for prevLast,toAdd in permutations(present,2):
                newPathCost = matrix[bits^(1<<toAdd)][prevLast][0] + connectGraph[prevLast][toAdd]
                newPath = matrix[bits^(1<<toAdd)][prevLast][1] + [obstacles[toAdd]]
                matrix[bits][toAdd] = min(matrix[bits][toAdd],(newPathCost,newPath))

        path = []
        for node in min(matrix[-1])[1]:
            path.append(tempObstacles.index(node))
        return path


def getDist(p1,p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

'''
def bulldoze(map, start, end):
    map = 0
    startNode = Node(start[0], start[1], start[2]) # row, col, direction
    endNode = Node(end[0], end[1], end[2])

    unexploredList = []
    exploredList = []

    unexploredList.append(startNode)

    while unexploredList:
        unexploredList.sort(key=lambda x: x.f)
        currentNode = unexploredList.pop(0)
        exploredList.append(currentNode)

        if currentNode == endNode:
            print("Path found.")
            path = []
            actions = []
            direction = []
            current = currentNode
            while current.parent is not None:
                path.append(current.getcoord())
                actions.append(current.prevaction)
                direction.append(current.direction)
                current = current.parent
            return [path[::-1], actions[::-1], direction[::-1]]
        
        nextNode = []
        moves = getnextLoc(currentNode)

        for move in moves:
            nextrow = move[0]
            nextcol = move[1]
            
            if not carwithinArea(nextrow//5, nextcol//5):
                continue

            newNode = Node(nextrow, nextcol, move[2])
            newNode.prevaction = move[3]
            newNode.parent = currentNode
            nextNode.append(newNode)

        for next in nextNode:
            if len([exploredNode for exploredNode in exploredList if next == exploredNode]) > 0:
                continue

            if next.prevaction == 'W' or next.prevaction == 'S':
                next.g = currentNode.g + 5
            elif next.prevaction == 'W001':
                next.g = currentNode.g + 1
            else:
                next.g = currentNode.g + 100
            
            next.h = manhattanDistance(next, endNode)
            next.updatef()

            if len([unexploredNode for unexploredNode in unexploredList if next == unexploredNode]) > 0:
                continue

            unexploredList.append(next)
'''

def findpath(map,start,end):
    startNode = Node(start[0], start[1], start[2])
    endNode = Node(end[0], end[1], end[2])

    unexploredList = []
    exploredList = []

    unexploredList.append(startNode)

    while unexploredList:
        unexploredList.sort(key = lambda x: x.f)
        currentNode = unexploredList.pop(0)
        exploredList.append(currentNode)

        if currentNode == endNode:
            print("Path found.")
            path = []
            actions = []
            direction = []
            current = currentNode
            while current.parent is not None:
                path.append(current.getcoord())
                actions.append(current.prevaction)
                direction.append(current.direction)
                current = current.parent
            return [path[::-1], actions[::-1], direction[::-1]]

        nextNode = []
        moves = getnextLoc(map, currentNode)

        for move in moves:
            nextrow = move[0]
            nextcol = move[1]
            
            # if not carwithinArea(nextrow, nextcol):
            #     continue

            if checkTurningCollision(map, currentNode.getcoord(), move): 
                continue
            
            if map.grid[nextrow][nextcol] >= 5:
                continue

            newNode = Node(nextrow, nextcol, move[2])
            newNode.prevaction = move[3]
            newNode.parent = currentNode
            nextNode.append(newNode)
        
        for next in nextNode:
            if len([exploredNode for exploredNode in exploredList if next == exploredNode]) > 0:
                continue

            if next.prevaction == 'W' or next.prevaction == 'S':
                next.g = currentNode.g + 5
            elif next.prevaction == 'W001':
                next.g = currentNode.g + 1
            else:
                next.g = currentNode.g + 100
            
            # next.h = manhattanDistance(next, endNode)
            next.h = euclideanDistance(next, endNode)
            next.updatef()

            if len([unexploredNode for unexploredNode in unexploredList if next == unexploredNode]) > 0:
                continue

            unexploredList.append(next)
    # print(currentNode.prevaction)
    # print("Safe path not found - attempt bulldozing algorithm")
    # return bulldoze(map, start, end)

# path is coordinates
# [path[::-1], actions[::-1], direction[::-1]]
def convertToRobot(pathList): 
    instruction = []
    for i in range(len(pathList)):
        if pathList[i][0] == 'W':
            instruction.append(pathList[i])
        elif pathList[i][0] == 'S':
            instruction.append(pathList[i])
        elif pathList[i] == 'K':
            instruction.append("K090")
        elif pathList[i] == 'L':
            instruction.append("L090")
        '''
        elif pathList[i] == 'A':
            instruction.append("A090")
        elif pathList[i] == 'D':
            instruction.append("D090")
        elif pathList[i] == 'Q':
            instruction.append("Q090")
        elif pathList[i] == 'E':
            instruction.append("E090")
        '''
    return instruction

# send to android : robot, x, y, direction
# path is coordinates
# [path[::-1], actions[::-1], direction[::-1]]
def convertToAndroid(pathList):
    instruction = []
    for i in range (len(pathList[0])):
        x = int((pathList[0][i][1] - 5)/10)
        y = int((200 - 5 - pathList[0][i][0])/10)
        instruction.append(''.join('ROBOT,', str(x), ',', str(y), ',', pathList[2][i]))
    return instruction

def instToFollow(nodePath, map, destination):
    allPaths = []
    combinedPaths = []
    pathLocations = []

    for i in range(len(nodePath)-1):
        print('Moving from: ', destination[nodePath[i]], ' -> ', destination[nodePath[i+1]])
        path = findpath(map, destination[nodePath[i]], destination[nodePath[i+1]])
        print(path)
        allPaths.append(convertToRobot(path[1]))
        pathLocation = []
        for i in range(len(path[0])):
            pathLocation.append(list(path[0][i]) + [path[2][i]])
        pathLocations.append(pathLocation)
    combinedPaths.append(allPaths)
    
    return combinedPaths, pathLocations

def pathFinder(pathFromAndroid, map):
    obstacleList = pathFromAndroid
    destination = map.parseTargets(obstacleList)

    destination.insert(0,(3,3,'n')) # start, n is facing down=
    destination = [i for i in destination if i != "No goal"]
    print(destination)

    nodePath = exhaustiveSearch(len(destination), destination)
    appendedPath, appendedLocations = instToFollow(nodePath, map, destination)
    appendedPath.append(nodePath)
    return appendedPath, appendedLocations

def main():
    map = Map()
    obstacleList = [[60,60,'w'], [90,90,'n'],[170,150,'e'],[180,40,'s'],[60,145,'w'],[25,120,'s']]
    # print(map.parseTargets(obstacleList))
    map.show_grid(False)

    combinedPath, locations = pathFinder(obstacleList, map)

    # print(combinedPath)
    return
    # locate position and direction of robot 
    start = [3,3,'n']
    locations[0] = [start]+locations[0]

    start_time = time.time()

    for path in locations:
        for location in path:
            map.set_robot_pos(location)
            map.show_grid()
            print(location)
            time.sleep(1.3)
        time.sleep(2.5)

    print("Elapsed time:",time.time() - start_time)
    print('Simulation Complete!')

if __name__ == "__main__":
    main()
