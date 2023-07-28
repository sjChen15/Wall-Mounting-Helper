#image_receive_process.py

import numpy as np
import TCPServer
from networkConfig import *

# Bind the socket to a specific port
sensor_server = TCPServer.ServerSocket(ALL_IP,TCP_CAMERA_PORT)
save_path = ("C:/Users/shiji/OneDrive/Documents/Wall-Mounting-Helper/Hardware/imgs_received/pi_cam_img.jpg")  # Specify the path to save the received image

try:
    while True:
        sensor_server.receiveImage(save_path)

except KeyboardInterrupt:
    sensor_server.closeSocket()