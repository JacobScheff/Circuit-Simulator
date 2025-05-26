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
        # Unlike gates/inputs, a wire can contain many different states. It can have sections of on and off.
        self.state = [] # (t_initial, t_enging), Stores time intervals where the wire is on
        self.deleted = False

    def draw(self):
        # Draw a line between the two wire connectors
        initial_element_pos = self.initial_element.pos
        intial_connector_pos = self.initial_element.wire_connectors[self.initial_index][0]
        ending_element_pos = self.ending_element.pos
        ending_connector_pos = self.ending_element.wire_connectors[self.ending_index][0]

        line_start = (initial_element_pos[0] + intial_connector_pos[0], initial_element_pos[1] + intial_connector_pos[1])
        line_end = (ending_element_pos[0] + ending_connector_pos[0], ending_element_pos[1] + ending_connector_pos[1])

        # Draw the entire wire as off
        pygame.draw.line(self.screen, WIRE_OFF_COLOR if self.state else WIRE_OFF_COLOR, line_start, line_end, WIRE_WIDTH)

        # Draw the on sections of the wire
        if self.state:
            for t_initial, t_ending in self.state:
                # Calculate the position of the wire at the given time
                x1 = lerp(line_start[0], line_end[0], t_initial)
                y1 = lerp(line_start[1], line_end[1], t_initial)
                x2 = lerp(line_start[0], line_end[0], t_ending)
                y2 = lerp(line_start[1], line_end[1], t_ending)

                # Draw the on section of the wire
                pygame.draw.line(self.screen, WIRE_ON_COLOR, (x1, y1), (x2, y2), WIRE_WIDTH)
        
    # Update the wire's state
    def update(self):
        starting_end_state = self.initial_element.state and not self.initial_element.wire_connectors[self.initial_index][1] # State and not is_input
        ending_end_state = self.ending_element.state and not self.ending_element.wire_connectors[self.ending_index][1] # State and not is_input

        self.state = starting_end_state or ending_end_state

    # Return True if the wire was clicked
    def handle_click(self, mouse_pos):
        # Check if the mouse is close to the wire
        initial_element_pos = self.initial_element.pos
        intial_connector_pos = self.initial_element.wire_connectors[self.initial_index][0]
        ending_element_pos = self.ending_element.pos
        ending_connector_pos = self.ending_element.wire_connectors[self.ending_index][0]
        x1, y1 = initial_element_pos[0] + intial_connector_pos[0], initial_element_pos[1] + intial_connector_pos[1]
        x2, y2 = ending_element_pos[0] + ending_connector_pos[0], ending_element_pos[1] + ending_connector_pos[1]
        
        # Check if mouse_pos is outside bounds of the wire
        if (mouse_pos[0] < min(x1, x2) or mouse_pos[0] > max(x1, x2) or
            mouse_pos[1] < min(y1, y2) or mouse_pos[1] > max(y1, y2)):
            return False

        # Calculate the distance from the mouse to the line segment
        distance = abs((y2 - y1) * mouse_pos[0] - (x2 - x1) * mouse_pos[1] + x2 * y1 - y2 * x1) / math.hypot(x2 - x1, y2 - y1)
        return distance < WIRE_WIDTH

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
        # Try except since element may already be deleted
        try:
            self.initial_element.input_wires.remove(self)
        except ValueError:
            pass
        try:
            self.ending_element.input_wires.remove(self)
        except ValueError:
            pass