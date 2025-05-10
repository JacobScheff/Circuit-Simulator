import pygame
import math
from config import *
from menu import Menu
from elements.element import Element

class Light(Element):
    def __init__(self, screen, pos):
        super().__init__(screen, pos)

        self.wire_connectors = [((pos[0] - LIGHT_RADIUS, pos[1]), True), ((pos[0] + LIGHT_RADIUS, pos[1]), False)]

    def draw(self):
        # Draw the light bulb
        color = (255, 255, 0) if self.state else (100, 100, 100)
        pygame.draw.circle(self.screen, color, self.pos, LIGHT_RADIUS)

        # Draw the wire connectors
        pygame.draw.circle(self.screen, (0, 0, 255), self.wire_connectors[0][0], WIRE_CONNECOR_RADIUS)
        pygame.draw.circle(self.screen, (0, 0, 255), self.wire_connectors[1][0], WIRE_CONNECOR_RADIUS)

    def update(self):
        self.state = 0 # Reset the state of the light bulb
        
        # Update the state of the light bulb based on the input elements
        for wire in self.input_wires:
            connector_index = wire.ending_index if wire.ending_element == self else wire.initial_index

            # If the wire is not connected to this light bulb's input connector, skip it
            if not self.wire_connectors[connector_index][1]:
                continue

            # If the wire is active, set the light bulb's state to True
            if wire.state:
                self.state = True
                return
    
    def set_pos(self, pos):
        # Set the position of the light bulb
        self.pos = pos
        self.wire_connectors[0] = ((pos[0] - LIGHT_RADIUS, pos[1]), True)
        self.wire_connectors[1] = ((pos[0] + LIGHT_RADIUS, pos[1]), False)

    # Return True if the light bulb was clicked
    def handle_click(self, mouse_pos):
        if math.hypot(self.pos[0] - mouse_pos[0], self.pos[1] - mouse_pos[1]) < LIGHT_RADIUS:
            return True
        return False

    def handle_menu_create(self, mouse_pos):
        # Check if the light is clicked
        if math.hypot(self.pos[0] - mouse_pos[0], self.pos[1] - mouse_pos[1]) < LIGHT_RADIUS:
            def delete_input():
                self.deleted = True
                return True # Close the menu after deleting the input
            
            menu = Menu(self.screen, mouse_pos, ["Delete"], [delete_input])
            return menu
        
    def create_new_element(self, mouse_pos):
        new_element = Light(self.screen, mouse_pos)
        return new_element