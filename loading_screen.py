import pygame
import time
from constants import *

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Loading Animation")

# Colors & Fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.Font("broken_console.ttf", 60) 

# Loading animation states
loading_states = ["Loading   ", "Loading.  ", "Loading.. ", "Loading..."]
state_index = 0

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)  # Clear screen

    # Render the current loading state
    text_surface = font.render(loading_states[state_index], True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)

    pygame.display.flip()  # Update display

    # Cycle through states
    state_index = (state_index + 1) % len(loading_states)
    
    time.sleep(0.5)  # Adjust speed of animation
    clock.tick(60)  # Keep framerate steady

    # Event handling (close window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
