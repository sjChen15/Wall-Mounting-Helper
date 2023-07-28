import pygame
import sensorProcessingPi
from pygameConsts import *
import os
import glob
import time
from picamera2 import Picamera2, Preview

#Camera
try:
    picam = Picamera2()
    config = picam.create_preview_configuration()
    picam.configure(config)
    picam.start()
except Exception as e:
    print(e)
    exit()
    
#Initalize Pygame
pygame.init()

#Create Window with custom title
pygame.display.set_caption("Wall Mounting Helper")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((1200,800))
WIDTH, HEIGHT = screen.get_size()
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

#Sensors
sensors = sensorProcessingPi.SensorProcessing(picam)

#Test display
font = pygame.font.Font(pygame.font.get_default_font(), 32)
d,a = sensors.getSensorData()
text = font.render(f'{d} {a}', True, WHITE)
textRect = text.get_rect()
textRect.center = (CENTER_X, 100)

#Cross in center
vert_rect = pygame.Rect(CENTER_X-2,CENTER_Y-8,4,16)
hori_rect = pygame.Rect(CENTER_X-8,CENTER_Y-2,16,4)

#image from computer
img_filename = "imgs_received/received_image.jpg"
img = ""

def cleanup():
    pygame.quit()
    sensors.closeSocket()
    picam.close()

sensor_loop_count = 200
last_time = 0
run = True
try:
    while run:
        #Fill display screen
        screen.fill(BLACK) #White background

        #Picture
        if img != "":
            screen.blit(img, (CENTER_X-img.get_width()//2,CENTER_Y-img.get_height()//2))
        #Test text
        screen.blit(text, textRect)
        
        pygame.display.update()
        
        file_time = os.path.getctime(img_filename)
        if last_time < file_time:
            print("got a more recent pic")
            img = pygame.image.load(img_filename)
            last_time = file_time
        
        #send data over every 50 loops
        if sensor_loop_count == 200:
            sensor_loop_count = 0
                    
            d,a = sensors.sendDataToPC()
            text = font.render(f'{d} {a}', True, WHITE)
            
        else:
            sensor_loop_count += 1
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cleanup()
                run = False
            elif event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_SPACE: #if space pressed send data over UDP
                    #take a picture
                   # picam.capture_file("test-python.jpg")
                    
                  #  d,a = sensors.sendDataToPC()
                 #   text = font.render(f'{d} {a}', True, WHITE)

                #else:    
                cleanup()
                run = False
except Exception as e:
    print(e)
    cleanup()
