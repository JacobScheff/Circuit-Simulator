import pygame
import math
from config import *
from menu import Menu

class AndGate:
    def __init__(self, screen, pos):
        self.screen = screen
        self.pos = pos
        self.state = False
        self.wire_connectors = [((self.pos[0] - OR_GATE_IMAGE.get_width() // 6, self.pos[1] - OR_GATE_IMAGE.get_height() // 5), True), ((self.pos[0] - OR_GATE_IMAGE.get_width() // 6, self.pos[1] + OR_GATE_IMAGE.get_height() // 5), True), ((self.pos[0] + OR_GATE_IMAGE.get_width() // 5, self.pos[1]), False)] # (pos, is_input)
        self.input_wires = [] # List of wires that connect to this light
        self.deleted = False # Whether to delete the element next frame

    def draw(self):
        # Draw a gray circle
        pygame.draw.circle(self.screen, (192, 192, 192)if not self.state else (255, 255, 255), self.pos, 20)

        # Draw the wire connectors
        for connector in self.wire_connectors:
            pygame.draw.circle(self.screen, (0, 0, 255), connector[0], WIRE_CONNECOR_RADIUS)

    def update(self):
        self.state = False # Reset the state of the light bulb

        first_input = False
        second_input = False
        
        # Update the state of the light bulb based on the input elements
        for wire in self.input_wires:
            connector_index = wire.ending_index if wire.ending_element == self else wire.initial_index

            # If the wire is not connected to one of the input connectors, skip it
            if not self.wire_connectors[connector_index][1]:
                continue

            # If the wire is active, set the light bulb's state to True
            if wire.state and connector_index == 0:
                first_input = True
            elif wire.state and connector_index == 1:
                second_input = True

        # If both inputs are True, set the light bulb's state to True
        if first_input and second_input:
            self.state = True

    def set_pos(self, pos):
        # Set the position of the light bulb
        self.pos = pos
        self.wire_connectors[0] = ((self.pos[0] - OR_GATE_IMAGE.get_width() // 6, self.pos[1] - OR_GATE_IMAGE.get_height() // 5), True)
        self.wire_connectors[1] = ((self.pos[0] - OR_GATE_IMAGE.get_width() // 6, self.pos[1] + OR_GATE_IMAGE.get_height() // 5), True)
        self.wire_connectors[2] = ((self.pos[0] + OR_GATE_IMAGE.get_width() // 5, self.pos[1]), False)

    # Return True if the light bulb was clicked
    def handle_click(self, mouse_pos):
        # TODO
        return False

    def handle_menu_create(self, mouse_pos):
        # Check if the or gate is clicked
        if False: # TODO: Check if clicked
            def delete_input():
                self.deleted = True
                return True # Close the menu after deleting the input
            
            menu = Menu(self.screen, mouse_pos, ["Delete"], [delete_input])
            return menu
        
    def create_new_element(self, mouse_pos):
        new_element = AndGate(self.screen, mouse_pos)
        return new_element