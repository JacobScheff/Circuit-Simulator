import pygame
import math
import pickle
from config import *

# Renders and operates the save menu, which allows the user to save the current simulation
def save_menu(clock, screen, main_simulation):
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

    # Save button
    save_button_rect = pygame.Rect(position[0] - 100, position[1] + 50, 200, 40)
    save_button_color = (100, 200, 100)
    save_button_text = "Save Simulation"
    save_button_surface = font.render(save_button_text, True, (255, 255, 255))
    save_button_text_rect = save_button_surface.get_rect(center=save_button_rect.center)
    save_button_hovered = False
    
    # Cancel button
    cancel_button_rect = pygame.Rect(position[0] - 100, position[1] + 100, 200, 40)
    cancel_button_color = (200, 100, 100)
    cancel_button_text = "Cancel"
    cancel_button_surface = font.render(cancel_button_text, True, (255, 255, 255))
    cancel_button_text_rect = cancel_button_surface.get_rect(center=cancel_button_rect.center)
    cancel_button_hovered = False
    cancel_clicked_last_tick = False

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
                    
                    if cancel_button_rect.collidepoint(event.pos):
                        if cancel_clicked_last_tick:
                            saving_menu_visible = False
                        cancel_clicked_last_tick = True
                        cancel_button_text = "Confirm Cancel"
                    else:
                        cancel_clicked_last_tick = False
                        cancel_button_text = "Cancel"
                    cancel_button_surface = font.render(cancel_button_text, True, (255, 255, 255))
                    cancel_button_text_rect = cancel_button_surface.get_rect(center=cancel_button_rect.center)

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

        # Draw the save button
        if save_button_rect.collidepoint(pygame.mouse.get_pos()):
            save_button_hovered = True
        else:
            save_button_hovered = False
        pygame.draw.rect(screen, (save_button_color if not save_button_hovered else (80, 180, 80)) if input_text else (40, 60, 40), save_button_rect, border_radius=5)
        screen.blit(save_button_surface, save_button_text_rect)

        # Draw the cancel button
        if cancel_button_rect.collidepoint(pygame.mouse.get_pos()):
            cancel_button_hovered = True
        else:
            cancel_button_hovered = False
        pygame.draw.rect(screen, cancel_button_color if not cancel_button_hovered else (180, 80, 80), cancel_button_rect, border_radius=5)
        screen.blit(cancel_button_surface, cancel_button_text_rect)

        # Check if save button is clicked
        if save_button_hovered and pygame.mouse.get_pressed()[0]:
            if input_text:
                # Here you would save the simulation with the name in input_text
                with open(f"saves/{input_text}.sim", "wb") as f:
                    pickle.dump(main_simulation, f)
                saving_menu_visible = False

        pygame.display.flip()
        clock.tick(FPS)