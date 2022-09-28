yDistance=28 #forward distance when turning
xDistance=28 #side distance when turning

obstacleLength=10
carLength=30

startOfCarToObstacle=20 #physical dist between car to obstacle



#command to move forward until 20cm from obstacle, store L1
l1=40 #get from stm

#take picture
right=True #get from image rec

gap=10
moveBack=(xDistance+yDistance-obstacleLength//2-gap+yDistance)-(startOfCarToObstacle+carLength//2+obstacleLength//2)
#command to move back
if right:
    pass
    #command to turn right 90 degrees
    #command to turn 180 degrees left
    #command to turn right
else:
    pass
    #command to turn left 90 degrees
    #command to turn 180 degrees right
    #command to turn left


#command to move forward until 20cm from obstacle, store l2
l2=40 #get from stm

#take picture
secondRight=True #get from image rec

secondMoveBack=xDistance+yDistance-(startOfCarToObstacle+carLength//2+obstacleLength//2)
#command to second move back

if secondRight:
    pass
    #command to turn 90 degrees right
    #command to turn 180 degrees left
else:
    pass
    #command to turn 90 degrees left
    #command to turn 180 degrees right


secondObstacleLongLength=60
protrude=(xDistance+yDistance-secondObstacleLongLength//2)
moveAlongSecondObstacle=secondObstacleLongLength-(secondObstacleLongLength//2-xDistance) - (yDistance-protrude)
#command to move along second obstacle



if secondRight:
    pass
    #turn left 90 degrees
else:
    pass
    #turn right 90 degrees


TotalDistToOrigin=carLength//2 + l1 + startOfCarToObstacle + obstacleLength + gap + xDistance + l2 + startOfCarToObstacle + obstacleLength//2
accountForLaterTurns=TotalDistToOrigin-yDistance-xDistance
#command to move straight with accountForLaterTurns distance



if secondRight:
    pass
    #turn left 90 degrees
    #turn right 90 degrees
else:
    pass
    #turn right 90 degrees
    #turn left 90 degrees
    




