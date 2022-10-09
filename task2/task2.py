from client_for_pc import PC_Comm

import serial
import time
import math

def mazeRun():
	pc_comms = PC_Comm()
	pc_comms.connect_PC()
	ser = serial.Serial('/dev/ttyUSB0', 115200, timeout = 0.5)
	
	# take picture
	firstRight = pc_comms.execute() # TODO: get from Image Rec

	firstMoveBack = moveForward()

	if firstRight:
		rightOne()
	else:
		leftOne()

	secondRight = pc_comms.execute() # TODO: get from Image Rec

	secondMoveBack = moveForward()

	if secondRight:
		rightTwo(firstMoveBack, secondMoveBack)
	else:
		leftTwo(firstMoveBack, secondMoveBack)


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

def rightTwo(distance1 = 100, distance2 = 100):
	cmds = ['E090', 'W010', 'Q180', 'W055']
	
	# TODO: calculate angle to go back to carpark
	# 50 refers to the distance of robot from centre of line
	if distance2 > distance1:
		cmds.append('Q' + "{:03d}".format(90))
		cmds.append('W' + "{:03d}".format(distance2 - distance1))

		cmds.append('Q' + "{:03d}".format(round(math.degrees(math.atan((2*distance1 + 10)/50)))))
		cmds.append('W' + "{:03d}".format(round(((2*distance1 + 10)**2 + 50**2)**0.5)))
		# cmds.append('Q' + "{:03d}".format(round(math.degrees(math.atan(((2*distance1 + 10)-5)/50))) + 90))
		# cmds.append('W' + "{:03d}".format(round((((2*distance1 + 10)-5)**2 + 50**2)**0.5)))
		# cmds.append('E' + "{:03d}".format(round(math.degrees(math.atan(((2*distance1 + 10)-5)/50)))))
	else:
		distance = distance1 + distance2 + 10

		cmds.append('Q' + "{:03d}".format(round(math.degrees(math.atan(distance/50))) + 90))
		cmds.append('W' + "{:03d}".format(round((distance**2 + 50**2)**0.5)))
		# cmds.append('Q' + "{:03d}".format(round(math.degrees(math.atan((distance-5)/50))) + 90))
		# cmds.append('W' + "{:03d}".format(round(((distance-5)**2 + 50**2)**0.5)))
		# cmds.append('E' + "{:03d}".format(round(math.degrees(math.atan((distance-5)/50)))))

	return sendCommands(cmds)

def leftTwo(distance1 = 100, distance2 = 100):
	cmds = ['Q090', 'W010', 'E180', 'W055']

	# TODO: calculate angle to go back to carpark
	if distance2 > distance1:
		cmds.append('E' + "{:03d}".format(90))
		cmds.append('W' + "{:03d}".format(distance2 - distance1))

		cmds.append('E' + "{:03d}".format(round(math.degrees(math.atan((2*distance1 + 10)/50)))))
		cmds.append('W' + "{:03d}".format(round(((2*distance1 + 10)**2 + 50**2)**0.5)))
		# cmds.append('E' + "{:03d}".format(round(math.degrees(math.atan(((2*distance1 + 10)-5)/50))) + 90))
		# cmds.append('W' + "{:03d}".format(round((((2*distance1 + 10)-5)**2 + 50**2)**0.5)))
		# cmds.append('Q' + "{:03d}".format(round(math.degrees(math.atan(((2*distance1 + 10)-5)/50)))))
	else:
		distance = distance1 + distance2 + 10
		
		cmds.append('E' + "{:03d}".format(round(math.degrees(math.atan(distance/50))) + 90))
		cmds.append('W' + "{:03d}".format(round((distance**2 + 50**2)**0.5)))
		# cmds.append('E' + "{:03d}".format(round(math.degrees(math.atan((distance-5)/50))) + 90))
		# cmds.append('W' + "{:03d}".format(round(((distance-5)**2 + 50**2)**0.5)))
		# cmds.append('Q' + "{:03d}".format(round(math.degrees(math.atan((distance-5)/50)))))

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

if __name__ == "__main__":
	print('Start Maze Run')
	mazeRun()