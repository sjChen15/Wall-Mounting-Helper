#main program to run on PC
import TCPServer
import UDPServer
import cv2

TCP_IP = '10.0.0.47'
TCP_PORT = 12345 
UDP_PORT = 65000
#tcp_server = TCPServer.ServerSocket(TCP_IP, TCP_PORT)
udp_server = UDPServer.ServerSocket(TCP_IP, UDP_PORT)


try:
    while True:
        udp_server.waitForMessage()
        cv2.waitKey(1)
except Exception as e:
    print(e)

udp_server.closeSocket()
