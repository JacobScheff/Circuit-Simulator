import pygame
import math
from config import *
from menu import Menu
from elements.element import Element

class XorGate(Element):
    def __init__(self, screen, pos):
        super().__init__(screen, pos)
        
        self.wire_connectors = [((-XOR_GATE_IMAGE.get_width() // 4, -XOR_GATE_IMAGE.get_height() // 5), True), ((-XOR_GATE_IMAGE.get_width() // 4, XOR_GATE_IMAGE.get_height() // 5), True), ((XOR_GATE_IMAGE.get_width() // 5, 0), False)] # (pos, is_input)

    def draw(self):
        # Draw XOR_GATE_IMAGE
        self.screen.blit(XOR_GATE_IMAGE if self.state else XOR_GATE_OFF_IMAGE, (self.pos[0] - XOR_GATE_IMAGE.get_width() // 2, self.pos[1] - XOR_GATE_IMAGE.get_height() // 2))

        # Draw the wire connectors
        self.draw_wire_connectors()

    def update(self):
        first_input = False
        second_input = False
        
        # Update the state of the element based on the input elements
        for wire in self.input_wires:
            connector_index = wire.ending_index if wire.ending_element == self else wire.initial_index

            # If the wire is not connected to one of the input connectors, skip it
            if not self.wire_connectors[connector_index][1]:
                continue

            # If the wire is active, set the element's state to True
            wire_state = wire.get_state(self)
            if wire_state and connector_index == 0:
                first_input = True
            elif wire_state and connector_index == 1:
                second_input = True

        # If both inputs are the same, set the element's state to 0
        if first_input is second_input:
            self.state = 0
        else:
            self.state = 1

    # Return True if the element was clicked
    def handle_click(self, mouse_pos):
        # Check if the mouse is over the element
        image_rect = XOR_GATE_IMAGE.get_rect(center=(self.pos[0], self.pos[1]))
        if image_rect.collidepoint(mouse_pos):
            return True
        
        return False

    def handle_menu_create(self, mouse_pos):
        # Check if the or gate is clicked
        if self.handle_click(mouse_pos):
            def delete_input():
                self.deleted = True
                return True # Close the menu after deleting the input
            
            menu = Menu(self.screen, mouse_pos, ["Delete"], [delete_input])
            return menu
        
    def create_new_element(self, mouse_pos):
        new_element = XorGate(self.screen, mouse_pos)
        return new_element