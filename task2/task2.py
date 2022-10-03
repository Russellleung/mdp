# from STM_connection import STMConnection
import serial
import time
import math

# read = ser.read()
# ser.write(text.encode())

def mazeRun():
    ser=serial.Serial('/dev/ttyUSB0',115200,timeout=0.5)

    yDistance = 28 # forward distance when turning
    xDistance = 28 # side distance when turning

    obstacleLength = 10
    carLength = 30

    startOfCarToObstacle = 20 # physical dist between car to obstacle

    # command to move forward until 20cm from obstacle, store L1
    l1 = 40 # get from STM

    # take picture
    firstRight = True # TODO: get from Image Rec

    gap = 10
    firstMoveBack = (xDistance + yDistance - obstacleLength//2 - gap + yDistance)-(startOfCarToObstacle+carLength//2 + obstacleLength//2)
    
    if firstRight:
        rightOne()
    else:
        leftOne()




    #command to move forward until 20cm from obstacle, store l2


    l2=40 #get from stm

    secondRight = True # TODO: get from Image Rec
    
    secondMoveBack = xDistance+yDistance-(startOfCarToObstacle+carLength//2+obstacleLength//2)

    distanceToOrigin = 

    angleToOrigin = 90 - math.degrees(math.atan((firstMoveBack + secondMoveBack)/25))

    if secondRight:
        rightTwo()
    else:
        leftTwo()

    secondObstacleLongLength=60
    protrude = (xDistance+yDistance-secondObstacleLongLength//2)
    moveAlongSecondObstacle=secondObstacleLongLength-(secondObstacleLongLength//2-xDistance) - (yDistance-protrude)
    #command to move along second obstacle



    TotalDistToOrigin=carLength//2 + l1 + startOfCarToObstacle + obstacleLength + gap + xDistance + l2 + startOfCarToObstacle + obstacleLength//2
    accountForLaterTurns=TotalDistToOrigin-yDistance-xDistance
    #command to move straight with accountForLaterTurns distance


def rightOne():
    # cmds = ['E090', 'Q180', 'E090']
    # cmds = ['E090', 'Q135', 'E045']
    cmds = ['S005', 'E045', 'Q090', 'E045'] 
    return sendCommands(cmds)
        
def leftOne():
    # cmds = ['Q090', 'E180', 'Q090']
    # cmds = ['Q090', 'E135', 'Q045']
    cmds = ['S005', 'Q045', 'E090', 'Q045'] 
    return sendCommands(cmds)

def rightTwo(distance = 100, angle = 90):
    cmds = ['E090', 'W010', 'Q180', 'W055', 'Q090']
    # TODO: calculate angle to go back to carpark
    cmds.append({}.format())
    return sendCommands(cmds)

def leftTwo(distance = 100, angle = 90):
    cmds = ['Q090', 'W010', 'E180', 'W055', 'E090']
    # TODO: calculate angle to go back to carpark
    return sendCommands(cmds)

def sendCommands(cmds):
    cmds = cmds[::-1]
    while cmds:
        read = ser.read()
        if read.decode() == "A":
            ser.write(cmds.pop().encode())
            next
    while ser.read() != "A":
        next
    print("All commands sent")