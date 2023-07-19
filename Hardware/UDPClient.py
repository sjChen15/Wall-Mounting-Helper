#Ref: https://stackoverflow.com/questions/64642122/how-to-send-real-time-sensor-data-to-pc-from-raspberry-pi-zero

import socket
from time import sleep
from struct import pack

class ClientSocket:
    def __init__(self, ip, port):
        self.UDP_SERVER_IP = ip
        self.UDP_SERVER_PORT = port
    
    def sendMessageToServer(self, message):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.sendto(message, (self.UDP_SERVER_IP,self.UDP_SERVER_PORT))
        print(u'Message sent to Server Socket [UDP_SERVER_IP: ' + self.UDP_SERVER_IP + ', UDP_SERVER_PORT: ' + str(self.UDP_SERVER_PORT) + ' ]')
    
    def closeSocket(self):
        self.sock.close()