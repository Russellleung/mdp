
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
        self.pc_comms = PC_Comm()
        #self.pc_comms.connect_PC()

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
        
        self.pc_comms.connect_PC()

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
                if len(direction)>7 and direction[:7] == 'taskOne':

                    unsortedTargets=self.parseAndroidToCarpath(direction[7:])
                    combinedPath,android = pathFinder(unsortedTargets,Map())
                   
                    
                    allPaths = combinedPath[0] 
                    target = combinedPath[1]
                    target=[unsortedTargets[i-1] for i in target]

                    
                    print("allPaths",allPaths)  # 2D array showing list of UART instructions from current obstacle to next obstacle i.e. path segments
                    print("target",target)  # 1D array showing order of obstacles to visit 
                    print("android",android) # 3D array showing position [x, y, D] of robot after each UART instruction separated by path segments
                    counter = 1
                    x = 0
                    
                    for path in allPaths:
                        newInst = []
                        start = path[0]
                        count = int(str(start[1:]))
                        print('path', path)
                        print('start', start)
                        # Append instruction list such that all consecutive movements in the same direction are summed together
                        for inst in path[1:]:
                            #direction for stm
                            direction = str(inst[0])
                            #opposite direction
                            opp_direction = ['W' if direction == 'S' else 'S' if direction == 'W' else 'T'][0]
                            print(direction, opp_direction, start[0], count)
                            
                            
                            if start[0] == direction:
                                count += int(str(inst[1:]))
                            elif start[0] == opp_direction:
                                count -= int(str(inst[1:]))
                            else:
                                print('xxx')
                                if count>0:
                                    newInst.append(start[0] + "{:03d}".format(count))
                                elif count<0:
                                    newInst.append(['W' if start[0] == 'S' else 'S'][0] + "{:03d}".format(-count))
                                else:
                                    continue
                                
                                start = inst
                                count = int(str(start[1:]))

                        if count>0:
                            # count = int(count*20/21)
                            #count = [x-5 if x>10 else x for x in [count]][0] # software offset
                            newInst.append(start[0] + "{:03d}".format(count))
                        elif count<0:
                            # count = int(count*20/21)
                            #count = [x+5 if x<-10 else x for x in [count]][0] # software offset
                            newInst.append(['W' if start[0] == 'S' else 'S'][0] + "{:03d}".format(-count))
                        else:
                            continue
                        print('-', '-', start[0], count)
                        # Print appended path that will be sent to STM along with checking with Image Server
                        newInst = ['K090' if x[0]=='K' else 'L090' if x[0]=='L' else x for x in newInst]
                        print('New path: ', newInst)
                        text = self.pc_comms.execute(newInst, target[counter], counter+1==len(target))
                        counter += 1

                        self.write_to_android(self.parseCarpathToAndroid(android[x]), client_sock)
                        x += 1

                        time.sleep(1)
                        text = text[11:]
                        self.write_to_android(text, client_sock)
                        print('Sent to android')

                    # Update information that robot has finished execution
                    time.sleep(0.2)
                    self.write_to_android('status,END', client_sock)
                    time.sleep(1)
                    self.write_to_android('TASK,END', client_sock)
                    
                    print('Done')

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

    def parseAndroidToCarpath(self, androidInput):
        # input is 1,1/1,2/.../20,20
        output = [inputs.split(',') for inputs in androidInput.split('/')]
        output = [[(int(position[1])-1)*10+5, (int(position[0])-1)*10+5, position[2].lower()]for position in output] # TODO: check whether +5 is required (will it give errors?)
        print("output",output)
        return output

    def parseCarpathToAndroid(self, path):
        output = []
        
        for position in path:
            output += [','.join(['ROBOT', str((position[1])//2), str((position[0])//2), position[2].upper()])]
        return output[-1]
  
print("Starting indoor comms")
test = bluetoothAndroid()
test.startComms()
