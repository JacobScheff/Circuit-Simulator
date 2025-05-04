import pygame
import math
from config import *
from menu import Menu

class Wire:
    def __init__(self, screen, initial_element, initial_index, ending_element, ending_index, state = 0):
        self.screen = screen
        self.initial_element = initial_element
        self.initial_index = initial_index
        self.ending_element = ending_element
        self.ending_index = ending_index
        self.state = state
        self.deleted = False

    def draw(self):
        # Draw a line from the initial element to the ending element
        pygame.draw.line(self.screen, WIRE_ON_COLOR if self.state else WIRE_OFF_COLOR, self.initial_element.wire_connectors[self.initial_index][0], self.ending_element.wire_connectors[self.ending_index][0], WIRE_RADIUS)

    # Update the wire's state
    def update(self):
        starting_end_state = self.initial_element.state and not self.initial_element.wire_connectors[self.initial_index][1] # State and not is_input
        ending_end_state = self.ending_element.state and not self.ending_element.wire_connectors[self.ending_index][1] # State and not is_input

        self.state = starting_end_state or ending_end_state

    # Return True if the wire was clicked
    def handle_click(self, mouse_pos):
        # Check if the mouse is close to the wire
        x1, y1 = self.initial_element.wire_connectors[self.initial_index][0]
        x2, y2 = self.ending_element.wire_connectors[self.ending_index][0]
        distance = abs((y2 - y1) * mouse_pos[0] - (x2 - x1) * mouse_pos[1] + x2 * y1 - y2 * x1) / math.hypot(x2 - x1, y2 - y1)
        return distance < WIRE_RADIUS

    def handle_menu_create(self, mouse_pos):
        # Check if the wire is clicked
        if self.handle_click(mouse_pos):
            def delete_input():
                self.deleted = True
                return True # Close the menu after deleting the input
            
            menu = Menu(self.screen, mouse_pos, ["Delete"], [delete_input])
            return menu
        
    # Prepare for deletion
    def delete(self):
        self.deleted = True
        self.initial_element.input_wires.remove(self)
        self.ending_element.input_wires.remove(self)