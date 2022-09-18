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
from map import *

YDIS = 15
XDIS = 35

class Node:
    def __init__(self, row, col, direction):
        self.parent = None
        self.prevaction = None
        self.row = row
        self.col = col
        self.direction = direction

        self.h = 0
        self.g = 0
        self.f = 0

    def updatef(self):
        self.f = self.g + self.h

    def getcoord(self):
        return (self.row, self.col)
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col and self.direction == other.direction

def manhattanDistance(cur, end):
    return abs(cur.row - end.row) + abs(cur.col - end.col)

def carwithinArea(row, col):
    return row > -1 + 15 and row < 201 - 15 and col > -1 + 15 and col < 201 - 15

def getnextLoc(node):
    nextloc = []
    checkfwd(node, nextloc)
    checkrev(node, nextloc)
    checkrightfwd(node, nextloc)
    checkleftfwd(node, nextloc)
    checkrightrev(node, nextloc)
    checkleftrev(node, nextloc)
    if (node.row % 5 != 0 or node.col % 5 != 0):
        adjust(node, nextloc)
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
        nextloc.append((node.row - 5, node.col, 'n', 'w005'))
        nextloc.append((node.row - 10, node.col, 'n', 'w010'))
        nextloc.append((node.row - 15, node.col, 'n', 'w015'))
        nextloc.append((node.row - 20, node.col, 'n', 'w020'))
    elif node.direction == 'e':
        nextloc.append((node.row, node.col + 5, 'e', 'w005'))
        nextloc.append((node.row, node.col + 10, 'e', 'w010'))
        nextloc.append((node.row, node.col + 15, 'e', 'w015'))
        nextloc.append((node.row, node.col + 20, 'e', 'w020'))
    elif node.direction == 's':
        nextloc.append((node.row + 5, node.col, 's', 'w005'))
        nextloc.append((node.row + 10, node.col, 's', 'w010'))
        nextloc.append((node.row + 15, node.col, 's', 'w015'))
        nextloc.append((node.row + 20, node.col, 's', 'w020')) 
    elif node.direction == 'w':
        nextloc.append((node.row, node.col - 5, 'w', 'w005'))
        nextloc.append((node.row, node.col - 10, 'w', 'w010'))
        nextloc.append((node.row, node.col - 15, 'w', 'w015'))
        nextloc.append((node.row, node.col - 20, 'w', 'w020'))

def checkrev(node, nextloc):
    if node.prevaction == 'w':
        return
    elif node.direction == 'n':
        nextloc.append((node.row + 5, node.col, 'n', 's'))
    elif node.direction == 'e':
        nextloc.append((node.row, node.col - 5, 'e', 's'))
    elif node.direction == 's':
        nextloc.append((node.row - 5, node.col, 's', 's'))
    elif node.direction == 'w':
        nextloc.append((node.row, node.col + 5, 'w', 's'))

def checkrightfwd(node, nextloc):
    if node.prevaction == 'd':
        return
    elif node.direction == 'n':
        nextloc.append((node.row - YDIS, node.col + XDIS, 'e', 'e'))
    elif node.direction == 'e':
        nextloc.append((node.row + XDIS, node.col + YDIS, 's', 'e'))
    elif node.direction == 's':
        nextloc.append((node.row + YDIS, node.col - XDIS, 'w', 'e'))
    elif node.direction == 'w':
        nextloc.append((node.row - XDIS, node.col - YDIS, 'n', 'e'))

def checkleftfwd(node, nextloc):
    if node.prevaction == 'a':
        return
    elif node.direction == 'n':
        nextloc.append((node.row - YDIS, node.col - XDIS, 'w', 'q'))
    elif node.direction == 'e':
        nextloc.append((node.row - XDIS, node.col + YDIS, 'n', 'q'))
    elif node.direction == 's':
        nextloc.append((node.row + YDIS, node.col + XDIS, 'e', 'q'))
    elif node.direction == 'w':
        nextloc.append((node.row + XDIS, node.col - YDIS, 's', 'q'))

