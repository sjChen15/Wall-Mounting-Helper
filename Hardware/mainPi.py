import pygame
import sensorProcessingPi
from pygameConsts import *
import os
import glob
import time
from picamera2 import Picamera2, Preview

#Initalize Pygame
pygame.init()

#Create Window with custom title
pygame.display.set_caption("Wall Mounting Helper")
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((1200,800))
WIDTH, HEIGHT = screen.get_size()
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

#Camera
#TODO: Try catch here?
picam = Picamera2()
config = picam.create_preview_configuration()
picam.configure(config)
picam.start()

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


latest_time = 0
run = True
while run:
    #Fill display screen
    screen.fill(WHITE) #White background

    #Picture
    if img != "":
        screen.blit(img, (0,0))
    #Test text
    screen.blit(text, textRect)

    #Crosshair
    pygame.draw.rect(screen, RED, vert_rect)
    pygame.draw.rect(screen, RED, hori_rect)
    
    
    #every loop pull most recent picture that's been saved abd display
    pygame.display.update()
    
    file_time = os.path.getctime(img_filename)
    if latest_time < file_time:
        img = pygame.image.load(img_filename)
        latest_time = file_time
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: #if space pressed send data over UDP
                #take a picture
                picam.capture_file("test-python.jpg")
                
                d,a = sensors.sendDataOverUDP()
                text = font.render(f'{d} {a}', True, WHITE)

            else:    
                pygame.quit()
                run = False


