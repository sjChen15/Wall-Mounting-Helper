#Ref: https://github.com/millo-L/Python-TCP-Image-Socket

import socket

class ServerSocket:

    def __init__(self, ip, port):
        self.TCP_IP = ip
        self.TCP_PORT = port

    def closeSocket(self):
        self.sock.close()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is close')

    def socketOpenAndReceiveImage(self, save_path):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.TCP_IP, self.TCP_PORT))
        # #non-blocking
        # self.sock.setblocking(0)            

        # #Time out after 2 seconds
        # self.sock.settimeout(2)

        self.sock.listen(1)
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is open')
        self.client_socket, self.addr = self.sock.accept()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is connected with client')
        
        image_data = bytearray()
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break
            image_data += data

        # Save the image to a file
        with open(save_path, "wb") as file:
            file.write(image_data)
            print(f"Image saved to: {save_path}")

        self.sock.close()
        print(f"Server socket for port {self.TCP_PORT} closed")
