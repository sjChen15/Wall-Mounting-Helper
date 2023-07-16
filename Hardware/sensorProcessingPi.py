#program to capture sensor data and send over UDP
import UDPClient
from time import sleep
import random
from struct import pack

IP = '10.0.0.47'
UDP_PORT = 65000

class SensorProcessing:

    def __init__(self):
        self.udp_client = UDPClient.ClientSocket(IP,UDP_PORT)

    def getSensorData(self):
        #Generate some random start vals
        return random.random(), random.random(), random.random()

    def sendDataOverUDP(self):
        x, y, z = self.getSensorData()
        message = pack('3f', x, y, z)
        self.udp_client.sendMessageToServer(message)

    def closeSocket(self):
        self.udp_client.closeSocket()
