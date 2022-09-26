import serial
import time
global ser

class STMConnection():

    def thread_recv(self):
        global ser
        ser=serial.Serial('/dev/ttyUSB0',115200,timeout=0.5)
        
        read = ser.read()
        if len(read) > 0:
            return(read.decode())

    def thread_send(self,text):
        global ser
        print("hi")
        ser=serial.Serial('/dev/ttyUSB0',115200,timeout=0.5)
        print(text, type(text))
        print(text, type(text.encode()))
        ser.write(text.encode())
        print("sent")
        time.sleep(0.5)