#image_receive_process.py

import numpy as np
import TCPServer

port = 12345
ip = "0.0.0.0"
# Bind the socket to a specific port
sensor_server = TCPServer.ServerSocket(ip,port)
save_path = ("C:/Users/shiji/OneDrive/Documents/Wall-Mounting-Helper/Hardware/imgs_received/pi_cam_img.jpg")  # Specify the path to save the received image

try:
    while True:
        sensor_server.receiveImage(save_path)

except KeyboardInterrupt:
    sensor_server.closeSocket()