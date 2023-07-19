#main program to run on Raspberry Pi
import TCPClient
import UDPClient
import cv2
from time import sleep
import random
from struct import pack

#test TCP
IP = '10.0.0.47'
TCP_PORT = 12345 
UDP_PORT = 65000
#client = TCPClient.ClientSocket(IP, TCP_PORT)

#run sensor program and pygame program at the same time

#psuedo code for main loop
try:
    while True:
        udp_client = UDPClient.ClientSocket(IP,UDP_PORT)
        #Generate some random start vals
        x, y, z = random.random(), random.random(), random.random()

        # Send a few vals
        for i in range(10):
            
            #Pack three 32-bit floats into message and send
            message = pack('3f', x, y, z)
            udp_client.sendMessageToServer(message)
            
            sleep(1)
            x += 1
            y += 1
            z += 1

        #connect to TCP
        #TCP
        #get sensor readings
        #convert accelerometer to whatever we need
        #read the distance as we need
        #package accelerometer and distance 
        #send package over UDP connection

        #send picture over TCP
        #receive if needed?
        
        #cv2.waitKey(1)
except KeyboardInterrupt:
    print("Terminating")
except Exception as e:
    print(e)