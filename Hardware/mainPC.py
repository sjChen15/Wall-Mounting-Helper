# main program to run on PC
import TCPClient
import UDPServer
import keyboard
import mathengine as math_engine
import time

PC_IP = "10.0.0.47"
PI_IP = "10.0.0.86"
TCP_CAMERA_PORT = 12345
TCP_SKEW_PORT = 9999
UDP_PORT = 65000
# tcp_server = TCPServer.ServerSocket(TCP_IP, TCP_PORT)
sensors_udp_server = UDPServer.ServerSocket(PC_IP, UDP_PORT)
skewed_image_tcp_client = TCPClient.ClientSocket(PI_IP, TCP_SKEW_PORT)
skewed_image_filename = "C:/Users/shiji/OneDrive/Documents/Wall-Mounting-Helper/Hardware/imgs_to_send/processed.png"
count = 1
try:
    while True:
        if count % 3 == 0:  # send picture on space

            math_engine.unskew_img()

            time.sleep(0.1)

            skewed_image_tcp_client.sendImage(skewed_image_filename)
            count = 0

        sensors_udp_server.waitForMessage()
        count += 1

except Exception as e:
    print(e)

sensors_udp_server.closeSocket()