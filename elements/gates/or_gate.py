import pygame
import math
from config import *
from menu import Menu
from elements.element import Element

class OrGate(Element):
    def __init__(self, screen, pos):
        super().__init__(screen, pos)
        
        self.wire_connectors = [((self.pos[0] - OR_GATE_IMAGE.get_width() // 6, self.pos[1] - OR_GATE_IMAGE.get_height() // 5), True), ((self.pos[0] - OR_GATE_IMAGE.get_width() // 6, self.pos[1] + OR_GATE_IMAGE.get_height() // 5), True), ((self.pos[0] + OR_GATE_IMAGE.get_width() // 5, self.pos[1]), False)] # (pos, is_input)

    def draw(self):
        # Draw OR_GATE_IMAGE
        self.screen.blit(OR_GATE_IMAGE if self.state else OR_GATE_OFF_IMAGE, (self.pos[0] - OR_GATE_IMAGE.get_width() // 2, self.pos[1] - OR_GATE_IMAGE.get_height() // 2))

        # Draw the wire connectors
        for connector in self.wire_connectors:
            pygame.draw.circle(self.screen, (0, 0, 255), connector[0], WIRE_CONNECOR_RADIUS)

    def update(self):
        self.state = 0 # Reset the state of the element
        
        # Update the state of the element based on the input elements
        for wire in self.input_wires:
            connector_index = wire.ending_index if wire.ending_element == self else wire.initial_index

            # If the wire is not connected to one of the input connectors, skip it
            if not self.wire_connectors[connector_index][1]:
                continue

            # If the wire is active, set the element's state to True
            if wire.state:
                self.state = True
                return

    def set_pos(self, pos):
        # Set the position of the element
        self.pos = pos
        self.wire_connectors[0] = ((self.pos[0] - OR_GATE_IMAGE.get_width() // 6, self.pos[1] - OR_GATE_IMAGE.get_height() // 5), True)
        self.wire_connectors[1] = ((self.pos[0] - OR_GATE_IMAGE.get_width() // 6, self.pos[1] + OR_GATE_IMAGE.get_height() // 5), True)
        self.wire_connectors[2] = ((self.pos[0] + OR_GATE_IMAGE.get_width() // 5, self.pos[1]), False)

    # Return True if the element was clicked
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
        new_element = OrGate(self.screen, mouse_pos)
        return new_element