def checkrightrev(node, nextloc):
    if node.prevaction == 'e':
        return
    elif node.direction == 'n':
        nextloc.append((node.row + XDIS, node.col + YDIS, 'w', 'd'))
    elif node.direction == 'e':
        nextloc.append((node.row + YDIS, node.col - XDIS, 'n', 'd'))
    elif node.direction == 's':
        nextloc.append((node.row - XDIS, node.col - YDIS, 'e', 'd'))
    elif node.direction == 'w':
        nextloc.append((node.row - YDIS, node.col + XDIS, 's', 'd'))

def checkleftrev(node, nextloc):
    if node.prevaction == 'q':
        return
    elif node.direction == 'n':
        nextloc.append((node.row + XDIS, node.col - YDIS, 'e', 'a'))
    elif node.direction == 'e':
        nextloc.append((node.row - YDIS, node.col - XDIS, 's', 'a'))
    elif node.direction == 's':
        nextloc.append((node.row - XDIS, node.col + YDIS, 'w', 'a'))
    elif node.direction == 'w':
        nextloc.append((node.row + YDIS, node.col + XDIS, 'n', 'a'))

def checkTurningCollision(grid,currentNode, endNode):
    
    if (endNode[3] == 'w' or endNode[3] == 's' or endNode[3] == 'w001'): # if going forward/reverse
        return False

    if grid[endNode[0]][endNode[1]] == 5:
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
def nearestNeightbour(n,obstacles):
    path = []
    visited = [False for i in range(n)]
    visited[0] = True
    currentNodeIndex = 0
    path.append(0)
    cost = calculateCost(n,0,obstacles,visited)
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
        cost = calculateCost(n,currentNodeIndex,obstacles,visited)
        #print(cost)

    return path

def calculateCost(n,index,obstacles,visited):

    cost = [0 for i in range(n)]
    for i in range (n):
        if visited[i] == True or i == index:
            continue
        cost[i] = travelTime(obstacles[index],obstacles[i])
    return cost

def travelTime(currentNode,nextNode):
    time = (currentNode[0] - nextNode[0])**2 + (currentNode[1] - nextNode[1])**2
    return int(math.ceil(math.sqrt(time)))

def bulldoze(map, start, end):
    startNode = Node(start[0], start[1], start[2])
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
            
            if not carwithinArea(nextrow, nextcol):
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

            if checkTurningCollision(map,currentNode.getcoord(), move): #endNode.getcoord() = obstacles list #endNode.getcoord(), currentNode.getcoord(),
                continue
            
            if map[nextrow][nextcol] >= 6:
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
    print("constrained path not found - bulldozing")
    return bulldoze(map,start,end)


#path is coordinates
#[path[::-1], actions[::-1], direction[::-1]]
def convertToRobot(pathList):
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
#path is coordinates
#[path[::-1], actions[::-1], direction[::-1]]
def convertToAndroid(pathList):
    instruction = []
    for i in range (len(pathList[0])):
        x = int((pathList[0][i][1] - 5)/10)
        y = int((200 - 5 - pathList[0][i][0])/10)
        instruction.append('robot,' +str(x)+ ',' +str(y)+ ',' +pathList[2][i])
    return instruction

def instToFollow(nodePath, map, destination):
    android = []
    allPaths = []
    combinedPaths = []
    for i in range(len(nodePath)-1):
        path = findpath(map.grid, destination[nodePath[i]], destination[nodePath[i+1]])
        allPaths.append(convertToRobot(path[1]))
        android.append(convertToAndroid(path))
    combinedPaths.append(allPaths)
    combinedPaths.append(android)
    print('combined paths')

    print(combinedPaths)
    return combinedPaths  

def pathFinder(pathFromAndroid):
    map = Map()
    print(map.grid)
    obstacleList = convert(pathFromAndroid)
    print(obstacleList)
    destination = map.parseTargets(obstacleList)
    print('test 1')
    destination.insert(0,(185,15,'n'))
    print(destination)
    nodePath = nearestNeightbour(len(destination),destination)
    print(nodePath)
    appendedPath = instToFollow(nodePath, map, destination)
    appendedPath.append(nodePath)
    return appendedPath

