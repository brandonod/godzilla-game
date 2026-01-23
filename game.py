import pygame
import sys
import random
from gpiozero import Button

#setup 
pygame.init() 
screen = pygame.display.set_mode((600, 900))
clock = pygame.time.Clock()
vel_y = 0
gravity = 1500  # pixels per second squared
jump_speed = 800  # pixels per second upward
speed = 300  # pixels per second horizontal
background_speed = 100  # pixels per second
running = True

# Setup buttons
left_button = Button(23)
jump_button = Button(24)
right_button = Button(25)

#load background 
background = pygame.image.load('godzilla_bg.png').convert()
background = pygame.transform.scale(background, screen.get_size())
background_width = background.get_width()

#load godzilla 
godzilla_neutral = pygame.image.load('godzilla_8bit.png')
godzilla_neutral = pygame.transform.scale(godzilla_neutral, (128,128)).convert_alpha()
godzilla_mask = pygame.mask.from_surface(godzilla_neutral)

#load badguys
bad_guy_image = pygame.image.load('bad-guy.png')
bad_guy_image = pygame.transform.scale(bad_guy_image, (128,128)).convert_alpha()
bad_guy_mask = pygame.mask.from_surface(bad_guy_image)

# List to store all bad guys (each is a dict with 'rect' and 'mask')
bad_guys = []

#godzilla rect for positioning
godzilla_rect = godzilla_neutral.get_rect()
godzilla_rect.centerx = screen.get_width() / 2
godzilla_rect.bottom = screen.get_height() - 50

# Initialize background positions
bg1 = 0
bg2 = background_width

# Start dt at a reasonable value
dt = 0

# Track if on ground
on_ground = True

# Timer for spawning (tracks seconds)
spawn_timer = 0

# Game state
is_dead = False

#game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check for jump button press
    if jump_button.is_pressed and on_ground and not is_dead:
        vel_y = -jump_speed
        on_ground = False

    # Check button states for movement
    if not is_dead:
        if left_button.is_pressed:
            godzilla_rect.x -= speed * dt
        if right_button.is_pressed:
            godzilla_rect.x += speed * dt

        # Apply gravity
        vel_y += gravity * dt
        godzilla_rect.y += vel_y * dt

        # Ground collision - bottom of screen with small margin
        ground_level = screen.get_height() - 50
        if godzilla_rect.bottom >= ground_level:
            godzilla_rect.bottom = ground_level
            vel_y = 0
            on_ground = True

        # Spawn bad guys - check every second
        spawn_timer += dt
        if spawn_timer >= 1.0:  # Every 1 second
            spawn_timer = 0  # Reset timer
            rng_spawn = random.randint(0, 100)
            if rng_spawn < 10:  # 10% chance (numbers 0-9)
                # Create new bad guy with rect and mask
                new_bad_guy_rect = bad_guy_image.get_rect()
                new_bad_guy_rect.centerx = screen.get_width()  # Spawn at right edge
                new_bad_guy_rect.bottom = screen.get_height() - 50
                
                bad_guys.append({
                    'rect': new_bad_guy_rect,
                    'mask': bad_guy_mask
                })

        # Move bad guys to the left
        for bad_guy in bad_guys[:]:  # Use slice to safely remove while iterating
            bad_guy['rect'].x -= background_speed * dt
            # Remove if off screen
            if bad_guy['rect'].right < 0:
                bad_guys.remove(bad_guy)
        
        # Pixel-perfect collision using masks
        for bad_guy in bad_guys:
            # Calculate offset between the two sprites
            offset_x = bad_guy['rect'].x - godzilla_rect.x
            offset_y = bad_guy['rect'].y - godzilla_rect.y
            
            # Check if masks overlap
            if godzilla_mask.overlap(bad_guy['mask'], (offset_x, offset_y)):
                print("you ded")
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

    # Draw everything (always draw, even when dead)
    screen.fill("black")
    screen.blit(background, (bg1, 0))
    screen.blit(background, (bg2, 0))
    
    # Draw all bad guys
    for bad_guy in bad_guys:
        screen.blit(bad_guy_image, bad_guy['rect'])
    
    screen.blit(godzilla_neutral, godzilla_rect)
    
    # Optional: Draw hitboxes for debugging (shows actual rect positions)
    # pygame.draw.rect(screen, (255, 0, 0), godzilla_rect, 2)
    # for bad_guy in bad_guys:
    #     pygame.draw.rect(screen, (0, 255, 0), bad_guy['rect'], 2)
    
    # Show game over text if dead
    if is_dead:
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
        screen.blit(text, text_rect)
        # Press middle button to restart
        if jump_button.is_pressed:
            is_dead = False

    pygame.display.flip()
    dt = clock.tick(60) / 1000  # Convert to seconds

pygame.quit()
sys.exit()