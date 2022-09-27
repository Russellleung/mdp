# prevactions:
# 'q' = left forward
# 'w' = forward
# 'e' = right forward
# 'a' = left backward
# 's' = backward
# 'd' = right backward

import sys
import numpy as np
import math
import time
from map import *

YDIS = 7
XDIS = 3

class Node:
    def __init__(self, row, col, direction):
        self.parent = None
        self.prevaction = None
        self.row = row
        self.col = col
        self.direction = direction

        self.f = 0
        self.g = 0
        self.h = 0

    def updatef(self):
        self.f = self.g + 1.2*self.h # TODO: attempt heuristic value set to 1.2 - need to determine whether optimal path provided

    def getcoord(self):
        return (self.row, self.col)
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col and self.direction == other.direction

def manhattanDistance(cur, end):
    return abs(cur.row - end.row) + abs(cur.col - end.col)

def carwithinArea(row, col):
    return row > 2 and row < 38 and col > 2 and col < 38
    # return row > -1 + 15 and row < 201 - 15 and col > -1 + 15 and col < 201 - 15

def getnextLoc(node):
    nextloc = []
    checkfwd(node, nextloc)
    checkrev(node, nextloc)
    checkrightfwd(node, nextloc)
    checkleftfwd(node, nextloc)
    checkrightrev(node, nextloc)
    checkleftrev(node, nextloc)
    # if (node.row % 5 != 0 or node.col % 5 != 0):
    #     adjust(node, nextloc)
    return nextloc

def adjust(node, nextloc):
    if node.direction == 'n':
        nextloc.append((node.row - 1, node.col, 'n', 'w001'))
    elif node.direction == 'e':
        nextloc.append((node.row, node.col + 1, 'e', 'w001'))
    elif node.direction == 's':
        nextloc.append((node.row + 1, node.col, 's', 'w001')) 
    elif node.direction == 'w':
        nextloc.append((node.row, node.col - 1, 'w', 'w001'))  

def checkfwd(node, nextloc):
    if node.prevaction == 's':
        return
    elif node.direction == 'n':
        nextloc.append((node.row + 1, node.col, 'n', 'w005'))
        nextloc.append((node.row + 2, node.col, 'n', 'w010'))
        nextloc.append((node.row + 3, node.col, 'n', 'w015'))
        nextloc.append((node.row + 4, node.col, 'n', 'w020'))
        nextloc.append((node.row + 5, node.col, 'n', 'w025'))
        nextloc.append((node.row + 6, node.col, 'n', 'w030'))
        nextloc.append((node.row + 7, node.col, 'n', 'w035'))
        nextloc.append((node.row + 8, node.col, 'n', 'w040'))
    elif node.direction == 'e':
        nextloc.append((node.row, node.col + 1, 'e', 'w005'))
        nextloc.append((node.row, node.col + 2, 'e', 'w010'))
        nextloc.append((node.row, node.col + 3, 'e', 'w015'))
        nextloc.append((node.row, node.col + 4, 'e', 'w020'))
        nextloc.append((node.row, node.col + 5, 'e', 'w025'))
        nextloc.append((node.row, node.col + 6, 'e', 'w030'))
        nextloc.append((node.row, node.col + 7, 'e', 'w035'))
        nextloc.append((node.row, node.col + 8, 'e', 'w040'))
    elif node.direction == 's':
        nextloc.append((node.row - 1, node.col, 's', 'w005'))
        nextloc.append((node.row - 2, node.col, 's', 'w010'))
        nextloc.append((node.row - 3, node.col, 's', 'w015'))
        nextloc.append((node.row - 4, node.col, 's', 'w020')) 
        nextloc.append((node.row - 5, node.col, 's', 'w025'))
        nextloc.append((node.row - 6, node.col, 's', 'w030'))
        nextloc.append((node.row - 7, node.col, 's', 'w035'))
        nextloc.append((node.row - 8, node.col, 's', 'w040')) 
    elif node.direction == 'w':
        nextloc.append((node.row, node.col - 1, 'w', 'w005'))
        nextloc.append((node.row, node.col - 2, 'w', 'w010'))
        nextloc.append((node.row, node.col - 3, 'w', 'w015'))
        nextloc.append((node.row, node.col - 4, 'w', 'w020'))
        nextloc.append((node.row, node.col - 5, 'w', 'w025'))
        nextloc.append((node.row, node.col - 6, 'w', 'w030'))
        nextloc.append((node.row, node.col - 7, 'w', 'w035'))
        nextloc.append((node.row, node.col - 8, 'w', 'w040'))

