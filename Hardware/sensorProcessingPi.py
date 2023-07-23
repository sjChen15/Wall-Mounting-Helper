#program to capture sensor data and send over UDP
import UDPClient
from time import sleep
import random
from struct import pack
import board, time, adafruit_vl53l1x

IP = '10.0.0.47'
UDP_PORT = 65000

class SensorProcessing:

    def __init__(self):
        self.udp_client = UDPClient.ClientSocket(IP,UDP_PORT)
        
        #PiCamera Setup
        self.picam_image_filename = "imgs/pi_cam_img.jpg"
        # Distance sensor setup
        i2c = board.I2C()
        self.distance_sensor = adafruit_vl53l1x.VL53L1X(i2c)
        self.distance_sensor.start_ranging()


    def getSensorData(self, picamera):
        # Take picture
        picamera.capture_file(self.picam_image_filename)

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
        self.udp_client.sendImageToServer(self.picam_image_filename)

        return d

    def closeSocket(self):
        self.udp_client.closeSocket()
