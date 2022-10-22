
from client_for_pc import PC_Comm
from STM_connection import STMConnection

# from carpath import *
import socket
import time
import bluetooth
import os
import platform

from carpath import pathFinder
from map import Map

from task2 import mazeRun

class bluetoothAndroid:

    # Address of android tablet
    addr="6C:2F:8A:38:0E:AA"

    # Function for sending to android
    def write_to_android(self, text, client_sock):
        print(text, type(text))

        try:
            client_sock.send(text)
        except Exception as e:
            # displayed on android
            print(f'[write to RPI ERROR] {str(e)}')
            raise e

    def __init__(self):
        self.sock = None
        self.isConnected = False
        self.threadListening = False
        #self.pc_comms = PC_Comm()

    # Function for connecting to android
    def connect_android(self):
        addr = "6C:2F:8A:38:0E:AA"
        stm = STMConnection()
        print("stm connected")
        #a = 'p'
        #stm.thread_send(a)
        # stm.thread_send('W020')
        os.system('sudo chmod o+rwx /var/run/sdp')
        os.system('sudo hciconfig hci0 piscan')
        print('hci0')
        server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        port = 1

        # Bind bluetooth to port 1
        server_sock.bind(("", port))
        print('bind')
        server_sock.listen(1)
        print('listen')

        # Details predefined by Android Tablet code for bluetooth
        uuid = "00001101-0000-1000-8000-00805f9b34fb"
        bluetooth.advertise_service(server_sock, "MDP-Team35",
		 service_id = uuid,
         service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
         profiles = [ bluetooth.SERIAL_PORT_PROFILE ],
        )

        print(f"Waiting for connection on RFCOMM channel {port}")

        # Bluetooth has successfully connected
        client_sock, client_info = server_sock.accept()
        print(f"Accepted connection from {client_info}")
        
        #self.pc_comms.connect_PC()

        # Listen for instructions from Android
        try:
            while True:
                print("In while loop...")
                data = client_sock.recv(1024)
                print("Received [%s]" %data)
                text = str(data.decode())
                print(text)
                
                self.write_to_android('status,START', client_sock)
                # text="taskOne2,3,N/10,15,N/5,7,N/17,18,S"
                # For manual controls on Tablet
                if text == 'STM,W': direction = 'W015'
                elif text == 'STM,S': direction = 'S015'
                elif text == 'STM,A': direction = 'A090'
                elif text == 'STM,D': direction = 'D090'
                elif text == 'STM,Q': direction = 'Q090'
                elif text == 'STM,E': direction = 'E090'
                elif text == 'f': direction = 'f000' # TODO: what does this do?
                elif text[:4] == 'task': direction = text
                else:
                    direction='W000'
                    print("No input to Android detected")
                    continue

                android = []
                allPaths = []

                # Send instructions for Image Recognition
                if len(direction)==7 and direction[:7] == 'taskTwo':

                    print("task 2 start button pressed")
                    mazeRun()

                    # Update information that robot has finished execution
                    time.sleep(0.2)
                    self.write_to_android('status,END', client_sock)
                    time.sleep(1)
                    self.write_to_android('TASK,END', client_sock)
                    
                    print('Done')
                    
                    break

                # Send instructions to STM for manual controls
                else:
                    stm.thread_send(direction) 
                    client_sock.send("Data sent to STM")
                    print('Executed command from Android to STM')

        # Error handling
        except IOError:
            print("error")
        
        # Awaits next instruction
        print("all done")

    def startComms(self):
        conn = bluetoothAndroid()
        conn.connect_android()

if __name__ == '__main__': 
    print("Starting task 2 comms")
    test = bluetoothAndroid()
    test.startComms()
