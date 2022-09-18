import cv2
import imagezmq
import socket
# import receivingImgFromRpi
import sys

image_hub = imagezmq.ImageHub()
print("Image server started")

while True:
    rpi_name, image = image_hub.recv_image()
    if rpi_name == "done":
        sys.exit(0)
    print("received")
    output_dir = r'/Users/russellleung/Downloads/Image_Recognition_final-code/receivedImages/image.jpg' 
    cv2.imwrite(output_dir, image)
    print("Receiving image, sending to image processing...")
    # message = receivingImgFromRpi.main()
    # if message is None:
    #     message = "No"
    # message = message.encode('utf-8')
    #image_hub.send_reply(message)
    image_hub.send_reply("received".encode('utf-8'))