import pygame
import math
from config import *
from menu import Menu
from new_element import NewElementButton
from wire import Wire
from elements import *

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Circuit Simulator")
clock = pygame.time.Clock()
running = True
adding_wire = False
wire_connectors_selected = []

# Create gate off images
OR_GATE_OFF_IMAGE.fill((80, 80, 80, 255), None, pygame.BLEND_RGBA_MULT)
AND_GATE_OFF_IMAGE.fill((80, 80, 80, 255), None, pygame.BLEND_RGBA_MULT)
NOT_GATE_OFF_IMAGE.fill((80, 80, 80, 255), None, pygame.BLEND_RGBA_MULT)

menus = []
wires = []
inputs = []
lights = []
or_gates = []
and_gates = []
not_gates = []
new_element_button = NewElementButton(screen, (30, 30), 20, 10)

sample_elements = [Input(screen, (100, 100)), Light(screen, (100, 100)), OrGate(screen, (100, 100)), AndGate(screen, (100, 100)), NotGate(screen, (100, 100))]
adding_element = -1 # -1 means no adding element selected, >0 is index of sample_elements

def auto_close_menus_from_click():
    for menu in menus:
        if not menu.bg_rect.collidepoint(mos_pos) and menu.close_on_click:
            menus.remove(menu)

while running:
    # Check if shift is held down
    shift = pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]
