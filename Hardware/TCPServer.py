#Ref: https://github.com/millo-L/Python-TCP-Image-Socket

import socket

class ServerSocket:

    def __init__(self, ip, port):
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #reuse socket in TIME_WAIT state
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server_socket.bind((self.TCP_IP, self.TCP_PORT))
        # #non-blocking
        # self.sock.setblocking(0)            

        # #Time out after 2 seconds
        # self.sock.settimeout(2)

    def closeSocket(self):
        self.sock.close()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is close')

    def receiveImage(self, save_path):
        self.server_socket.listen(1)
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is open')
        client_socket, addr = self.server_socket.accept()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is connected with client')
        
        image_data = bytearray()
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            image_data += data

        # Save the image to a file
        with open(save_path, "wb") as file:
            file.write(image_data)
            print(f"Image saved to: {save_path}")