import time
import cv2
import imagezmq
import socket
# import receivingImgFromRpi
import sys
import io
from imutils.video import VideoStream

print('Server connection establishing with Image Server')
global sender
global rpi_name
sender = imagezmq.ImageSender(connect_to='tcp://127.0.0.1:5555')
rpi_name = socket.gethostname()
print('Connection established with Image Server')
picam = VideoStream().start()
time.sleep(2)
# image = io.open("images/sierra.jpg",'rb')
image = picam.read()
print("image read")
sender.send_image(rpi_name, image)
print("image sent")
picam.stop()