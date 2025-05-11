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
NOR_GATE_OFF_IMAGE.fill((80, 80, 80, 255), None, pygame.BLEND_RGBA_MULT)
AND_GATE_OFF_IMAGE.fill((80, 80, 80, 255), None, pygame.BLEND_RGBA_MULT)
NAND_GATE_OFF_IMAGE.fill((80, 80, 80, 255), None, pygame.BLEND_RGBA_MULT)
XOR_GATE_OFF_IMAGE.fill((80, 80, 80, 255), None, pygame.BLEND_RGBA_MULT)
XNOR_GATE_OFF_IMAGE.fill((80, 80, 80, 255), None, pygame.BLEND_RGBA_MULT)
NOT_GATE_OFF_IMAGE.fill((80, 80, 80, 255), None, pygame.BLEND_RGBA_MULT)

menus = []
wires = []

new_element_button = NewElementButton(screen, (30, 30), 20, 10)

element_types = [Input, Light, OrGate, AndGate, XorGate, NotGate, NorGate, NandGate, XnorGate]
element_names = ["Input", "Light", "Or", "And", "Xor", "Not", "Nor", "Nand", "Xnor"]
elements = [[] for _ in range(len(element_types))]
sample_elements = [element(screen, (0, 0)) for element in element_types]
adding_element = -1 # -1 means no adding element selected, >0 is index of sample_elements
new_element_menu_visible = False

# Returns the list that the element belongs to
def element_to_list(element):
    for i in range(len(element_types)):
        if isinstance(element, element_types[i]):
            return elements[i]
    raise ValueError("Element not found in any list")

def auto_close_menus_from_click():
    for menu in menus:
        if not menu.bg_rect.collidepoint(mos_pos) and menu.close_on_click:
            menu.closing_callback()
            menus.remove(menu)

# Runs when the new element button is clicked or w key is pressed
def create_new_element_menu():
    global adding_element
    global something_clicked
    global new_element_menu_visible
    something_clicked = True
    selected_functions = [] # The functions to run when the menu button is clicked

    # Wire selected
    def wire_selected():
        global adding_wire
        adding_wire = True
        return True
    selected_functions.append(wire_selected)

    # Element selected
    for i in range(len(element_types)):
        def element_selected_function(i):
            global adding_element
            adding_element = i
            return True
        selected_functions.append(lambda i=i: element_selected_function(i))
        def set_new_element_visible_to_false():
            global new_element_menu_visible
            new_element_menu_visible = False
    menu = Menu(screen, mos_pos, ["Wire"] + element_names, selected_functions, True, set_new_element_visible_to_false)
    menus.append(menu)
    new_element_menu_visible = True

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
            if event.key == pygame.K_w:
                # If the new element key is pressed, no element or wire is being added, and the create new element menu isn't visible, then create a new element menu
                if adding_element == -1 and not adding_wire and not new_element_menu_visible:
                    create_new_element_menu()
            elif event.key == pygame.K_ESCAPE:
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
                            menu.closing_callback()
                            menus.remove(menu)
                            break

                    # Handle elements
                    for elements_list in elements:
                        for element in elements_list:
                            # If handle_click returns True, close the menu
                            something_clicked = element.handle_click(mos_pos) or something_clicked

                    # Handle new element button
                    if new_element_button.collidepoint(mos_pos):
                        create_new_element_menu()

                    # Close menus if clicked outside of them
                    auto_close_menus_from_click()

                    # If nothing was clicked, and adding_element is not -1, create a new element
                    if not something_clicked and adding_element >= 0:
                        # Create a new element
                        new_element = sample_elements[adding_element].create_new_element(mos_pos)
                        elements[adding_element].append(new_element)

                        # Reset adding_element
                        adding_element = -1

                # Right mouse button clicked (context menu)
                elif event.button == 3:
                    # Handle wire
                    for wire in wires:
                        if wire.handle_click(mos_pos):
                            menu = wire.handle_menu_create(mos_pos)
                            if menu is not None:
                                menus.append(menu)
                            break

                    # Handle elements
                    for elements_list in elements:
                        for element in elements_list:
                            if element.handle_click(mos_pos):
                                menu = element.handle_menu_create(mos_pos)
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
                            if not wire_conncted and math.hypot(element.pos[0] + connectors[i][0][0] - mos_pos[0], element.pos[1] + connectors[i][0][1] - mos_pos[1]) < WIRE_CONNECOR_RADIUS:
                                wire_conncted = True
                                wire_connectors_selected.append((element, i))

                    # Check if the mouse is over the wire connector of any element
                    for elements_list in elements:
                        for element in elements_list:
                            check_wire_connects(element)
                        
                    if wire_conncted and len(wire_connectors_selected) % 2 == 0:
                        wires.append(Wire(screen, wire_connectors_selected[-2][0], wire_connectors_selected[-2][1], wire_connectors_selected[-1][0], wire_connectors_selected[-1][1]))
                        adding_wire = False

                        # Add the wire to the elements' input_wires list
                        wire_connectors_selected[-2][0].input_wires.append(wires[-1])
                        wire_connectors_selected[-1][0].input_wires.append(wires[-1])

    # Remove deleted elements
    for element_list in elements:
        for element in element_list:
            if element.deleted:
                # Remove the element from the wires' input_wires list
                for wire in wires:
                        wire.delete()
                element_list.remove(element)
                break # Can break since user can only delete one element at a time
    # Remove deleted wires - Wire is at end since the elements need to remove references to it first
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
    for elements_list in elements:
        for element in elements_list:
            element.update()

    # Draw the wires
    for wire in wires:
        wire.draw()

    # Draw the elements
    for elements_list in elements:
        for element in elements_list:
            element.draw()

    # Draw the selected wire connectors
    if len(wire_connectors_selected) % 2 == 1:
        last_connected_element_pos = wire_connectors_selected[-1][0].pos
        last_connected_connector_pos = wire_connectors_selected[-1][0].wire_connectors[wire_connectors_selected[-1][1]][0]
        pygame.draw.circle(screen, (255, 0, 0), (last_connected_element_pos[0] + last_connected_connector_pos[0], last_connected_element_pos[1] + last_connected_connector_pos[1]), WIRE_CONNECOR_RADIUS)

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
        last_connected_element_pos = wire_connectors_selected[-1][0].pos
        last_connected_connector_pos = wire_connectors_selected[-1][0].wire_connectors[wire_connectors_selected[-1][1]][0]
        pygame.draw.line(screen, (255, 255, 255), (last_connected_element_pos[0] + last_connected_connector_pos[0], last_connected_element_pos[1] + last_connected_connector_pos[1]), mos_pos, WIRE_WIDTH)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()