def checkrev(node, nextloc):
    if node.prevaction == 'w':
        return
    elif node.direction == 'n':
        nextloc.append((node.row - 1, node.col, 'n', 's'))
        nextloc.append((node.row - 2, node.col, 'n', 's'))
        nextloc.append((node.row - 3, node.col, 'n', 's'))
        nextloc.append((node.row - 4, node.col, 'n', 's'))
        nextloc.append((node.row - 5, node.col, 'n', 's'))
        nextloc.append((node.row - 6, node.col, 'n', 's'))
        nextloc.append((node.row - 7, node.col, 'n', 's'))
        nextloc.append((node.row - 8, node.col, 'n', 's'))
    elif node.direction == 'e':
        nextloc.append((node.row, node.col - 1, 'e', 's'))
        nextloc.append((node.row, node.col - 2, 'e', 's'))
        nextloc.append((node.row, node.col - 3, 'e', 's'))
        nextloc.append((node.row, node.col - 4, 'e', 's'))
        nextloc.append((node.row, node.col - 5, 'e', 's'))
        nextloc.append((node.row, node.col - 6, 'e', 's'))
        nextloc.append((node.row, node.col - 7, 'e', 's'))
        nextloc.append((node.row, node.col - 8, 'e', 's'))
    elif node.direction == 's':
        nextloc.append((node.row + 1, node.col, 's', 's'))
        nextloc.append((node.row + 2, node.col, 's', 's'))
        nextloc.append((node.row + 3, node.col, 's', 's'))
        nextloc.append((node.row + 4, node.col, 's', 's'))
        nextloc.append((node.row + 5, node.col, 's', 's'))
        nextloc.append((node.row + 6, node.col, 's', 's'))
        nextloc.append((node.row + 7, node.col, 's', 's'))
        nextloc.append((node.row + 8, node.col, 's', 's'))
    elif node.direction == 'w':
        nextloc.append((node.row, node.col + 1, 'w', 's'))
        nextloc.append((node.row, node.col + 2, 'w', 's'))
        nextloc.append((node.row, node.col + 3, 'w', 's'))
        nextloc.append((node.row, node.col + 4, 'w', 's'))
        nextloc.append((node.row, node.col + 5, 'w', 's'))
        nextloc.append((node.row, node.col + 6, 'w', 's'))
        nextloc.append((node.row, node.col + 7, 'w', 's'))
        nextloc.append((node.row, node.col + 8, 'w', 's'))

def checkleftrev(node, nextloc): # a
    if node.prevaction == 'q':
        return
    elif node.direction == 'n':
        nextloc.append((node.row - YDIS, node.col - XDIS, 'e', 'a'))
    elif node.direction == 'e':
        nextloc.append((node.row + XDIS, node.col - YDIS, 's', 'a'))
    elif node.direction == 's':
        nextloc.append((node.row + YDIS, node.col + XDIS, 'w', 'a'))
    elif node.direction == 'w':
        nextloc.append((node.row - XDIS, node.col + YDIS, 'n', 'a'))

def checkrightrev(node, nextloc): # d
    if node.prevaction == 'e':
        return
    elif node.direction == 'n':
        nextloc.append((node.row - YDIS, node.col + XDIS, 'w', 'd'))
    elif node.direction == 'e':
        nextloc.append((node.row - XDIS, node.col - YDIS, 'n', 'd'))
    elif node.direction == 's':
        nextloc.append((node.row + YDIS, node.col - XDIS, 'e', 'd'))
    elif node.direction == 'w':
        nextloc.append((node.row + XDIS, node.col + YDIS, 's', 'd'))

def checkleftfwd(node, nextloc): # q
    if node.prevaction == 'a':
        return
    elif node.direction == 'n':
        nextloc.append((node.row + YDIS, node.col - XDIS, 'w', 'q'))
    elif node.direction == 'e':
        nextloc.append((node.row + XDIS, node.col + YDIS, 'n', 'q'))
    elif node.direction == 's':
        nextloc.append((node.row - YDIS, node.col + XDIS, 'e', 'q'))
    elif node.direction == 'w':
        nextloc.append((node.row - XDIS, node.col - YDIS, 's', 'q'))

def checkrightfwd(node, nextloc): # e
    if node.prevaction == 'd':
        return
    elif node.direction == 'n':
        nextloc.append((node.row + YDIS, node.col + XDIS, 'e', 'e'))
    elif node.direction == 'e':
        nextloc.append((node.row - XDIS, node.col + YDIS, 's', 'e'))
    elif node.direction == 's':
        nextloc.append((node.row - YDIS, node.col - XDIS, 'w', 'e'))
    elif node.direction == 'w':
        nextloc.append((node.row + XDIS, node.col - YDIS, 'n', 'e'))

def checkTurningCollision(map, currentNode, endNode):
    if (endNode[3] == 'w' or endNode[3] == 's' or endNode[3] == 'w001'): # if going forward/reverse
        return False

    if map.grid[endNode[0]][endNode[1]] == 5:
        return True
    
    return False

def getDestination(obstacle):

    if obstacle[2] == 'n':
        return (obstacle[0]-20,obstacle[1],'s')
    elif obstacle[2] == 's':
        return (obstacle[0]+20,obstacle[1],'n')
    elif obstacle[2] == 'e':
        return (obstacle[0],obstacle[1]+20,'w')
    elif obstacle[2] == 'w':
        return (obstacle[0],obstacle[1]-20,'e')

