#Ref: https://stackoverflow.com/questions/64642122/how-to-send-real-time-sensor-data-to-pc-from-raspberry-pi-zero

import socket
from struct import unpack
import sys
import socket
import errno
from time import sleep

class ServerSocket:
    def __init__(self, ip, port):
        self.UDP_IP = ip
        self.UDP_PORT = port
        self.picam_image_filename ="imgs/pi_cam_img.jpg"
        self.socketOpen()
    
    def socketOpen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))

        #non-blocking
        self.sock.setblocking(0)            

        #Time out after 2 seconds
        self.sock.settimeout(2)
        print(u'Server socket [ UDP_IP: ' + self.UDP_IP + ', UDP_PORT: ' + str(self.UDP_PORT) + ' ] is open')

    def closeSocket(self):
        self.sock.close()
        print(u'Server socket [ UDP_IP: ' + self.UDP_IP + ', UDP_PORT: ' + str(self.UDP_PORT) + ' ] is closed')

    def waitForMessage(self):
        #Ref: https://stackoverflow.com/questions/16745409/what-does-pythons-socket-recv-return-for-non-blocking-sockets-if-no-data-is-r
        try:
            message, address = self.sock.recvfrom(4096)
        except socket.error as e:
            err = e.args[0]
            # if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
            #     sleep(1)
            #     print ('No data available')
            if err == "timed out": #timed out goes here
                print ('No data available')
            else:
                # a "real" error occurred
                print (e)
        else:
            # got a message, do something :)
            print(f'Received {len(message)} from {address}')
            d = unpack('1f', message)
            print(f'Distance = {d} cm')