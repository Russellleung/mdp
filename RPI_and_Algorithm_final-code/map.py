import numpy as np

class Map:
    def __init__(self):
        self.grid = np.zeros((201,201))

    def inMap(self, npy, npx):
        #check if map coordinate is within range
        if npy < 0 or npy > 200 or npx < 0 or npx > 200:
            return False
        else:
            return True

    def parseTargets(self, convtargets):
        #gets targets from convert function, assuming (row, col, direction)
        goals = []

        for target in convtargets:
            row = target[0]
            col = target[1]

            #update sim grid with targets
            self.grid[row][col] = 6

            #create restricted zone around target
            for i in range(51):
                for j in range(51):
                    npy = row-25 + i
                    npx = col-25 + j
                    if self.inMap(npy, npx):
                        self.grid[npy][npx] = max(5, self.grid[npy][npx])

            #create movement-restricted zone around target
            for i in range(41):
                for j in range(41):
                    npy = row-20 + i
                    npx = col-20 + j
                    if self.inMap(npy, npx):
                        self.grid[npy][npx] = max(6, self.grid[npy][npx])

            #returns goalstates that needs to be achieved
            tgtgoal = self.getGoal(target)
            goals.append(tgtgoal)
        
        return goals

    def getGoal(self, target):
        #get where we want the vehicle to position for each target
        #assumes goalstates will not fall into restricted area
        row = target[0]
        col = target[1]
        direction = target[2]

        if direction == 'n':
            self.grid[row-35][col] = 4
            return (row-35, col, 's')
        elif direction == 'e':
            self.grid[row][col+35] = 3
            return (row, col+35, 'w')
        elif direction == 's':
            self.grid[row+35][col] = 2
            return (row+35, col, 'n')
        elif direction == 'w':
            self.grid[row][col-35] = 1
            return (row, col-35, "e")
        

