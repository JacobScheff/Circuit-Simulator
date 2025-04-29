import pygame
import math
from menu import Menu
from new_element import NewElementButton
from input import Input
from wire import Wire
from light import Light

SCREEN_SIZE = (1200, 600)
GRID_SIZE = 25 # Grid size when grid is enabled

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Circuit Simualtor")
clock = pygame.time.Clock()
FPS = 60
running = True

menus = []
inputs = []
lights = []
new_element_button = NewElementButton(screen, (30, 30), 20, 10)

sample_elements = [Input(screen, (100, 100), 0), Light(screen, (100, 100))]
adding_element = -1 # -1 means no adding element selected, >0 is index of sample_elements

def auto_close_menus_from_click():
    for menu in menus:
        if not menu.bg_rect.collidepoint(mos_pos) and menu.close_on_click:
            menus.remove(menu)

while running:
    # Check if shift is held down
    shift = pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]

    # Get the mouse position
    mos_pos = pygame.mouse.get_pos()

    # If shift is held down, snap the mouse position to the grid
    if shift:
        mos_pos = (math.floor(mos_pos[0] / GRID_SIZE) * GRID_SIZE, math.floor(mos_pos[1] / GRID_SIZE) * GRID_SIZE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
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

                # Handle light
                for light in lights:
                    something_clicked = light.handle_click(mos_pos) or something_clicked

                # Handle new element button
                if new_element_button.collidepoint(mos_pos):
                    something_clicked = True
                    def input_selected():
                        global adding_element
                        adding_element = 0
                        return True
                    def light_selected():
                        global adding_element
                        adding_element = 1
                        return True
                    menu = Menu(screen, mos_pos, ["Input", "Light"], [input_selected, light_selected])
                    menus.append(menu)

                # Close menus if clicked outside of them
                auto_close_menus_from_click()

                # If nothing was clicked, and adding_element is not -1, create a new element
                if not something_clicked and adding_element >= 0:
                    # Create a new element
                    new_element = sample_elements[adding_element].create_new_element(mos_pos)
                    if adding_element == 0:
                        inputs.append(new_element)
                    elif adding_element == 1:
                        lights.append(new_element)

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
                # Handle light
                for light in lights:
                    if light.handle_click(mos_pos):
                        menu = light.handle_menu_create(mos_pos)
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
    for light in lights:
        if light.deleted:
            lights.remove(light)
            break

    # Clear the screen
    screen.fill((0, 0, 0))

    # If shift is held down, draw the grid with gridsize
    if shift:
        for i in range(0, SCREEN_SIZE[0], GRID_SIZE):
            pygame.draw.line(screen, (50, 50, 50), (i, 0), (i, SCREEN_SIZE[1]))
        for i in range(0, SCREEN_SIZE[1], GRID_SIZE):
            pygame.draw.line(screen, (50, 50, 50), (0, i), (SCREEN_SIZE[0], i))
    
    # Draw the inputs
    for input in inputs:
        input.draw()

    # Draw the lights
    for light in lights:
        light.draw()

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