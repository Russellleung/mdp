import serial
import time
import imagezmq
#import cv2

import socket

#from imutils.video import VideoStream
from picamera import PiCamera
from picamera.array import PiRGBArray
#import STM_connection

import multiprocessing

ser=serial.Serial('/dev/ttyUSB0',115200,timeout=0.5)
# given target at (x,y) and car faces north,
# car should move until 20 cm away from the obstacle
# distance from center of car to obstacle = 5 + 20 + 15 = 40
# thus, initialize startpos at (x, y-40)

# assuming counterclockwise movement, next target position will be (x+40, y)
# car will need to do a fwdright followed by a U turn

QUARTERTURNRAD = 21
UTURNRAD = 42 #assumption
#initialize obstacle at (100,100)

def fwdtilclose():
    global ser
    #add code to make it go forward til its 20cm away from obstacle
    print('Move forward')
    stmtosend = 'w000'
    ser.write(stmtosend.encode())
    #remove once buffer is done
    time.sleep(4)
    print('Checking')
    while True:
        read = ser.read()
        readDecoded = read.decode()
        print(readDecoded)

        #receive '0' when 20 cm for stop signal
        if readDecoded == '0':
            return print("Obstacle infront")
    #wait to receive stop signal at 20cm


def moveForwardUntilObstacle():
    global ser
    #add code to make it go forward til its 20cm away from obstacle
    ser.write("C100".encode())

    while True:    
        read = ser.read()
        readDecoded = read.decode()
        print(readDecoded)

        #receive '0' when 20 cm for stop signal
        if readDecoded == 'O':
            return print("Obstacle infront")
    #wait to receive stop signal at 20cm

def execute(instlist):
    #execute instructions and wait for response when whole sequence done
    global ser
    for inst in instlist:
        print(inst)
        ser.write(inst.encode())
        time.sleep(5)

def scanimage():
    #start camera
    global sender
    global rpi_name
    time.sleep(3)
    print('Starting Camera')
    camera = PiCamera(resolution=(640, 640))
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format = "bgr")
    image = rawCapture.array
    rawCapture.truncate(0)
    #send image over to server to analyze
    print("sending image")
    reply = sender.send_image(rpi_name, image)
    print("sent")
    reply = str(reply.decode())
    print('[LOG] ImageRecognition - Message received from server: ' + reply)
    camera.close()

    #takes photo and sees if its bullseye
    if reply == 'False':
        #turn and try again
        return False
    else:
        return True
        
def move(units):
    #tell car to move x units
    if units < 0:
        #rev
        return 'S0'+ str(-units)
    else:
        #fwd
        if units < 10:
            return 'W00' + str(units)
        return 'W0' + str(units)
        
def uturn():
    #uturn left
    return 'Q180'

def turnright():
    return 'E090'

def turncalc():
    instruction = []
    #does a quarter turn followed by a uturn
    yback = (QUARTERTURNRAD + UTURNRAD) -40+16 #position to begin turn process to ensure it completes on target y
    instruction.append("S0"+str(abs(yback)))
    instruction.append(turnright())
    xforward = 40 - QUARTERTURNRAD #units the car will need to move after right turn to ensure the uturn ends on target x
    instruction.append("W0"+str(abs(xforward)))
    instruction.append(uturn())
    return instruction



#process
print('Starting process')
sender = imagezmq.ImageSender(connect_to='tcp://192.168.35.23:5555')
rpi_name = socket.gethostname()
print('Server connection established')
#Begin moving forward
execute(['q'])
moveForwardUntilObstacle()
print('Image scanning')
#Path for STM
stmlist = turncalc()
#Checks if image is bullseye, if it is execute while loop, else end
while not scanimage():
    #send the path list
    print('Executing path')
    execute(stmlist)
    moveForwardUntilObstacle()
    print('Obstacle detected')
    print('Image scanning')


#execute(['q'])
#moveForwardUntilObstacle()
#stmlist = turncalc()
#for _ in range(2):
     #send the path list
 #    print('Executing path')
  #   execute(stmlist)
  #   moveForwardUntilObstacle()
  #   print('Obstacle detected')
  #   print('Image scanning')
