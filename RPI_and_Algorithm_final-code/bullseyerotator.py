import serial
import time
import imagezmq
import cv2

import socket

from imutils.video import VideoStream
from picamera import PiCamera
from picamera.array import PiRGBArray

import multiprocessing

ser=serial.Serial('/dev/ttyUSB0',115200,timeout=0.5)
# given target at (x,y) and car faces north,
# car should move until 20 cm away from the obstacle
# distance from center of car to obstacle = 5 + 20 + 15 = 40
# thus, initialize startpos at (x, y-40)

# assuming counterclockwise movement, next target position will be (x+40, y)
# car will need to do a fwdright followed by a U turn

QUARTERTURNRAD = 25
UTURNRAD = 50 #assumption
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

def execute(instlist):
    #execute instructions and wait for response when whole sequence done
    global ser
    count = 0
    # Instructions to receive:
    #first = 's035'
    #second = 'e090'
    #third = 'w015'
    #forth = 'q180'
    for inst in instlist:
        ser.write(inst.encode())
        time.sleep(10)




    instStr = ''
    while (count < len(instlist)):
        instStr += (instlist[count])
        count += 1
    #instStr="".join(instlist)
    ser.write(instStr.encode())
    time.sleep(20)
    print('first 20 seconds')
    return

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
    reply = sender.send_image(rpi_name, image)

    reply = str(reply.decode())
    print('[LOG] ImageRecognition - Message received from server: ' + reply)
    camera.close()

    #takes photo and sees if its bullseye
    if reply == 'Go':
        #turn and try again
        return False
    else:
        return True
        
def move(units):
    #tell car to move x units
    if units < 0:
        #rev
        return 's0'+ str(-units)
    else:
        #fwd
        if units < 10:
            return 'w00' + str(units)
        return 'w0' + str(units)
        
def uturn():
    #uturn left
    return 'q180'

def turnright():
    return 'e090'

def turncalc():
    instruction = []
    #does a quarter turn followed by a uturn
    yback = 40 + 10 - (QUARTERTURNRAD + UTURNRAD) #position to begin turn process to ensure it completes on target y
    instruction.append(move(yback))
    instruction.append(turnright())
    xforward = 40 - QUARTERTURNRAD #units the car will need to move after right turn to ensure the uturn ends on target x
    instruction.append(move(xforward))
    instruction.append(uturn())
    return instruction

#process
print('Starting process')
sender = imagezmq.ImageSender(connect_to='tcp://192.168.40.48:5555')
rpi_name = socket.gethostname()
print('Server connection established')
#Begin moving forward
fwdtilclose()
print('Image scanning')
#Path for STM
stmlist = turncalc()
#Checks if image is bullseye, if it is execute while loop, else end
while not scanimage():
    #send the path list
    print('Executing path')
    execute(stmlist)
    #wait for proces to finish
    time.sleep(4)
    #move forward till 20cm
    fwdtilclose()
    print('Obstacle detected')
    print('Image scanning')
