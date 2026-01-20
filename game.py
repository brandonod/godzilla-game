import pygame
import sys
import random

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

#load badguys
bad_guy_image = pygame.image.load('bad-guy.png')
bad_guy_image = pygame.transform.scale(bad_guy_image, (128,128)).convert_alpha()

# List to store all bad guys
bad_guys = []

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

# Timer for spawning (tracks seconds)
spawn_timer = 0

is_dead = False

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

    # Spawn bad guys - check every second
    spawn_timer += dt
    if spawn_timer >= 1.0:  # Every 1 second
        spawn_timer = 0  # Reset timer
        rng_spawn = random.randint(0, 100)
        if rng_spawn < 10:  # 10% chance (numbers 0-9)
            # Create new bad guy
            new_bad_guy = bad_guy_image.get_rect()
            new_bad_guy.centerx = screen.get_width()  # Spawn at right edge
            new_bad_guy.bottom = screen.get_height() - 50
            bad_guys.append(new_bad_guy)

    # Move bad guys to the left
    for bad_guy in bad_guys[:]:  # Use slice to safely remove while iterating
        bad_guy.x -= background_speed * dt
        # Remove if off screen
        if bad_guy.right < 0:
            bad_guys.remove(bad_guy)
    
    # collision - check each bad guy
    for bad_guy in bad_guys:
        if godzilla_hitbox.colliderect(bad_guy):
            is_dead = True
            break


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
    
    # Draw all bad guys
    for bad_guy in bad_guys:
        screen.blit(bad_guy_image, bad_guy)
    
    screen.blit(godzilla_neutral, godzilla_hitbox)

    if is_dead:
        font = pygame.font.Font(None, 75)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width() /2, screen.get_height() /2))
        screen.blit(text, text_rect)

    pygame.display.flip()
    dt = clock.tick(60) / 1000  # Convert to seconds

pygame.quit()
sys.exit()