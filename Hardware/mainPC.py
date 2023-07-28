# main program to run on PC
import TCPClient
import UDPServer
import keyboard
import mathengine as math_engine
import time
from networkConfig import *

# tcp_server = TCPServer.ServerSocket(TCP_IP, TCP_PORT)
sensors_udp_server = UDPServer.ServerSocket(ALL_IP, UDP_PORT)
skewed_image_tcp_client = TCPClient.ClientSocket(PI_IP, TCP_SKEW_PORT)
skewed_image_filename = "C:/Users/shiji/OneDrive/Documents/Wall-Mounting-Helper/Hardware/imgs_to_send/processed.png"
count = 1

#params from UDP
distance = 1 #in cm
accelerometer = [1,1,1] #[x,y,z]
try:
    while True:
        if count % 5 == 0:  # send picture on space

            math_engine.unskew_img(distance, accelerometer)

            time.sleep(0.1)

            skewed_image_tcp_client.sendImage(skewed_image_filename)
            count = 0

        d,a = sensors_udp_server.waitForMessage()
        if d != None:
            distance = d
            accelerometer = a

        count += 1

except Exception as e:
    print(e)

sensors_udp_server.closeSocket()