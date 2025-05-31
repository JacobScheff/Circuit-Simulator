import pygame
import math
from config import *
from new_element import *
from wire import *
from elements import *

class Simulation:
    def __init__(self, screen, element_types, element_names, num_inputs):
        self.screen = screen

        self.menus = [] # List of menus that are currently open
        self.wires = []
        self.elements = [[] for _ in range(len(element_types))]
        self.adding_wire = False
        self.wire_connectors_selected = []
        self.new_element_menu_visible = False
        self.mos_pos = (0, 0) # Mouse position
        self.adding_element = -1 # -1 means no adding element selected, >0 is index of sample_elements
        self.something_clicked = False
        self.wire_connected = False
        self.paused = False

        self.new_element_button = NewElementButton(screen, (30, 30), 20, 10)
        self.sample_elements = [element(screen, (0, 0)) for element in element_types]
        self.element_types = element_types
        self.element_names = element_names
        self.inputs = [Input(screen, (INPUT_SIZE[0] / 2, screen.get_height() / (num_inputs + 1) * (i + 1))) for i in range(num_inputs)] # List of inputs for each element type

    # Returns the list that the element belongs to
    def element_to_list(self, element):
        for i in range(len(self.element_types)):
            if isinstance(element, self.element_types[i]):
                return self.elements[i]
        raise ValueError("Element not found in any list")
    
    def auto_close_menus_from_click(self):
        for menu in self.menus:
            if not menu.bg_rect.collidepoint(self.mos_pos) and menu.close_on_click:
                menu.closing_callback()
                self.menus.remove(menu)

    # Runs when the new element button is clicked or w key is pressed
    def create_new_element_menu(self):
        something_clicked = True
        selected_functions = [] # The functions to run when the menu button is clicked
    
        # Wire selected
        def wire_selected():
            self.adding_wire = True
            return True
        selected_functions.append(wire_selected)
    
        # Element selected
        for i in range(len(self.element_types)):
            def element_selected_function(i):
                self.adding_element = i
                return True
            selected_functions.append(lambda i=i: element_selected_function(i))
            def set_new_element_visible_to_false():
                self.new_element_menu_visible = False
        menu = Menu(self.screen, self.mos_pos, ["Wire"] + self.element_names, selected_functions, True, set_new_element_visible_to_false)
        self.menus.append(menu)
        self.new_element_menu_visible = True
    
    # Updates the simulation state by a single tick
    def tick(self):
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
                    if self.adding_element == -1 and not self.adding_wire and not self.new_element_menu_visible:
                        self.create_new_element_menu()
                # Space key pressed, toggle pause
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                # Escape key pressed, close all menus
                elif event.key == pygame.K_ESCAPE:
                    self.menus.clear()
                    adding_element = -1
                    self.adding_wire = False
                    # If an element is selcted for wire connection and second isn't selected, remove the first one
                    if len(self.wire_connectors_selected) % 2 == 1:
                        self.wire_connectors_selected.pop()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Not adding a wire
                if not self.adding_wire:
                    # Left mouse button clicked
                    if event.button == 1:
                        something_clicked = False
                        # Handle menu
                        for menu in self.menus:
                            # If handle_click returns True, close the menu
                            if menu.handle_click(mos_pos):
                                something_clicked = True
                                menu.closing_callback()
                                self.menus.remove(menu)
                                break

                        # Handle elements
                        for elements_list in self.elements:
                            for element in elements_list:
                                # If handle_click returns True, close the menu
                                something_clicked = element.handle_click(mos_pos) or something_clicked

                        # Handle inputs
                        for input_element in self.inputs:
                            # If handle_click returns True, close the menu
                            something_clicked = input_element.handle_click(mos_pos) or something_clicked

                        # Handle new element button
                        if self.new_element_button.collidepoint(mos_pos):
                            self.create_new_element_menu()

                        # Close menus if clicked outside of them
                        self.auto_close_menus_from_click()

                        # If nothing was clicked, and adding_element is not -1, create a new element
                        if not something_clicked and self.adding_element >= 0:
                            # Create a new element
                            new_element = self.sample_elements[self.adding_element].create_new_element(mos_pos)
                            self.elements[self.adding_element].append(new_element)

                            # Reset adding_element
                            self.adding_element = -1

                    # Right mouse button clicked (context menu)
                    elif event.button == 3:
                        # Handle wire
                        for wire in self.wires:
                            if wire.handle_click(mos_pos):
                                menu = wire.handle_menu_create(mos_pos)
                                if menu is not None:
                                    self.menus.append(menu)
                                break

                        # Handle elements
                        for elements_list in self.elements:
                            for element in elements_list:
                                if element.handle_click(mos_pos):
                                    menu = element.handle_menu_create(mos_pos)
                                    if menu is not None:
                                        self.menus.append(menu)
                                    break
                                
                        # Close menus if clicked outside of them
                        self.auto_close_menus_from_click()
                else:
                    self.wire_connected = False
                    # Left mouse button clicked
                    if event.button == 1:
                        # Handle wire creation
                        def check_wire_connects(element):
                            # Check if wire was already connected
                            if self.wire_connected:
                                return

                            # Check to make sure the second selected connection isn't the same as the first
                            if len(self.wire_connectors_selected) % 2 == 1:
                                if element == self.wire_connectors_selected[-1][0]:
                                    return

                            # Determine if any wires are connected
                            connectors = element.wire_connectors
                            for i in range(len(connectors)):
                                if not self.wire_connected and math.hypot(element.pos[0] + connectors[i][0][0] - mos_pos[0], element.pos[1] + connectors[i][0][1] - mos_pos[1]) < WIRE_CONNECOR_RADIUS:
                                    self.wire_connected = True
                                    self.wire_connectors_selected.append((element, i))

                        # Check if the mouse is over the wire connector of any element
                        for elements_list in self.elements:
                            for element in elements_list:
                                check_wire_connects(element)

                        # Check if the mouse is over the wire connector of any input
                        for input_element in self.inputs:
                            check_wire_connects(input_element)

                        if self.wire_connected and len(self.wire_connectors_selected) % 2 == 0:
                            self.wires.append(Wire(self.screen, self.wire_connectors_selected[-2][0], self.wire_connectors_selected[-2][1], self.wire_connectors_selected[-1][0], self.wire_connectors_selected[-1][1]))
                            self.adding_wire = False

                            # Add the wire to the elements' input_wires list
                            self.wire_connectors_selected[-2][0].input_wires.append(self.wires[-1])
                            self.wire_connectors_selected[-1][0].input_wires.append(self.wires[-1])

        # Remove deleted elements
        for element_list in self.elements:
            for element in element_list:
                if element.deleted:
                    # Remove the element from the wires' input_wires list
                    for wire in self.wires:
                            wire.delete()
                    element_list.remove(element)
                    break # Can break since user can only delete one element at a time
        # Remove deleted wires - Wire is at end since the elements need to remove references to it first
        for wire in self.wires:
            if wire.deleted:
                wire.delete()
                self.wires.remove(wire)
                break

        # Clear the screen
        self.screen.fill((0, 0, 0))

        # If shift is held down, draw the grid with gridsize
        if shift:
            for i in range(0, SCREEN_SIZE[0], GRID_SIZE):
                pygame.draw.line(self.screen, (50, 50, 50), (i, 0), (i, SCREEN_SIZE[1]))
            for i in range(0, SCREEN_SIZE[1], GRID_SIZE):
                pygame.draw.line(self.screen, (50, 50, 50), (0, i), (SCREEN_SIZE[0], i))

        # Update the wires' states
        for wire in self.wires:
            wire.update(self.paused)

        # Update the elements' states
        for elements_list in self.elements:
            for element in elements_list:
                element.update()

        # Draw the wires
        for wire in self.wires:
            wire.draw()

        # Draw the elements
        for elements_list in self.elements:
            for element in elements_list:
                element.draw()

        # Draw the inputs
        for input_element in self.inputs:
            input_element.draw()

        # Draw the selected wire connectors
        if len(self.wire_connectors_selected) % 2 == 1:
            last_connected_element_pos = self.wire_connectors_selected[-1][0].pos
            last_connected_connector_pos = self.wire_connectors_selected[-1][0].wire_connectors[self.wire_connectors_selected[-1][1]][0]
            pygame.draw.circle(self.screen, (255, 0, 0), (last_connected_element_pos[0] + last_connected_connector_pos[0], last_connected_element_pos[1] + last_connected_connector_pos[1]), WIRE_CONNECOR_RADIUS)

        # Draw the new element button
        self.new_element_button.draw()

        # Draw the menus
        for menu in self.menus:
            menu.draw()

        # Draw the selected element at mos_pos
        if self.adding_element >= 0:
            element = self.sample_elements[self.adding_element]
            element.set_pos(mos_pos)
            element.draw()

        # Draw a wire icon at mos_pos if adding a wire and no element is selected yet
        if self.adding_wire and len(self.wire_connectors_selected) % 2 == 0:
            pygame.draw.rect(self.screen, (255, 255, 255), (mos_pos[0] - WIRE_CONNECOR_RADIUS / 2, mos_pos[1] - WIRE_CONNECOR_RADIUS / 2, WIRE_CONNECOR_RADIUS, WIRE_CONNECOR_RADIUS))

        # Draw a wire from selected element to mouse position if adding a wire and only first element is selected
        if self.adding_wire and len(self.wire_connectors_selected) % 2 == 1:
            last_connected_element_pos = self.wire_connectors_selected[-1][0].pos
            last_connected_connector_pos = self.wire_connectors_selected[-1][0].wire_connectors[self.wire_connectors_selected[-1][1]][0]
            pygame.draw.line(self.screen, (255, 255, 255), (last_connected_element_pos[0] + last_connected_connector_pos[0], last_connected_element_pos[1] + last_connected_connector_pos[1]), mos_pos, WIRE_WIDTH)

    # # Render the simulation state to the screen
    # def render(self, screen):
        