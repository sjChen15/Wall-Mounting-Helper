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
picam = Picamera2()
config = picam.create_preview_configuration()
picam.configure(config)
picam.start()

#Sensors
sensors = sensorProcessingPi.SensorProcessing(picam)

#Test display
font = pygame.font.Font(pygame.font.get_default_font(), 32)
d = sensors.getSensorData()
text = font.render(f'{d}', True, BLACK)
textRect = text.get_rect()
textRect.center = (CENTER_X, CENTER_Y - 200)

#Cross in center
vert_rect = pygame.Rect(CENTER_X-2,CENTER_Y-8,4,16)
hori_rect = pygame.Rect(CENTER_X-8,CENTER_Y-2,16,4)

#image from computer
img = ""

def cleanup():
    pygame.quit()
    sensors.closeSocket()
    picam.close()


latest_filename = "" #filename of the last pulled image    
run = True
while run:
    #Fill display screen
    screen.fill(WHITE) #White background

    #Picture
    if img != "":
        screen.blit(img, (100,100))
    #Test text
    screen.blit(text, textRect)

    #Crosshair
    pygame.draw.rect(screen, RED, vert_rect)
    pygame.draw.rect(screen, RED, hori_rect)
    
    
    #every loop pull most recent picture that's been saved abd display
    pygame.display.update()
    
    
    folder_most_recent_file = max(glob.glob('/home/fydp/Documents/Wall-Mounting-Helper/Hardware/imgs/*'), key=os.path.getmtime)
    if len(os.listdir('/home/fydp/Documents/Wall-Mounting-Helper/Hardware/imgs')) != 0 and folder_most_recent_file != latest_filename:
        img = pygame.image.load(folder_most_recent_file)
        latest_filename = folder_most_recent_file
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: #if space pressed send data over UDP
                d = sensors.sendDataOverUDP()
                text = font.render(f'{d}', True, BLACK)
            else:    
                pygame.quit()
                run = False


