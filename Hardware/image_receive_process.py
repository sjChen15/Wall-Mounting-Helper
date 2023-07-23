#image_receive_process.py

import numpy as np
import TCPServer

port = 9999
ip = "0.0.0.0"
# Bind the socket to a specific port
sensor_server = TCPServer.ServerSocket(ip,port)
save_path = ("imgs/received_image.jpg")  # Specify the path to save the received image
img_num = 0

while True:
    img_num +=1
    sensor_server.socketOpenAndReceiveImage(save_path)

    if img_num > 10000:
        break

sensor_server.closeSocket()