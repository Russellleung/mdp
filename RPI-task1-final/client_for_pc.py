import socket
import time
from STM_connection import STMConnection
#from android_bluetooth import*

import serial

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
        # new code
        try:
            ser = serial.Serial('/dev/ttyUSB0',115200,timeout=0.5)
        except SerialException:
            ser = serial.Serial('/dev/ttyUSB1',115200,timeout=0.5)
        instlist = instlist[::-1]
        # stm.thread_send(instlist.pop())
        # ser.write(instlist.pop().encode())
        #prev = "X"
        while instlist:
            #time.sleep(0.1)
            #current = stm.thread_recv() #will not be x
            print(instlist)
            nextInstruction = instlist.pop()
            counter = 0 # added
            # stm.thread_send(nextInstruction)
            time.sleep(0.6) # default 0.6
            ser.write(nextInstruction.encode())
            #time.sleep(0.1) #pause after sending inst
            # current=stm.thread_recv()#should not be x
            current = ser.read().decode()
            while current != "X":
                if counter>40:
                    ser.write(nextInstruction.encode())
                    counter = 0
                print('stuck')
                time.sleep(0.2)
                # current = stm.thread_recv()
                print('Instruction on robot currently: ', current)
                current = ser.read().decode()
                counter += 1
                
            '''
            if current != prev:
                if current == "X":
                    nextInstruction = instlist.pop()
                    stm.thread_send(nextInstruction)
                    prev = current
            '''
            '''
            time.sleep(0.2)
            nextInstruction = instlist.pop()
            if (stm.thread_recv() == nextInstruction[0]):
                next
            print(nextInstruction)
            stm.thread_send(nextInstruction)
            time.sleep(0.2)
            '''
            '''
            while (stm.thread_recv() != "X"):
                pass
            '''
            '''
            if (stm.thread_recv() == nextInstruction[0]):
                while True:
                    if stm.thread_recv() == "X":
                        break
            else:
                instlist.append(nextInstruction)
            '''
        
        
        # new code
        '''
        for inst in instlist:
            stm.thread_send(inst)
            time.sleep(4)
            
            countA=0
            while True:
                ans=stm.thread_recv()
                if ans=="M":
                    break
                elif ans=="A":
                    countA+=1
                    if countA>10:
                        time.sleep(0.5)
                        break
            
            while True:
                ans=stm.thread_recv()
                if ans=="X":
                    break
            '''
        print("before scan image")
        text = PC_Comm.scanimage(PC_Comm, target,isLast)
        #return text
        return 'TARGET,' + ",".join([str(0),str(0)]) + ',' + str(text)

   

    # Function to keep scanning until target is found
    def scanimage(self, target,isLast):
        print("isLast",isLast)
        #start camera
        global sender
        global rpi_name
        time.sleep(3)
        print('Starting Camera')
        camera = PiCamera(resolution=(1280, 1280))
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



