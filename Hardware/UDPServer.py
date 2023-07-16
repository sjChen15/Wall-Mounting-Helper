#Ref: https://stackoverflow.com/questions/64642122/how-to-send-real-time-sensor-data-to-pc-from-raspberry-pi-zero

import socket
from struct import unpack

class ServerSocket:
    def __init__(self, ip, port):
        self.UDP_IP = ip
        self.UDP_PORT = port
        self.socketOpen
    
    def socketOpen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        print(u'Server socket [ UDP_IP: ' + self.UDP_IP + ', UDP_PORT: ' + str(self.UDP_PORT) + ' ] is open')

    def socketClose(self):
        self.sock.close()
        print(u'Server socket [ UDP_IP: ' + self.UDP_IP + ', UDP_PORT: ' + str(self.UDP_PORT) + ' ] is closed')

    def waitForMessage(self):
        message, address = self.sock.recvfrom(4096)
        print(f'Received {len(message)} from {address}')
        x, y, z = unpack('3f', message)
        print(f'X: {x}, Y: {y}, Z: {z}')

