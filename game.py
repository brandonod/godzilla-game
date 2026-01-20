import pygame
import sys

#setup 
pygame.init() 
screen = pygame.display.set_mode((600, 900))
clock = pygame.time.Clock()
vel_y = 0
gravity = 1500  # pixels per second squared
jump_speed = 600  # pixels per second upward
speed = 300  # pixels per second horizontal
background_speed = 100  # pixels per second
running = True

#load background 
background = pygame.image.load('godzilla_bg.png').convert()
background = pygame.transform.scale(background, screen.get_size())
background_width = background.get_width()

#load godzilla 
godzilla_neutral = pygame.image.load('godzilla_8bit.png')
godzilla_neutral = pygame.transform.scale(godzilla_neutral, (128,128)).convert_alpha()

#godzilla hitbox 
godzilla_hitbox = godzilla_neutral.get_rect()
godzilla_hitbox.centerx = screen.get_width() / 2
godzilla_hitbox.bottom = screen.get_height() - 50  # Start near bottom

# Initialize background positions
bg1 = 0
bg2 = background_width

# Start dt at a reasonable value
dt = 0

# Track if on ground
on_ground = True

#game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Jump only on key press, not hold
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and on_ground:
                vel_y = -jump_speed
                on_ground = False

    #keymovement (horizontal only)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        godzilla_hitbox.y += speed * dt
    if keys[pygame.K_a]:
        godzilla_hitbox.x -= speed * dt
    if keys[pygame.K_d]:
        godzilla_hitbox.x += speed * dt

    # Apply gravity
    vel_y += gravity * dt
    godzilla_hitbox.y += vel_y * dt

    # Ground collision - bottom of screen with small margin
    ground_level = screen.get_height() - 50
    if godzilla_hitbox.bottom >= ground_level:
        godzilla_hitbox.bottom = ground_level
        vel_y = 0
        on_ground = True

    # Update background positions
    bg1 -= background_speed * dt
    bg2 -= background_speed * dt

    # Reset positions when they go off screen
    if bg1 <= -background_width:
        bg1 = background_width
    if bg2 <= -background_width:
        bg2 = background_width

    # Draw everything
    screen.fill("black")
    screen.blit(background, (bg1, 0))
    screen.blit(background, (bg2, 0))
    screen.blit(godzilla_neutral, godzilla_hitbox)

    pygame.display.flip()
    dt = clock.tick(60) / 1000  # Convert to seconds

pygame.quit()
sys.exit()