# sent from android : id, direction, x, y
def convert(obstaclesFromAndroid):
    obstacles = []
    temp = obstaclesFromAndroid.split(":") # temp[1] = x temp[2] = y
    if temp[0] == "beginImgRec":
        for i in range (1,len(temp)-1):
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

# find path to visit 
def nearestNeightbour(n, obstacles):
    path = []
    visited = [False for i in range(n)]
    visited[0] = True
    currentNodeIndex = 0
    path.append(0)
    cost = calculateCost(n, 0, obstacles, visited)
    #print(cost)
    for i in range (n-1):
        closestDist = 9999
        closestDistIndex = 0
        for i in range(len(cost)):
            if visited[i] == True:
                continue
            if cost[i] < closestDist:
                closestDist = cost[i]
                closestDistIndex = i
        
        path.append(closestDistIndex)
        visited[closestDistIndex] = True
        currentNodeIndex = closestDistIndex
        cost = calculateCost(n, currentNodeIndex, obstacles, visited)

    print(path)
    return path

def calculateCost(n, index, obstacles, visited):
    cost = [0 for i in range(n)]
    for i in range (n):
        if visited[i] == True or i == index:
            continue
        cost[i] = travelTime(obstacles[index], obstacles[i])
    return cost

def travelTime(currentNode, nextNode):
    time = (currentNode[0] - nextNode[0])**2 + (currentNode[1] - nextNode[1])**2
    return int(math.ceil(math.sqrt(time)))

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

            if next.prevaction == 'w' or next.prevaction == 's':
                next.g = currentNode.g + 5
            elif next.prevaction == 'w001':
                next.g = currentNode.g + 1
            else:
                next.g = currentNode.g + 100
            
            next.h = manhattanDistance(next, endNode)
            next.updatef()

            if len([unexploredNode for unexploredNode in unexploredList if next == unexploredNode]) > 0:
                continue

            unexploredList.append(next)

def findpath(map,start,end):
    startNode = Node(start[0], start[1], start[2])
    endNode = Node(end[0], end[1], end[2])

    unexploredList = []
    exploredList = []

    unexploredList.append(startNode)

    while unexploredList:
        # print(unexploredList[-1].prevaction, 'XY')
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
            
            if not carwithinArea(nextrow, nextcol):
                continue

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

            if next.prevaction == 'w' or next.prevaction == 's':
                next.g = currentNode.g + 5
            elif next.prevaction == 'w001':
                next.g = currentNode.g + 1
            else:
                next.g = currentNode.g + 100
            
            next.h = manhattanDistance(next, endNode)
            next.updatef()

            if len([unexploredNode for unexploredNode in unexploredList if next == unexploredNode]) > 0:
                continue

            unexploredList.append(next)
    print(currentNode.prevaction)
    print("Safe path not found - attempt bulldozing algorithm")
    return bulldoze(map, start, end)


# path is coordinates
# [path[::-1], actions[::-1], direction[::-1]]
def convertToRobot(pathList): # TODO: what are our admissible UART instructions
    instruction = []
    for i in range (len(pathList)):
        if pathList[i][:1] == 'w':
            instruction.append(pathList[i])
        elif pathList[i] == 's':
            instruction.append("s005")
        elif pathList[i] == 'a':
            instruction.append("a090")
        elif pathList[i] == 'd':
            instruction.append("d090")
        elif pathList[i] == 'q':
            instruction.append("q090")
        elif pathList[i] == 'e':
            instruction.append("e090")
    return instruction

# send to android : robot, x, y, direction
# path is coordinates
# [path[::-1], actions[::-1], direction[::-1]]
def convertToAndroid(pathList):
    instruction = []
    for i in range (len(pathList[0])):
        x = int((pathList[0][i][1] - 5)/10)
        y = int((200 - 5 - pathList[0][i][0])/10)
        instruction.append('robot,' +str(x)+ ',' +str(y)+ ',' +pathList[2][i])
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
            pathLocation += [list(path[0][i]) + [path[2][i]]]
        pathLocations += [pathLocation]
    combinedPaths.append(allPaths)
    
    return combinedPaths, pathLocations

def pathFinder(pathFromAndroid, map):
    obstacleList = pathFromAndroid
    destination = map.parseTargets(obstacleList)

    destination.insert(0,(3,3,'n')) # start, n is facing down

    destination = [i for i in destination if i != "No goal"]
    print(destination)

    nodePath = nearestNeightbour(len(destination), destination)
    appendedPath, appendedLocations = instToFollow(nodePath, map, destination)
    appendedPath.append(nodePath)
    return appendedPath, appendedLocations

def main():
    map = Map()
    obstacleList = [[60,60,'n'],[170,100,'e'],[180,40,'s'],[60,145,'n'],[25,120,'s']]
    print(map.parseTargets(obstacleList))
    map.show_grid(False)

    combinedPath, locations = pathFinder(obstacleList, map)

    print(locations)
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

    print("Elapsed time:",time.time()-start_time)
    print('Simulation Complete!')


if __name__ == "__main__":
    main()