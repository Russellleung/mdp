import threading 
from multiprocessing import Process
from client_for_pc import PC_Comm
from android_bluetooth import bluetoothAndroid

class multithreadComm:


    def __init__(self):
        self.pc_comms = PC_Comm(self)
        self.android_comms = bluetoothAndroid(self.pc_comms)

   # Function to connect to the PC Server (for Image Rec)
    def startPC_Comm(self):
        self.pc = self.pc_comms.connect_PC()

   # Establish Bluetooth Connection with Android
    def startAndroid_Comm(self):
        self.android = self.android_comms.connect_android(self)

    #-----------------------

    def main(self):
       # Create threads

        start_android_comms = threading.Thread(target=self.startAndroid_Comm)
        start_pc_comms = threading.Thread(target=self.startPC_Comm)

      # Start threads 
        start_android_comms.start()
        start_pc_comms.start()

       # join threads to the main thread. main thread will only exit after all other threads are completed
        start_android_comms.join()
        start_pc_comms.join()

if __name__ == '__main__':
    conn = multithreadComm()
    conn.__init__()
    conn.main()
