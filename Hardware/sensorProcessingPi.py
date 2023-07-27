#program to capture sensor data and send over UDP
import UDPClient
import TCPClient
from time import sleep
import random
from struct import pack
import board, time, busio, adafruit_vl53l1x, adafruit_adxl34x

IP = '10.0.0.47'
UDP_PORT = 65000
TCP_PORT = 12345
class SensorProcessing:

    def __init__(self, picamera):
        self.udp_client = UDPClient.ClientSocket(IP,UDP_PORT)
        self.tcp_client = TCPClient.ClientSocket(IP,TCP_PORT)

        #PiCamera Setup
        self.cam = picamera
        self.picam_image_filename = "imgs_to_send/pi_cam_img.jpg"
        # Distance sensor setup
        i2c = board.I2C()
        self.distance_sensor = adafruit_vl53l1x.VL53L1X(i2c)
        # self.distance_sensor.distance_mode = 2
        #self.distance_sensor.timing_budget = 500
        #self.distance_sensor.sampling_rate = 5
        self.distance_sensor.start_ranging()
        
        #accelerometer steup
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.accelerometer = adafruit_adxl34x.ADXL345(i2c)


    def getSensorData(self):
        # Take picture
        self.cam.capture_file(self.picam_image_filename)

        if self.distance_sensor.data_ready and self.accelerometer.acceleration:
            distance = self.distance_sensor.distance
            if distance == None:
                print("Nonetype distance, try again")
                return 0, self.accelerometer.acceleration
            print("Distance: {0} cm, {1: .2f} in".format(distance, distance*0.394))
            self.distance_sensor.clear_interrupt()
            
            return distance, self.accelerometer.acceleration
        return 0, (0,0,0)

    def sendDataToPC(self):
        d,a = self.getSensorData()

        #Send sensor readings
        message = pack('4f', d,a[0],a[1],a[2])
        self.udp_client.sendMessageToServer(message)

        #Send picture
        self.tcp_client.sendImage(self.picam_image_filename)

        return d,a

    def closeSocket(self):
        self.udp_client.closeSocket()
