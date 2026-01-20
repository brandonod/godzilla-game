import pygame
pygame.init()

# --- Setup ---
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Jump Tutorial")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Player variables
player_width = 40
player_height = 60
player_x = 50
player_y = SCREEN_HEIGHT - player_height - 10 # Start just above the bottom of the screen
vel_x = 5
vel_y = 0 # Vertical velocity
ground_y = player_y # The Y position of the "floor"
gravity = 1
jump_speed = -20 # Initial upward velocity when jumping

is_jumping = False

clock = pygame.time.Clock()
run = True

# --- Game Loop ---
while run:
    clock.tick(60) # Limit to 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            # Trigger jump only if not already jumping (on the ground)
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                vel_y = jump_speed # Set a strong initial upward velocity

    # --- Movement & Physics ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= vel_x
    if keys[pygame.K_RIGHT]:
        player_x += vel_x

    # Apply gravity and update vertical position
    if is_jumping:
        vel_y += gravity # Gravity increases downward velocity over time
        player_y += vel_y

        # Check for collision with the "ground"
        if player_y >= ground_y:
            player_y = ground_y # Stop at the ground
            is_jumping = False # No longer jumping
            vel_y = 0 # Reset vertical velocity

    # Ensure player stays within horizontal screen boundaries
    if player_x < 0:
        player_x = 0
    if player_x > SCREEN_WIDTH - player_width:
        player_x = SCREEN_WIDTH - player_width

    # --- Drawing ---
    win.fill(BLACK) # Fill the screen with black
    pygame.draw.rect(win, BLUE, (player_x, player_y, player_width, player_height)) # Draw the player

    pygame.display.flip() # Update the display

pygame.quit()
