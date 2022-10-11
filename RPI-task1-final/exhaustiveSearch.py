from itertools import permutations
def exhaustiveSearch(start,obstacles):
        lenObstacles=len(obstacles)
        
        connectGraph=[[[[]] for i in range(lenObstacles)] for i in range(lenObstacles)]
        for i in range(lenObstacles):
            for j in range(lenObstacles):
                if i!=j:
                    connectGraph[i][j]=getDist(obstacles[i],obstacles[j])
        
        
        
        maxBit=1<<lenObstacles
        matrix=[[(float("inf"),[])]*lenObstacles for i in range(maxBit)]
        for i in range(lenObstacles): 
            matrix[1<<i][i] = (getDist(start,obstacles[i]), [start,obstacles[i]])
        
        for bits in range(maxBit):
            present=[]
            for i in range(lenObstacles):
                if (1<<i) & bits:
                    present.append(i)
                    
            for prevLast,toAdd in permutations(present,2):
                newPathCost=matrix[bits^(1<<toAdd)][prevLast][0] + connectGraph[prevLast][toAdd]
                newPath=matrix[bits^(1<<toAdd)][prevLast][1]+[obstacles[toAdd]]
                matrix[bits][toAdd]=min(matrix[bits][toAdd],(newPathCost,newPath))
               
        return min(matrix[-1])[1]


def getDist(p1,p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])


print(exhaustiveSearch([0,0],[[3,4],[5,6],[8,7],[10,11],[2,10]]))
