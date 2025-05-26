import pygame
import math
from config import *
from menu import Menu
from elements.element import Element

class NotGate(Element):
    def __init__(self, screen, pos):
        super().__init__(screen, pos)

        self.wire_connectors = [((-NOT_GATE_IMAGE.get_width() // 5, 0), True), ((NOT_GATE_IMAGE.get_width() // 4, 0), False)] # (pos, is_input)

    def draw(self):
        # Draw NOT_GATE_IMAGE
        self.screen.blit(NOT_GATE_IMAGE if self.state else NOT_GATE_OFF_IMAGE, (self.pos[0] - NOT_GATE_IMAGE.get_width() // 2, self.pos[1] - NOT_GATE_IMAGE.get_height() // 2))

        # Draw the wire connectors
        self.draw_wire_connectors()

    def update(self):
        self.state = 0 # Reset the state of the element
        
        # Update the state of the element based on the input elements
        for wire in self.input_wires:
            connector_index = wire.ending_index if wire.ending_element == self else wire.initial_index

            # If the wire is not connected to one of the input connectors, skip it
            if not self.wire_connectors[connector_index][1]:
                continue

            # If the wire is active, set the not gate's output to False
            if wire.get_state(self):
                self.state = 0
                return
            
        # If the input is False, set the not gate's output to True
        self.state = True

    # Return True if the element was clicked
    def handle_click(self, mouse_pos):
        # Check if the mouse is over the element
        image_rect = NOT_GATE_IMAGE.get_rect(center=(self.pos[0], self.pos[1]))
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
        new_element = NotGate(self.screen, mouse_pos)
        return new_element