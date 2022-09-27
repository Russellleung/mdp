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

    def execute1(self, instlist, target):
        stm = STMConnection()
        for inst in instlist:
            stm.thread_send(inst)
            while True:
                if stm.thread_recv()=="Done":
                    break
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
                        text = 'TARGET,' + str(target) + ',' +  str(reply) 
                        return text
                else:
                        print('not in image id')
                        text = 'TARGET,' + str(target) + ',' + str(reply)
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



