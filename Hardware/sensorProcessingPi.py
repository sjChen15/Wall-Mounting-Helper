#program to capture sensor data and send over UDP
import UDPClient
from time import sleep
import random
from struct import pack

IP = '10.0.0.47'
UDP_PORT = 65000

def getSensorData():
    #Generate some random start vals
    return random.random(), random.random(), random.random()

def sendDataOverUDP():
    udp_client = UDPClient.ClientSocket(IP,UDP_PORT)

    x, y, z = getSensorData()
    message = pack('3f', x, y, z)
    udp_client.sendMessageToServer(message)