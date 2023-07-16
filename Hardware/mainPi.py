import pygame
import sensorProcessingPi
from pygameConsts import *
#Initalize Pygame
pygame.init()

#Create Window with custom title
pygame.display.set_caption("Wall Mounting Helper")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((400,200))
WIDTH, HEIGHT = screen.get_size()
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

#Test display
x,y,z = sensorProcessingPi.getSensorData()
font = pygame.font.Font(pygame.font.get_default_font(), 32)
text = font.render(f'{x} {y} {z}', True, BLACK)
textRect = text.get_rect()
textRect.center = (CENTER_X, CENTER_Y - 200)

#Cross in center
vert_rect = pygame.Rect(CENTER_X-2,CENTER_Y-8,4,16)
hori_rect = pygame.Rect(CENTER_X-8,CENTER_Y-2,16,4)

run = True
while run:
    #Fill display screen
    screen.fill(WHITE) #White background

    #Test text
    screen.blit(text, textRect)

    #Crosshair
    pygame.draw.rect(screen, RED, vert_rect)
    pygame.draw.rect(screen, RED, hori_rect)
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
        elif event.type == pygame.KEYDOWN:
            pygame.quit()
            run = False
    
