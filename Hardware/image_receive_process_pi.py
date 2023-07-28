#image_receive_process.py

import numpy as np
import TCPServer
from networkConfig import *

# Bind the socket to a specific port
sensor_server = TCPServer.ServerSocket(ALL_IP,TCP_SKEW_PORT)
save_path = ("imgs_received/received_image.jpg")  # Specify the path to save the received image

while True:
    try:
        sensor_server.receiveImage(save_path)

    except KeyboardInterrupt:
        sensor_server.closeSocket()
        break
    except Exception as e:
        sensor_server.closeSocket()
        break