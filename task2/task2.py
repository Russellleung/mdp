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

def moveForward()
	cmds = [] 
	return sendCommands(cmds)

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
	cmds = ['E090', 'W010', 'Q180', 'W055']
	# TODO: calculate angle to go back to carpark
	# 50 refers to the distance of robot from centre of line
	cmds.append('Q' + "{:03d}".format(round(math.degrees(math.atan(distance/50))) + 90))
	cmds.append('W' + "{:03d}".format(round((distance**2 + 50**2)**0.5)))
	return sendCommands(cmds)

def leftTwo(distance = 100, angle = 90):
	cmds = ['Q090', 'W010', 'E180', 'W055']
	# TODO: calculate angle to go back to carpark
	cmds.append('E' + "{:03d}".format(round(math.degrees(math.atan(distance/50))) + 90))
	cmds.append('W' + "{:03d}".format(round((distance**2 + 50**2)**0.5)))
	return sendCommands(cmds)

def sendCommands(cmds):
	cmds = cmds[::-1]
	while cmds:
		if ser.read().decode() == "A":
			time.sleep(0.6)
			ser.write(cmds.pop().encode())
			next
	while ser.read().decode() != "A":
		time.sleep(0.6)
		next
	print("All commands sent")