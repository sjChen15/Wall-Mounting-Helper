import pygame
import sensorProcessingPi
from pygameConsts import *
#Initalize Pygame
pygame.init()

#Create Window with custom title
pygame.display.set_caption("Wall Mounting Helper")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

#Test display
x,y,z = sensorProcessingPi.getSensorData()
text = FONT.render(f'{x} {y} {z}', True, BLACK)
textRect = text.get_rect()
textRect.center = (CENTER_X, CENTER_Y - 200)

#Cross in center
vert_rect = pygame.Rect(CENTER_X-10,CENTER_Y-50,20,100)
hori_rect = pygame.Rect(CENTER_X-50,CENTER_X-10,100,20)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False

    #Fill display screen
    screen.fill(WHITE) #White background

    #Test text
    screen.blit(text, textRect)

    #Crosshair
    pygame.draw.rect(screen, RED, vert_rect)
    pygame.draw.rect(screen, RED, hori_rect)
    