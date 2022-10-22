# from client_for_pc import PC_Comm
# 
# import serial
# import time
# import math
# 
# ser = serial.Serial('/dev/ttyUSB0', 115200, timeout = 0.5)
# 
# def mazeRun():
#     pc_comms = PC_Comm()
#     pc_comms.connect_PC()
#     
#     #yi an code
#     ser.write("C150".encode())
#     print("moving")
#     firstreply=PC_Comm.scanimage(PC_Comm, False)
#     firstRight=firstreply=='38'
#     if firstRight==True:
#         ser.write("J001".encode())
#     else:
#         ser.write("J002".encode())
#     while ser.read().decode()!='K': # after movement complete continue
#         time.sleep(0.5)
#     ser.write("C150".encode())
#     secondRight = PC_Comm.scanimage(PC_Comm, True)=="38"
#     if secondRight==True:
#         ser.write("J003".encode())
#     else:
#         ser.write("J004".encode())
#     return
    
from client_for_pc import PC_Comm

import serial
import time
import math

from CustomThread import CustomThread

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout = 0.5)


def mazeRun():
    pc_comms = PC_Comm()
    pc_comms.connect_PC()
    
#    ser.write("C150".encode())
#     while ser.read().decode()!='K': # after movement complete continue
#         time.sleep(0.2)
#    ser.write("J005".encode())
    
    #yi an code
    t1 = CustomThread(target=ser.write, args=("C150".encode(),))
    t2 = CustomThread(target=PC_Comm.scanimage, args=(PC_Comm, False))
    t1.start()
    t2.start()
    t1.join()
    firstRight = t2.join() == "38"

    if firstRight:
        ser.write("J013".encode())
    else:
        ser.write("J011".encode())
    while ser.read().decode()!='K': # after movement complete continue
        time.sleep(0.2)
        
    if firstRight:
        t1 = CustomThread(target=turn, args=("J014".encode(),))
        t2 = CustomThread(target=PC_Comm.scanimage, args=(PC_Comm, True))
        t1.start()
        t2.start()
        t1.join()
        secondRight = t2.join() == "38"
    else:
        t1 = CustomThread(target=turn, args=("J012".encode(),))
        t2 = CustomThread(target=PC_Comm.scanimage, args=(PC_Comm, True))
        t1.start()
        t2.start()
        t1.join()
        secondRight = t2.join() == "38"
    while ser.read().decode()!='K': # after movement complete continue
        time.sleep(0.2)

    if firstRight:
        if secondRight:
            ser.write("J018".encode())
        else:
            ser.write("J017".encode())
    else:
        if secondRight:
            ser.write("J016".encode())
        else:
            ser.write("J015".encode())

    return
'''
    #for multithreading 2nd 
    if firstRight==True:
        ser.write("J006".encode())
    else:
        ser.write("J005".encode())
    while ser.read().decode()!='K': # after movement complete continue
        time.sleep(0.2)
         
    t1 = CustomThread(target=ser.write, args=("C150".encode(),))
    t2 = CustomThread(target=PC_Comm.scanimage, args=(PC_Comm, True))
    t1.start()
    t2.start()
    t1.join()
    
    detected_class = t2.join()
    
    #problem with islast
    if detected_class == "100":
        if firstRight:
            ser.write("J012".encode())
            PC_Comm.scanimage(PC_Comm, True)
            
        else:
            ser.write("J011".encode())
            PC_Comm.scanimage(PC_Comm, True)
        
    secondRight = detected_class == "38"
    if firstRight:
        if secondRight:
            ser.write("J010".encode())
        else:
            ser.write("J009".encode())
    else:
        if secondRight:
            ser.write("J008".encode())
        else:
            ser.write("J007".encode())
'''
    
    
def turn(command):
    time.sleep(2)
    ser.write(command)

    
    
    
    
#     
#     ser.write("C150".encode())
#     print("moving")
#     firstreply=PC_Comm.scanimage(PC_Comm, False)
#     firstRight=firstreply=='38'
#     if firstRight==True:
#         ser.write("J001".encode())
#     else:
#         ser.write("J002".encode())
#     while ser.read().decode()!='K': # after movement complete continue
#         time.sleep(0.5)
#     ser.write("C150".encode())
#     secondRight = PC_Comm.scanimage(PC_Comm, True)=="38"
#     if secondRight==True:
#         ser.write("J003".encode())
#     else:
#         ser.write("J004".encode())
#     return
#     
#     
#     # take picture
#     firstreply=PC_Comm.scanimage(PC_Comm, False)
#     firstRight = firstreply=="38" # TODO: get from Image Rec
#     
#     moveForward()#creep forward
#     #firstMoveBack = ser.read(4).decode()
#     #print(firstMoveBack, '1')
#     initial = ser.in_waiting
#     while ser.in_waiting==initial:
#         time.sleep(0.6)
#         print('in waiting', ser.in_waiting)
#     firstMoveBack = ser.readline().replace(b'\x00', b'').decode()
#     
#     if firstMoveBack[0] == 'C':
#         firstMoveBack = int(firstMoveBack[5:])
#         
# 
#     if firstRight==True:
#         print("first: right turn")
#         rightOne()
#         #rightTwo(60,150)
#     else:
#         print("first: left turn")
#         leftOne()
#     
#     #return
#     moveForward()
#     secondRight = PC_Comm.scanimage(PC_Comm, True)=="38" # TODO: get from Image Rec
#     
#     secondMoveBack = ser.readline().replace(b'\x00', b'').decode()
#     # print('secondMoveBack', secondMoveBack, type(secondMoveBack))
#     if secondMoveBack[0] == 'C':
#         secondMoveBack = int(secondMoveBack[5:])
#         
#     print('secondMoveBack', secondMoveBack, type(secondMoveBack))
# 
#     if secondRight==True:
#         print("second: right turn")
#         rightTwo(firstMoveBack, secondMoveBack)
#     else:
#         print("second: left turn")
#         leftTwo(firstMoveBack, secondMoveBack)


