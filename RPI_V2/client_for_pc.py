import socket
import time
from STM_connection import STMConnection
#from android_bluetooth import*

from carpath import *
from map import *

import imagezmq
from picamera import PiCamera
from picamera.array import PiRGBArray


class PC_Comm:

    #stm = 0

    # Function to connect to the PC server
    def connect_PC(self):
        # Only establish connection if available
        try:
            print('Server connection establishing with Image Server')
            global sender
            global rpi_name
            sender = imagezmq.ImageSender(connect_to='tcp://192.168.35.23:5555')
            rpi_name = socket.gethostname()

            print('Connection established with Image Server')
        except:
            print('Image server not available')
        return 

    # Function to execute each path one by one

    def execute(self, instlist, target,isLast):
        stm = STMConnection()
        for inst in instlist:
            stm.thread_send(inst)
            time.sleep(3)
            while False:
                if stm.thread_recv()=="A":
                    break
        print("before scan image")
        text = PC_Comm.scanimage(PC_Comm, target,isLast)
        return text

   

    # Function to keep scanning until target is found
    def scanimage(self, target,isLast):
        print("isLast",isLast)
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
        print("image captured")
        #send image over to server to analyze
        reply = sender.send_image(rpi_name, image) if isLast==False else sender.send_image("end",image)
        print("after reply")
        try:
                reply = int(reply.decode())
        except:
                reply = 0
        print('[LOG] ImageRecognition - Message received from server: ' + str(reply))
        camera.close()

        #takes photo only when it is target
        if isinstance(reply, int):
                print("target",target)
                if reply < 41 and reply >10:
                	    #image recognized, send acknowledgement to android
                        text = 'TARGET,' + ",".join([str((target[1] - 5)//10 + 1),str((target[0] - 5)//10 + 1)]) + ',' +  str(reply) 
                        return text
                else:
                        print('not in image id')
                        text = 'TARGET,' + ",".join([str((target[1] - 5)//10 + 1),str((target[0] - 5)//10 + 1)]) + ',' + str(reply)
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



