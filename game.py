import pygame
import sys

#setup 
pygame.init() 
screen = pygame.display.set_mode((600, 900))
clock = pygame.time.Clock()
dt = 0 
speed = 300
running = True

#load backgroudn 
background = pygame.image.load('godzilla_bg.png').convert()
background = pygame.transform.scale(background, screen.get_size())

#load godzilla 
godzilla_neutral = pygame.image.load('godzilla_8bit.png')
godzilla_neutral = pygame.transform.scale(godzilla_neutral, (128,128)).convert_alpha()

#godzilla hitbox 
godzilla_hitbox = godzilla_neutral.get_rect()
godzilla_hitbox.center = (screen.get_width() / 2, screen.get_height() / 2)

#game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.quit:
            running = False

    #keymovement 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        godzilla_hitbox.y -= speed * dt
    if keys[pygame.K_s]:
        godzilla_hitbox.y += speed * dt
    if keys[pygame.K_a]:
        godzilla_hitbox.x -= speed * dt
    if keys[pygame.K_d]:
        godzilla_hitbox.x += speed * dt


    screen.fill("black")
    screen.blit(background, (0,0))
    screen.blit(godzilla_neutral, godzilla_hitbox)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()