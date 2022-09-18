import socket
import time
from STM_connection import STMConnection
from android_bluetooth import*

from carpath import *
from map import *

import imagezmq
import cv2
from imutils.video import VideoStream
from picamera import PiCamera
from picamera.array import PiRGBArray


class PC_Comm:

    stm = 0

    # Function to connect to the PC server
    def connect_PC(self):
        # Only establish connection if available
        try:
            print('Server connection establishing with Image Server')
            global sender
            global rpi_name
            sender = imagezmq.ImageSender(connect_to='tcp://192.168.40.49:5555')
            rpi_name = socket.gethostname()
            print('Connection established with Image Server')
        except:
            print('Image server not available')
        return 

    def __init__(self, andComms):
        self.android_bluetooth = andComms

    # Function to execute each path one by one
    def execute(self, instlist, target):
        #execute instructions on STM and wait for response when whole sequence done
        stm = STMConnection()
        stm.thread_send('r030')
        count = 0
        instStr = ''

        while (count < len(instlist)):
                instStr += (instlist[count])
                count += 1
        print(instStr)
        stm.thread_send(instStr)

        counter = 0
        print('Count', count)
        while True:
                read = stm.thread_recv()
                print(read)
                print(type(read))
                try: 
                       read = int(read)
                       print(type(read))
                       if isinstance(read, int):
                               print(read)
                               counter += 1
                               print('Counter ', counter)
                except:
                       print(read)

                # Execution is finished
                if counter == count:
                       if read == 0:
                             print('finish executing')
                             break

                # In the event the instructions were erased from the STM
                elif read == 0:
                        print('Error Handling: early break')
                        newInst = ''
                        pointer = counter
                        print('ptr', pointer)
                        print('len', len(instlist))
                        while(pointer < len(instlist)):
                               newInst += (instlist[pointer])
                               pointer +=1
                               print('ptr', pointer)
                        print('Backup:')
                        print(newInst)
                        stm.thread_send(newInst)

        # Scan image
        text = PC_Comm.scanimage(PC_Comm, target)
        return text

    # Function to keep scanning until target is found
    def scanimage(self, target):
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

        try:
                reply = int(reply.decode())
        except:
                reply = 0
        print('[LOG] ImageRecognition - Message received from server: ' + str(reply))
        camera.close()

        #takes photo only when it is target
        if isinstance(reply, int):
                if reply < 41 and reply >10:
                	    #image recognized, send acknowledgement to android
                        text = 'Target,' + str(target) + ',' +  str(reply) 
                        return text
                else:
                        print('not in image id')
                        text = 'Target,' + str(target) + ',' + str(reply)
                        return text
        else:
                # continue to move for STM
                return ''

    

    def startComms(self):
        ser = PC_Comm()
        ser.connect_PC()
        time.sleep(3)
        print('Connection to RPI established')
        self.stm = STMConnection()



