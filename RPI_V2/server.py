# from curses import keyname
import cv2
import imagezmq
import socket
import detection
import sys

import torch
import subprocess

from stitchImages import start_stitch

# clear_images(r'C:\Users\ASUS\Desktop\mdp\mdpv1_yolov5\runs\detect')
# clear_images(r'C:\Users\ASUS\Desktop\mdp\mdpv1_yolov5\stitchedImages\rawCaptures')

image_hub = imagezmq.ImageHub()
print("Image server started")

while True:
    rpi_name, image = image_hub.recv_image()
    print("received")
    output_dir = r'C:\Users\ASUS\Desktop\mdp\mdpv1_yolov5\imagezmq_images\image.jpg' 
    cv2.imwrite(output_dir, image)
    print("Receiving image, sending to image processing...")

    print(f"Setup complete. Using torch {torch.__version__} ({torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else 'CPU'})")
    p = subprocess.getstatusoutput("python detect.py --weights best_299.pt --save-conf --img 640 --conf 0.75 --source ./imagezmq_images") 
    output = p[1]
    with open('outputs/output_test.txt', 'w') as f:    # path to output .txt file
     f.write(output)
    message_dict = detection.process_output(path = "outputs/output_test.txt")
    

    message = None
    if detection.highest_conf(message_dict):
        message=detection.highest_conf(message_dict)[1]
    else:
        message=100
    
    

    message = str(message)
    print("message = ", message)
    message = message.encode('utf-8')
    image_hub.send_reply(message)
    print(rpi_name)
    if rpi_name == "end":
        print("end")
        break

print("start stitch")
start_stitch()

    



