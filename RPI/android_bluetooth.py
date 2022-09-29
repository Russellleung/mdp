# from client_for_pc import *
from STM_connection import STMConnection

# from carpath import *
import socket
import time
import bluetooth
import os

from carpath import pathFinder
from map import Map

class bluetoothAndroid:

    # Address of android tablet
    addr="6C:2F:8A:38:0E:AA"

    # Function for sending to android
    def write_to_android(self, text, client_sock):
        print(text)
        print(type(text))
        try:
            client_sock.send(text)
        except Exception as e:
            # displayed on android
            print('[write to RPI ERROR] %s' % str(e))
            raise e

    def __init__(self):
        self.sock = None
        self.isConnected = False
        self.threadListening = False
        #self.pc_comms = PCComms

    # Function for connecting to android
    def connect_android(self):
        addr = "6C:2F:8A:38:0E:AA"
        stm = STMConnection()
        print("stm connected")
        #a = 'p'
        #stm.thread_send(a)
        # stm.thread_send('W020')


        os.system('sudo hciconfig hci0 piscan')
        server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        port = 1

        # Bind bluetooth to port 1
        server_sock.bind(("", port))
        server_sock.listen(1)

        # Details predefined by Android Tablet code for bluetooth
        uuid = "00001101-0000-1000-8000-00805f9b34fb"
        bluetooth.advertise_service(server_sock, "MDP-Team35",
		 service_id = uuid,
         service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
         profiles = [ bluetooth.SERIAL_PORT_PROFILE ],
        )

        print("Waiting for connection on RFCOMM channel %d" % port)

        # Bluetooth has successfully connected
        client_sock, client_info = server_sock.accept()
        print("Accepted connection from ", client_info)

        # Listen for instructions from Android
        try:
            while True:
                print("In while loop...")
                data = client_sock.recv(1024)
                print("Received [%s]" %data)
                text = str(data.decode())
                print(text)
                
                self.write_to_android('status,START', client_sock)
                #text="taskOne2,3,N/10,15,N/5,7,N/17,18,S"
                # For manual controls on Tablet
                if text == 'STM,W': direction = 'W015'
                elif text == 'STM,S': direction = 'S015'
                elif text == 'STM,A': direction = 'A015'
                elif text == 'STM,D': direction = 'D015'
                elif text == 'STM,Q': direction = 'Q015'
                elif text == 'STM,E': direction = 'E015'
                elif text == 'f': direction = 'f000'
                elif text[:4] == 'task': direction = text
                else:
                    direction='W000'
                    print("no text")

                android = []
                allPaths = []
                
                # Send instructions to STM for manual controls
                if len(direction)<5:
                    stm.thread_send(direction) 
                    client_sock.send("Data sent to STM")
                    print('Executed command from Android to STM')

                # Send instructions for Image Recognition
                elif direction[:7] == 'taskOne':

                    unsortedTargets=self.parseAndroidToCarpath(direction[7:])
                    combinedPath,android = pathFinder(unsortedTargets,Map())
                    
                    allPaths = combinedPath[0] 
                    target = combinedPath[1]
                    target=[unsortedTargets[i] for i in target]


                    print(allPaths)  # 2D array showing list of UART instructions from current obstacle to next obstacle i.e. path segments
                    print(android)  # 1D array showing order of obstacles to visit 
                    print(target) # 3D array showing position [x, y, D] of robot after each UART instruction separated by path segments
                    counter = 1
                    x = 0
                    
                    for path in allPaths:
                        newInst = []
                        start = path[0]
                        count = int(str(start[1:]))

                        # Append instruction list such that all consecutive movements in the same direction are summed together
                        for inst in path[1:]:
                            if start[0] == inst[0]:
                                count += int(str(inst[1:]))
                            else:
                                total = count 
                                if total < 10:
                                    newInst.append(start[0] + '00' + str(total))
                                elif total < 100:
                                    newInst.append(start[0] + '0' + str(total))
                                else:
                                    newInst.append(start[0] + str(total))
                                start = inst
                                count = int(str(start[1:]))
                        total = count 
                        if total < 10:
                            newInst.append(start[0] + '00' + str(total))
                        elif total < 100:
                            newInst.append(start[0] + '0' + str(total))
                        else:
                            newInst.append(start[0] + str(total))

                        # Print appended path that will be sent to STM along with checking with Image Server
                        print('New path: ')
                        print(newInst)
                    
                        text = self.pc_comms.execute(newInst, target[counter])
                        counter += 1

                        self.write_to_android(self.parseCarpathToAndroid(android[x][-1]), client_sock)
                        x += 1

                        time.sleep(1)
                        self.write_to_android(text, client_sock)
                        print('sent to android')

                    # Update information that robot has finished execution
                    time.sleep(0.2)
                    self.write_to_android('status,END', client_sock)
                    print('done')

                # # Execute fastest path
                # elif direction[:6] == 'beginF':
                #         instructions = 'r065p000'
                #         stm.thread_send(instructions)

                else:
                    print('No data sent')
        # Error handling
        except IOError:
            pass
        
        # Awaits next instruction
        print("all done")

    def startComms(self):
        conn = bluetoothAndroid()
        conn.connect_android()

    def parseAndroidToCarpath(self, androidInput):
        # input is 1,1/1,2/.../20,20
        output = [inputs.split(',') for inputs in androidInput.split('/')]
        output = [[(int(position[0])-1)*10+5, (int(position[1])-1)*10+5, position[2].lower()]for position in output] # TODO: check whether +5 is required (will it give errors?)
        return output

    def parseCarpathToAndroid(self, carPathInput):
        output = []
        for path in carPathInput:
            for position in path:
                output += [','.join(['ROBOT', str((position[0])//2), str((position[1])//2), position[2].upper()])]
        return output
        
test = bluetoothAndroid()
test.startComms()