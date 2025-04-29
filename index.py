import pygame
import math
from menu import Menu
from new_element import NewElementButton
from input import Input
from wire import Wire

SCREEN_SIZE = (1200, 600)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Circuit Simualtor")
clock = pygame.time.Clock()
FPS = 60
running = True

menus = []
inputs = []
new_element_button = NewElementButton(screen, (30, 30), 20, 10)

sample_elements = [Input(screen, (100, 100), 0)]
adding_element = -1 # -1 means no adding element selected, >0 is index of sample_elements

def auto_close_menus_from_click():
    for menu in menus:
        if not menu.bg_rect.collidepoint(mos_pos) and menu.close_on_click:
            menus.remove(menu)

while running:
    mos_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                mouse_pos = pygame.mouse.get_pos()
                inputs.append(Input(screen, mouse_pos, 0))
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Left mouse button clicked
            if event.button == 1:
                something_clicked = False
                # Handle menu
                for menu in menus:
                    # If handle_click returns True, close the menu
                    if menu.handle_click(mos_pos):
                        something_clicked = True
                        menus.remove(menu)
                        break

                # Handle input
                for input in inputs:
                    something_clicked = input.handle_click(mos_pos) or something_clicked

                # Handle new element button
                if new_element_button.collidepoint(mos_pos):
                    something_clicked = True
                    def input_selected():
                        global adding_element
                        adding_element = 0
                        return True
                    menu = Menu(screen, mos_pos, ["Input"], [input_selected])
                    menus.append(menu)

                # Close menus if clicked outside of them
                auto_close_menus_from_click()

                # If nothing was clicked, and adding_element is not -1, create a new element
                if not something_clicked and adding_element >= 0:
                    # Create a new element
                    new_element = sample_elements[adding_element].create_new_element(mos_pos)
                    inputs.append(new_element)

                    # Reset adding_element
                    adding_element = -1

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

    # Remove deleted elements
    for input in inputs:
        if input.deleted:
            inputs.remove(input)
            break

    screen.fill((0, 0, 0))
    
    # Draw the inputs
    for input in inputs:
        input.draw()

    # Draw the new element button
    new_element_button.draw()

    # Draw the menus
    for menu in menus:
        menu.draw()

    # Draw the selected element at mos_pos
    if adding_element >= 0:
        element = sample_elements[adding_element]
        element.set_pos(mos_pos)
        element.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()