print("TODO!!!!! Modify write connectors to represent offsets, not global positions")
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
                # If an element is selcted for wire connection and second isn't selected, remove the first one
                if len(wire_connectors_selected) % 2 == 1:
                    wire_connectors_selected.pop()
        
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

                    # Handle new element button
                    if new_element_button.collidepoint(mos_pos):
                        something_clicked = True
                        def wire_selected():
                            global adding_wire
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
                        def or_selected():
                            global adding_element
                            adding_element = 2
                            return True
                        def and_selected():
                            global adding_element
                            adding_element = 3
                            return True
                        def not_selected():
                            global adding_element
                            adding_element = 4
                            return True
                        menu = Menu(screen, mos_pos, ["Wire", "Input", "Light", "Or", "And", "Not"], [wire_selected, input_selected, light_selected, or_selected, and_selected, not_selected])
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
                        elif adding_element == 2:
                            or_gates.append(new_element)
                        elif adding_element == 3:
                            and_gates.append(new_element)
                        elif adding_element == 4:
                            not_gates.append(new_element)

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
                    # Handle wire
                    for wire in wires:
                        if wire.handle_click(mos_pos):
                            menu = wire.handle_menu_create(mos_pos)
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
                    # Handle or
                    for or_gate in or_gates:
                        if or_gate.handle_click(mos_pos):
                            menu = or_gate.handle_menu_create(mos_pos)
                            if menu is not None:
                                menus.append(menu)
                            break

                    # Handle and
                    for and_gate in and_gates:
                        if and_gate.handle_click(mos_pos):
                            menu = and_gate.handle_menu_create(mos_pos)
                            if menu is not None:
                                menus.append(menu)
                            break

                    # Handle not
                    for not_gate in not_gates:
                        if not_gate.handle_click(mos_pos):
                            menu = not_gate.handle_menu_create(mos_pos)
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
                        global wire_conncted
                        # Check if wire was already connected
                        if wire_conncted:
                            return
                        
                        # Check to make sure the second selected connection isn't the same as the first
                        if len(wire_connectors_selected) % 2 == 1:
                            if element == wire_connectors_selected[-1][0]:
                                return
                        
                        # Determine if any wires are connected
                        connectors = element.wire_connectors
                        for i in range(len(connectors)):
                            if not wire_conncted and math.hypot(connectors[i][0][0] - mos_pos[0], connectors[i][0][1] - mos_pos[1]) < WIRE_CONNECOR_RADIUS:
                                wire_conncted = True
                                wire_connectors_selected.append((element, i))

                    for input in inputs:
                        check_wire_connects(input)
                    for light in lights:
                        check_wire_connects(light)
                    for or_gate in or_gates:
                        check_wire_connects(or_gate)
                    for and_gate in and_gates:
                        check_wire_connects(and_gate)
                    for not_gate in not_gates:
                        check_wire_connects(not_gate)
                        
                    if wire_conncted and len(wire_connectors_selected) % 2 == 0:
                        wires.append(Wire(screen, wire_connectors_selected[-2][0], wire_connectors_selected[-2][1], wire_connectors_selected[-1][0], wire_connectors_selected[-1][1]))
                        adding_wire = False

                        # Add the wire to the elements' input_wires list
                        wire_connectors_selected[-2][0].input_wires.append(wires[-1])
                        wire_connectors_selected[-1][0].input_wires.append(wires[-1])

    # Remove deleted elements
    for input in inputs:
        if input.deleted:
            for wire in input.input_wires:
                wire.delete()
            inputs.remove(input)
            break
    for light in lights:
        if light.deleted:
            for wire in light.input_wires:
                wire.delete()
            lights.remove(light)
            break
    for or_gate in or_gates:
        if or_gate.deleted:
            for wire in or_gate.input_wires:
                wire.delete()
            or_gates.remove(or_gate)
            break
    for and_gate in and_gates:
        if and_gate.deleted:
            for wire in and_gate.input_wires:
                wire.delete()
            and_gates.remove(and_gate)
            break
    for not_gate in not_gates:
        if not_gate.deleted:
            for wire in not_gate.input_wires:
                wire.delete()
            not_gates.remove(not_gate)
            break
    # Wire is at end since the elements need to remove references to it first
    for wire in wires:
        if wire.deleted:
            wire.delete()
            wires.remove(wire)
            break

    # Clear the screen
    screen.fill((0, 0, 0))

    # If shift is held down, draw the grid with gridsize
    if shift:
        for i in range(0, SCREEN_SIZE[0], GRID_SIZE):
            pygame.draw.line(screen, (50, 50, 50), (i, 0), (i, SCREEN_SIZE[1]))
        for i in range(0, SCREEN_SIZE[1], GRID_SIZE):
            pygame.draw.line(screen, (50, 50, 50), (0, i), (SCREEN_SIZE[0], i))
    
    # Update the wires' states
    for wire in wires:
        wire.update()

    # Update the elements' states
    for input in inputs:
        input.update()
    for light in lights:
        light.update()
    for or_gate in or_gates:
        or_gate.update()
    for and_gate in and_gates:
        and_gate.update()
    for not_gate in not_gates:
        not_gate.update()

    # Draw the wires
    for wire in wires:
        wire.draw()

    # Draw the inputs
    for input in inputs:
        input.draw()
    # Draw the lights
    for light in lights:
        light.draw()
    # Draw the or gates
    for or_gate in or_gates:
        or_gate.draw()
    # Draw the and gates
    for and_gate in and_gates:
        and_gate.draw()
    # Draw the not gates
    for not_gate in not_gates:
        not_gate.draw()

    # Draw the selected wire connectors
    if len(wire_connectors_selected) % 2 == 1:
        pygame.draw.circle(screen, (255, 0, 0), wire_connectors_selected[-1][0].wire_connectors[wire_connectors_selected[-1][1]][0], WIRE_CONNECOR_RADIUS, 5)

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

    # Draw a wire icon at mos_pos if adding a wire and no element is selected yet
    if adding_wire and len(wire_connectors_selected) % 2 == 0:
        pygame.draw.rect(screen, (255, 255, 255), (mos_pos[0] - WIRE_CONNECOR_RADIUS / 2, mos_pos[1] - WIRE_CONNECOR_RADIUS / 2, WIRE_CONNECOR_RADIUS, WIRE_CONNECOR_RADIUS))

    # Draw a wire from selected element to mouse position if adding a wire and only first element is selected
    if adding_wire and len(wire_connectors_selected) % 2 == 1:
        pygame.draw.line(screen, (255, 255, 255), wire_connectors_selected[-1][0].wire_connectors[wire_connectors_selected[-1][1]][0], mos_pos, 5)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()