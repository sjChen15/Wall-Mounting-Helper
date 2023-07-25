#image_receive_process.py

import numpy as np
import TCPServer

port = 9999
ip = "0.0.0.0"
# Bind the socket to a specific port
sensor_server = TCPServer.ServerSocket(ip,port)
save_path = ("imgs_received/received_image.jpg")  # Specify the path to save the received image

while True:
    sensor_server.socketOpenAndReceiveImage(save_path)


sensor_server.closeSocket()