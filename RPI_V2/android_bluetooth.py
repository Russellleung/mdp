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
                print(f"Received [{data}]")
                text = str(data.decode())
                print(text)
                
                self.write_to_android('status,START', client_sock)
                # text = "taskOne2,3,N/10,15,N/5,7,N/17,18,S"
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

                positions = []
                instructions = []

                # Send instructions for Image Recognition
                if len(direction)>7 and direction[:7] == 'taskOne':

                    unsortedTargets = self.parseAndroidToCarpath(direction[7:])
                    combinedPath, positions = pathFinder(unsortedTargets, Map())
                    
                    instructions = combinedPath[0] 
                    order = combinedPath[1]
                    order = [unsortedTargets[i-1] for i in order]


                    print("instructions", instructions)  # 2D array showing list of UART instructions from current obstacle to next obstacle i.e. path segments
                    print("order", order)  # 1D array showing order of obstacles to visit 
                    print("positions", positions) # 3D array showing position [x, y, D] of robot after each UART instruction separated by path segments
                    counter = 1
                    x = 0
                    
                    for path in instructions:
                        newInst = []
                        start = path[0]
                        count = int(str(start[1:]))

                        # Append instruction list such that all consecutive movements in the same direction are summed together
                        for inst in path[1:]:
                            if start[0] == inst[0]:
                                count += int(str(inst[1:]))
                            else:
                                total = count 
                                newInst.append(start[0] + "{:03d}".format(total))
                                start = inst
                                count = int(str(start[1:]))

                        total = count 
                        newInst.append(start[0] + "{:03d}".format(total))

                        # Print appended path that will be sent to STM along with checking with Image Server
                        print('New path: ')
                        print(newInst)
                        text = self.pc_comms.execute(newInst, order[counter], counter+1==len(order))
                        counter += 1

                        self.write_to_android(self.parseCarpathToAndroid(positions[x]), client_sock)
                        x += 1

                        time.sleep(1)
                        self.write_to_android(text, client_sock)
                        print('Sent to android')

                    # Update information that robot has finished execution
                    time.sleep(0.2)
                    self.write_to_android('status,END', client_sock)
                    print('Done')

                # Execute fastest path
                # elif direction[:6] == 'beginF':

                #     instructions = 'r065p000'
                #     stm.thread_send(instructions)

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
  
test = bluetoothAndroid()
test.startComms()
