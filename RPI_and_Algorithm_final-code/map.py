import numpy as np
import os
import copy

class Map:
    def __init__(self):
        self.grid = [[0 for i in range(41)] for i in range(41)]
        self.grid_snapshot = copy.deepcopy(self.grid)
        self.changed = False
        self.robot = [3,3,'n']

    def show_grid(self, updated = True):
        key_map = {"0": ".", # empty
               "1": "+", 
               "2": "+", 
               "3": "+",
               "4": "+",
               "5": ".",
               "6": "#",
               "7": "^",
               "8": ">",
               "9": "v",
               "10": "<",
               "11": "—",
               "12": "|"}
        format = (lambda x: key_map[str(x)])

        if updated:
            # os.system('clear') # for Mac/Linux
            os.system('cls') # for Windows
        else:
            self.grid_snapshot = copy.deepcopy(self.grid)

        for x in range(41):
            for y in range(41):
                if self.grid[x][y] == 1:
                    self.grid_snapshot[x][y+6] = 12
                    self.grid_snapshot[x-1][y+6] = 12
                    self.grid_snapshot[x+1][y+6] = 12

                elif self.grid[x][y] == 2:
                    self.grid_snapshot[x+6][y] = 11
                    self.grid_snapshot[x+6][y-1] = 11
                    self.grid_snapshot[x+6][y+1] = 11

                elif self.grid[x][y] == 3:
                    self.grid_snapshot[x][y-6] = 12
                    self.grid_snapshot[x-1][y-6] = 12
                    self.grid_snapshot[x+1][y-6] = 12

                elif self.grid[x][y] == 4:
                    self.grid_snapshot[x-6][y] = 11
                    self.grid_snapshot[x-6][y-1] = 11
                    self.grid_snapshot[x-6][y+1] = 11

        # self.grid_snapshot[]
        for s in self.grid_snapshot[::-1]:
            print(*[format(i) for i in s])

    def set_robot_pos(self, newPos):
        self.grid_snapshot = copy.deepcopy(self.grid)
        self.robot = newPos
        if newPos[2] == 'n':
            for i in range(7):
                for j in range(7):
                    self.grid_snapshot[newPos[0]+i-3][newPos[1]+j-3] = 7
        elif newPos[2] == 'e':
            for i in range(7):
                for j in range(7):
                    self.grid_snapshot[newPos[0]+i-3][newPos[1]+j-3] = 8
        elif newPos[2] == 's':
            for i in range(7):
                for j in range(7):
                    self.grid_snapshot[newPos[0]+i-3][newPos[1]+j-3] = 9
        elif newPos[2] == 'w':
            for i in range(7):
                for j in range(7):
                    self.grid_snapshot[newPos[0]+i-3][newPos[1]+j-3] = 10

    def scale_down(self, npy, npx, round=True):
        if round:
            scaled_npy = npy//5
            scaled_npx = npx//5
        else:
            scaled_npy = npy/5
            scaled_npx = npx/5
        return scaled_npy, scaled_npx

    def inMap(self, npy, npx, unscaled=True):
        #check if map coordinate is within range
        if unscaled:
            npy, npx = self.scale_down(npy, npx)
        if npy < 3 or npy > 38 or npx < 3 or npx > 38:
            return False
        else:
            return True

    def parseTargets(self, convtargets):
        # gets targets from convert function, assuming (row, col, direction)
        if self.changed == False:
            self.changed = True
        else:
            self.grid = [[0 for i in range(41)] for i in range(41)]
            self.changed = True

        goals = []

        for target in convtargets:
            row = target[0]
            col = target[1]
            row, col = self.scale_down(row, col)
            # print(row)

            # update sim grid with targets
            self.grid[row][col] = 6

            # create restricted zone around target
            for i in range(11):
                for j in range(11):
                    npy = row-5 + i
                    npx = col-5 + j
                    if self.inMap(npy, npx, unscaled = False):
                        self.grid[npy][npx] = max(5, self.grid[npy][npx])

            # create movement-restricted zone around target
            for i in range(3):
                for j in range(3):
                    npy = row-1 + i
                    npx = col-1 + j
                    if self.inMap(npy, npx, unscaled = False):
                        self.grid[npy][npx] = max(6, self.grid[npy][npx])

            # returns goalstates that needs to be achieved
            tgtgoal = self.getGoal(target)
            goals.append(tgtgoal)
        
        return goals

    def getGoal(self, target):
        # get where we want the vehicle to position for each target
        # assumes goals are not in restricted area
        row = target[0]
        col = target[1]
        direction = target[2]
        row, col = self.scale_down(row, col)

        if direction == 'n':
            if (row+7)>38:
                return ('No goal')
            self.grid[row+7][col] = 4
            return (row+7, col, 's')
        elif direction == 'e':
            if (col+7)>38:
                return ('No goal')
            self.grid[row][col+7] = 3
            return (row, col+7, 'w')
        elif direction == 's':
            if (row-7)<3:
                return ('No goal')
            self.grid[row-7][col] = 2
            return (row-7, col, 'n')
        elif direction == 'w':
            if (col-7)<3:
                return ('No goal')
            self.grid[row][col-7] = 1
            return (row, col-7, "e")

# 6 refers to target
# 5 refers to collision zone
# 4 refers to position to scan target and direction north
# 3 refers to position to scan target and direction east
# 2 refers to position to scan target and direction south
# 1 refers to position to scan target and direction west


