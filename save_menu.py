import pygame
import math
from config import *

# Renders and operates the save menu, which allows the user to save the current simulation
def save_menu(clock, screen):
    position = (screen.get_width() // 2, screen.get_height() // 2)
    background_color = (120, 120, 120)
    size = (600, 400)

    # Create a rectangle for the background
    bg_rect = pygame.Rect(position[0] - size[0] // 2, position[1] - size[1] // 2, size[0], size[1])

    # Create a rectangle for the simulation name input box
    input_box_rect = pygame.Rect(position[0] - 150, position[1] - 50, 300, 40)
    input_box_color = (200, 200, 200)
    input_box_active = False
    input_text = ""
    font = pygame.font.Font(None, 36)

    saving_menu_visible = True
    while saving_menu_visible:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                saving_menu_visible = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Close the menu on Escape key
                    saving_menu_visible = False
                elif input_box_active:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    # Check if it is a letter or number
                    elif event.unicode.isalnum() or event.unicode in [' ', '_', '-']:
                        input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if input_box_rect.collidepoint(event.pos):
                        input_box_active = True
                    else:
                        input_box_active = False

        # Draw the menu background
        screen.fill(background_color, bg_rect)

        # Draw the title
        title_surface = font.render("Save Simulation?", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(position[0], position[1] - 170))
        screen.blit(title_surface, title_rect)

        # Draw the input box
        pygame.draw.rect(screen, input_box_color, input_box_rect, border_radius=5)
        if input_box_active:
            input_box_color = (150, 150, 150)
        else:
            input_box_color = (200, 200, 200)
        input_surface = font.render(input_text, True, (0, 0, 0))
        input_rect = input_surface.get_rect(center=input_box_rect.center)
        screen.blit(input_surface, input_rect)
        pygame.draw.rect(screen, (0, 0, 0), input_box_rect, 2, border_radius=5)

        pygame.display.flip()
        clock.tick(FPS)