def moveForward():
    cmds = ['C050'] 
    return sendCreepCommands(cmds)

def rightOne():
    # cmds = ['E090', 'Q180', 'E090']
    # cmds = ['E090', 'Q135', 'E045']
    # cmds = ['E045', 'W005', 'Q090', 'W005', 'E041']
    cmds = ['E045', 'Q090', 'E041'] 
    return sendCommands(cmds)
        
def leftOne():
    # cmds = ['Q090', 'E180', 'Q090']
    # cmds = ['Q090', 'E135', 'Q045']
    # cmds = ['Q045', 'W005', 'E090', 'W005', 'Q041']
    cmds = ['Q045', 'E090', 'Q041'] 
    return sendCommands(cmds)

def rightTwo(distance1 = 100, distance2 = 100):
    cmds = ['E085', 'Q175', 'W065']
    
    # TODO: calculate angle to go back to carpark
    # 50 refers to the distance of robot from centre of line
    if distance2 > distance1:
        cmds.append('Q' + "{:03d}".format(90))
        cmds.append('W' + "{:03d}".format(distance2 - distance1))

        # cmds.append('Q' + "{:03d}".format(round(math.degrees(math.atan(50/(2*distance1 + 10))))))
        # cmds.append('W' + "{:03d}".format(round(((2*distance1 + 10)**2 + 50**2)**0.5)))
        cmds.append('Q' + "{:03d}".format(round(math.degrees(math.atan(50/((2*distance1 + 10)-15)))) + 3))
        cmds.append('W' + "{:03d}".format(round((((2*distance1 + 10)-15)**2 + 50**2)**0.5)))
        cmds.append('E' + "{:03d}".format(round(math.degrees(math.atan(50/((2*distance1 + 10)-15)))) - 5 - 3)) # -5 added to compensate for ground
    else:
        distance = distance1 + distance2 + 10

        # cmds.append('Q' + "{:03d}".format(round(math.degrees(math.atan(50/distance))) + 90))
        # cmds.append('W' + "{:03d}".format(round((distance**2 + 50**2)**0.5)))
        cmds.append('Q' + "{:03d}".format(round(math.degrees(math.atan(50/(distance-15)))) + 90 + 3))
        cmds.append('W' + "{:03d}".format(round(((distance-15)**2 + 50**2)**0.5)))
        cmds.append('E' + "{:03d}".format(round(math.degrees(math.atan(50/(distance-15)))) - 5 - 3)) # -5 added to compensate for ground

    return sendCommands(cmds)

def leftTwo(distance1 = 100, distance2 = 100):
    cmds = ['Q085', 'E175', 'W065']
    
    # TODO: calculate angle to go back to carpark
    # 50 refers to the distance of robot from centre of line
    if distance2 > distance1:
        cmds.append('E' + "{:03d}".format(90))
        cmds.append('W' + "{:03d}".format(distance2 - distance1))

        # cmds.append('E' + "{:03d}".format(round(math.degrees(math.atan(50/(2*distance1 + 10))))))
        # cmds.append('W' + "{:03d}".format(round(((2*distance1 + 10)**2 + 50**2)**0.5)))
        cmds.append('E' + "{:03d}".format(round(math.degrees(math.atan(50/((2*distance1 + 10)-15)))) + 3))
        cmds.append('W' + "{:03d}".format(round((((2*distance1 + 10)-15)**2 + 50**2)**0.5)))
        cmds.append('Q' + "{:03d}".format(round(math.degrees(math.atan(50/((2*distance1 + 10)-15)))) - 5 - 3)) # -5 added to compensate for ground
    else:
        distance = distance1 + distance2 + 10

        # cmds.append('E' + "{:03d}".format(round(math.degrees(math.atan(50/distance))) + 90))
        # cmds.append('W' + "{:03d}".format(round((distance**2 + 50**2)**0.5)))
        cmds.append('E' + "{:03d}".format(round(math.degrees(math.atan(50/(distance-15)))) + 90 + 3))
        cmds.append('W' + "{:03d}".format(round(((distance-15)**2 + 50**2)**0.5)))
        cmds.append('Q' + "{:03d}".format(round(math.degrees(math.atan(50/(distance-15)))) - 5 - 3)) # -5 added to compensate for ground
        
    return sendCommands(cmds)

def sendCommands(cmds):
    print('Sending')
    cmds = cmds[::-1]
    ser.readline()
    ser.readline()
    ser.readline()
    ser.write(cmds.pop().encode())
    while cmds:
        #print(ser.read().decode())
        temp=ser.read().decode()
        print(temp, 'a')
        if temp == "X":
            #time.sleep(0.3)#temp
            print('X detected')            
            
            ser.write(cmds.pop().encode())
        
    while ser.inWaiting()== 0:
        pass
    while ser.read().decode() != "X":
        time.sleep(0.1)
        
    #print(ser.read().decode())
    print("All commands sent")

def sendCreepCommands(cmds):
    print('Sending')
    cmds = cmds[::-1]
    ser.write(cmds.pop().encode())
    #while cmds:
        #print(ser.read().decode())
        
        #if ser.read().decode() != "":
            #ser.write(cmds.pop().encode())
            #continue
    # while ser.peek().decode() == "":
    while ser.inWaiting()== 0:
        print(ser.inWaiting())
        time.sleep(0.6)
    print(ser.inWaiting())
    print("All commands sent")

if __name__ == "__main__":
    print('Start Maze Run')
    mazeRun()
