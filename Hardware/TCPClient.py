#Ref: https://github.com/millo-L/Python-TCP-Image-Socket

import socket

class ClientSocket: 
    def __init__(self, ip, port):
        self.TCP_SERVER_IP = ip
        self.TCP_SERVER_PORT = port
        self.connectCount = 0

    def send_image(self, image_path):
        # Create a TCP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((self.TCP_SERVER_IP, self.TCP_SERVER_PORT))
        print(u'Client socket is connected with Server socket [ TCP_SERVER_IP: ' + self.TCP_SERVER_IP + ', TCP_SERVER_PORT: ' + str(self.TCP_SERVER_PORT) + ' ]')

        # Read the image data
        with open(image_path, "rb") as file:
            image_data = file.read()

        # Send the image data
        client_socket.sendall(image_data)
        print("Image sent!")

        # Close the socket
        client_socket.close()