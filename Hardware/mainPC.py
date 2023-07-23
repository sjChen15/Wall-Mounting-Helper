#main program to run on PC
import TCPClient
import UDPServer
import keyboard

IP = '10.0.0.47'
TCP_CAMERA_PORT = 12345 
TCP_SKEW_PORT = 9999
UDP_PORT = 65000
#tcp_server = TCPServer.ServerSocket(TCP_IP, TCP_PORT)
sensors_udp_server = UDPServer.ServerSocket(IP, UDP_PORT)
skewed_image_tcp_client = TCPClient.ClientSocket(IP, TCP_SKEW_PORT)
skewed_image_filename = "imgs/squink.png"
try:
    while True:
        sensors_udp_server.waitForMessage()

        if keyboard.is_pressed('space'): #send picture on space
            skewed_image_tcp_client.sendImage(skewed_image_filename)
            break

except Exception as e:
    print(e)

sensors_udp_server.closeSocket()