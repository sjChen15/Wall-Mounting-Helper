#program to capture sensor data and send over UDP
import UDPClient
import TCPClient
from time import sleep
import random
from struct import pack
import board, time, adafruit_vl53l1x

IP = '10.0.0.47'
UDP_PORT = 65000
TCP_PORT = 12345
class SensorProcessing:

    def __init__(self, picamera):
        self.udp_client = UDPClient.ClientSocket(IP,UDP_PORT)
        self.tcp_client = TCPClient.ClientSocket(IP,TCP_PORT)

        #PiCamera Setup
        self.cam = picamera
        self.picam_image_filename = "imgs/pi_cam_img.jpg"
        # Distance sensor setup
        i2c = board.I2C()
        self.distance_sensor = adafruit_vl53l1x.VL53L1X(i2c)
        self.distance_sensor.start_ranging()


    def getSensorData(self):
        # Take picture
        self.cam.capture_file(self.picam_image_filename)

        if self.distance_sensor.data_ready:
            distance = self.distance_sensor.distance
            if distance == None:
                print("Nonetype distance, try again")
                return 0
            print("Distance: {0} cm, {1: .2f} in".format(distance, distance*0.394))
            self.distance_sensor.clear_interrupt()
        return distance

    def sendDataOverUDP(self):
        d = self.getSensorData()

        #Send sensor readings
        message = pack('1f', d)
        self.udp_client.sendMessageToServer(message)

        #Send picture
        self.tcp_client.sendImage(self.picam_image_filename)

        return d

    def closeSocket(self):
        self.udp_client.closeSocket()
