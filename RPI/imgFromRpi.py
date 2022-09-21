import time
#import cv2
import imagezmq
import socket
# import receivingImgFromRpi
import sys
import io
# from imutils.video import VideoStream
from picamera import PiCamera
from picamera.array import PiRGBArray

print('Server connection establishing with Image Server')
global sender
global rpi_name
sender = imagezmq.ImageSender(connect_to='tcp://192.168.35.23:5555')
rpi_name = socket.gethostname()
print('Connection established with Image Server')

# picam = VideoStream().start()
# time.sleep(2)

# TESTING WITH PICAMERA CAPTURE INSTEAD OF VideoStream()
#picam = PiCamera()
# picam.start_preview()
# time.sleep(10)
# picam.stop_preview()
#picam.resolution = (640, 480)
# output = PiRGBArray(picam)
#picam.capture('/home/rpi/image.jpg')
#image = io.open("image.jpg",'rb')
# image = io.open("images/sierra.jpg",'rb')
#print(help(picam))
#image = picam.read()
#print("image read")

camera = PiCamera(resolution=(640, 640))
rawCapture = PiRGBArray(camera)
camera.capture(rawCapture, format = "bgr")
image = rawCapture.array
rawCapture.truncate(0)
    #send image over to server to analyze
print("sending image")
reply = sender.send_image(rpi_name, image)
print("image sent")

reply = str(reply.decode())
print('[LOG] ImageRecognition - Message received from server: ' + reply)
camera.close()

#sender.send_image(rpi_name, image)
print("image sent")
#camera.stop()