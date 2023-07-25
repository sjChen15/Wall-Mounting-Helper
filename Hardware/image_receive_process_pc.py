#image_receive_process.py

import numpy as np
import TCPServer

port = 12345
ip = "0.0.0.0"
# Bind the socket to a specific port
sensor_server = TCPServer.ServerSocket(ip,port)
save_path = ("C:/Users/shiji/OneDrive/Documents/Wall-Mounting-Helper/Hardware/imgs_received/pi_cam_img.jpg")  # Specify the path to save the received image
img_num = 0

while True:
    img_num +=1
    sensor_server.socketOpenAndReceiveImage(save_path)

    if img_num > 10:
        break

sensor_server.closeSocket()