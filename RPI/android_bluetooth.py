# from client_for_pc import *
from STM_connection import STMConnection

# from carpath import *
import socket
import time
import bluetooth
import os

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
        a = 'p'
        stm.thread_send(a)
        stm.thread_send('W020')
        

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
                while False:
                        
                        print("In while loop...")
#                         stm.thread_send( 'W030')
                        data = client_sock.recv(1024)
                        print("Received [%s]" %data)
                        text = str(data.decode())
                        print(text)
                        
                        self.write_to_android('status,START', client_sock)

                        # For manual controls on Tablet
                        if text == 'w': direction = 'w000'
                        elif text == 's': direction = 's015'
                        elif text == 'STM,A': direction = 'A015'
                        elif text == 'd': direction = 'd015'
                        elif text == 'q': direction = 'q015'
                        elif text == 'e': direction = 'e015'
                        elif text == 'f': direction = 'f000'
                        elif text[:5] == 'begin': direction = text
                        else:
                            direction='w000'
                            print("no text")

                        android = []
                        allPaths = []

                        # Send instructions to STM for manual controls
                        if len(direction)<5:
                                stm.thread_send(direction) 
                                client_sock.send("Data sent to STM")
                                print('Executed command from Android to STM')

                        # Send instructions for Image Recognition
                        # elif direction[:8] == 'beginImg':
                        #         # Find path
                        #         combinedPath = pathFinder(direction)
                        #         print('Sent path to RPI algorithm')

                        #         # Arrange output format
                        #         allPaths = combinedPath[0]
                        #         android = combinedPath[1]
                        #         target = combinedPath[2]

                        #         counter = 1
                        #         x = 0

                        #         # Sort the path instructions
                        #         for path in allPaths:
                        #                 newInst = []
                        #                 start = path[0]
                        #                 count = int(str(start[1:]))

                        #                 # Append instruction list such that all consecutive movements in the same direction are summed together
                        #                 for inst in path[1:]:
                        #                        if start[0] == inst[0]:
                        #                                   count += int(str(inst[1:]))
                        #                        else:
                        #                                   total = count 
                        #                                   if total < 10:
                        #                                              newInst.append(start[0] + '00' + str(total))
                        #                                   elif total < 100:
                        #                                              newInst.append(start[0] + '0' + str(total))
                        #                                   else:
                        #                                              newInst.append(start[0] + str(total))
                        #                                   start = inst
                        #                                   count = int(str(start[1:]))
                        #                 total = count 
                        #                 if total < 10:
                        #                        newInst.append(start[0] + '00' + str(total))
                        #                 elif total < 100:
                        #                        newInst.append(start[0] + '0' + str(total))
                        #                 else:
                        #                        newInst.append(start[0] + str(total))

                        #                 # Print appended path that will be sent to STM along with checking with Image Server
                        #                 print('New path: ')
                        #                 print(newInst)

                        #                 text = self.pc_comms.execute(newInst, target[counter])
                        #                 counter += 1

                        #                 self.write_to_android(android[x][-1], client_sock)
                        #                 x += 1

                        #                 # Send to android the locations of robot
                        #                 time.sleep(1)
                        #                 self.write_to_android(text, client_sock)
                        #                 print('sent to android')

                        #         # Update information that robot has finished execution
                        #         time.sleep(0.2)
                        #         self.write_to_android('status,END', client_sock)
                        #         print('done')

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
        
test = bluetoothAndroid()
test.startComms()