#main program to run on PC
import TCPServer
import cv2

TCP_IP = '10.0.0.47'
TCP_PORT = 12345 
server = TCPServer.ServerSocket(TCP_IP, TCP_PORT)


# #psuedo code for main loop
# try:
#     while True:
#         #connect to both sockets
#         #get sensor readings
#         #get picture
#         #send picture?

#         cv2.waitKey(1)
# except Exception as e:
#     print(e)