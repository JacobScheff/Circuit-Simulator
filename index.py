import pygame
import math
from menu import Menu
from input import Input

SCREEN_SIZE = (1200, 600)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Circuit Simualtor")
clock = pygame.time.Clock()
FPS = 60
running = True

menus = []
inputs = []

def auto_close_menus_from_click():
    for menu in menus:
        if not menu.bg_rect.collidepoint(mos_pos) and menu.close_on_click:
            menus.remove(menu)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                mouse_pos = pygame.mouse.get_pos()
                inputs.append(Input(screen, mouse_pos, 0))
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mos_pos = pygame.mouse.get_pos()

            # Left mouse button clicked
            if event.button == 1:
                # Handle menu
                for menu in menus:
                    # If handle_click returns True, close the menu
                    if menu.handle_click(mos_pos):
                        menus.remove(menu)
                        break

                # Handle input
                for input in inputs:
                    input.handle_click(mos_pos)

                # Close menus if clicked outside of them
                auto_close_menus_from_click()

            # Right mouse button clicked (context menu)
            elif event.button == 3:
                # Handle input
                for input in inputs:
                    if input.rect.collidepoint(mos_pos):
                        menu = input.handle_menu_create(mos_pos)
                        if menu is not None:
                            menus.append(menu)
                        break
                
                # Close menus if clicked outside of them
                auto_close_menus_from_click()

    screen.fill((0, 0, 0))
    
    # Draw the inputs
    for input in inputs:
        input.draw()

    # Draw the menus
    for menu in menus:
        menu.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()