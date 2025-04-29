import pygame
import math
from config import *
from menu import Menu
from new_element import NewElementButton
from input import Input
from wire import Wire
from light import Light

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Circuit Simualtor")
clock = pygame.time.Clock()
running = True
adding_wire = False
wire_connectors_selected = []

menus = []
wires = []
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

        if event.type == pygame.KEYDOWN:
            # Escape key pressed, close all menus
            if event.key == pygame.K_ESCAPE:
                menus.clear()
                adding_element = -1
                adding_wire = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:

            # Not adding a wire
            if not adding_wire:
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
                        def wire_selected():
                            adding_wire = True
                            return True
                        def input_selected():
                            global adding_element
                            adding_element = 0
                            return True
                        def light_selected():
                            global adding_element
                            adding_element = 1
                            return True
                        menu = Menu(screen, mos_pos, ["Wire", "Input", "Light"], [wire_selected, input_selected, light_selected])
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
            else:
                wire_conncted = False
                # Left mouse button clicked
                if event.button == 1:
                    # Handle wire creation
                    def check_wire_connects(element):
                        # Check if wire was already connected
                        if wire_conncted:
                            return
                        
                        # Determine if any wires are connected
                        connectors = element.wire_connectors
                        for i in range(len(connectors)):
                            if connectors[i].collidepoint(mos_pos) and not wire_conncted:
                                wire_conncted = True
                                wire_connectors_selected.append((input, i))

                    for input in inputs:
                        check_wire_connects(input)
                    for light in lights:
                        check_wire_connects(light)
                        
                    if wire_conncted and len(wire_connectors_selected) >= 2:
                        wires.append(Wire(screen, wire_connectors_selected[0], wire_connectors_selected[1]))
                        wire_connectors_selected.clear()
                        adding_wire = False

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