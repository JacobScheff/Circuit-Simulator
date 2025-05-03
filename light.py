import pygame
import math
from config import *
from menu import Menu

class Light:
    def __init__(self, screen, pos):
        self.screen = screen
        self.pos = pos
        self.radius = 30
        self.state = False
        self.wire_connectors = [(pos[0] - self.radius, pos[1]), (pos[0] + self.radius, pos[1])]
        self.input_elements = [] # List of elements that connect to this light
        self.deleted = False # Whether to delete the element next frame

    def draw(self):
        # Draw the light bulb
        color = (255, 255, 0) if self.state else (100, 100, 100)
        pygame.draw.circle(self.screen, color, self.pos, self.radius)

        # Draw the wire connectors
        pygame.draw.circle(self.screen, (0, 0, 255), self.wire_connectors[0], WIRE_CONNECOR_RADIUS)
        pygame.draw.circle(self.screen, (0, 0, 255), self.wire_connectors[1], WIRE_CONNECOR_RADIUS)

    def update(self):
        # Update the state of the light bulb based on the input elements
        self.state = any(input_element.state for input_element in self.input_elements)

    def set_pos(self, pos):
        # Set the position of the light bulb
        self.pos = pos
        self.wire_connectors[0] = (pos[0] - self.radius, pos[1])
        self.wire_connectors[1] = (pos[0] + self.radius, pos[1])

    # Return True if the light bulb was clicked
    def handle_click(self, mouse_pos):
        if math.hypot(self.pos[0] - mouse_pos[0], self.pos[1] - mouse_pos[1]) < self.radius:
            return True
        return False

    def handle_menu_create(self, mouse_pos):
        # Check if the input box is clicked
        if math.hypot(self.pos[0] - mouse_pos[0], self.pos[1] - mouse_pos[1]) < self.radius:
            def delete_input():
                self.deleted = True
                return True # Close the menu after deleting the input
            
            menu = Menu(self.screen, mouse_pos, ["Delete"], [delete_input])
            return menu
        
    def create_new_element(self, mouse_pos):
        new_element = Light(self.screen, mouse_pos)
        return new_element