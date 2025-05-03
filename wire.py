import pygame
import math
from config import *

class Wire:
    def __init__(self, screen, initial_element, initial_index, initial_is_input, ending_element, ending_index, ending_is_input, state = 0):
        self.screen = screen
        self.initial_element = initial_element
        self.initial_index = initial_index
        self.initial_is_input = initial_is_input
        self.ending_element = ending_element
        self.ending_index = ending_index
        self.ending_is_input = ending_is_input
        self.state = state
        self.deleted = False

    def draw(self):
        # Draw a line from the initial element to the ending element
        pygame.draw.line(self.screen, WIRE_ON_COLOR if self.state else WIRE_OFF_COLOR, self.initial_element.wire_connectors[self.initial_index][0], self.ending_element.wire_connectors[self.ending_index][0], 5)

    # Update the wire's state
    def update(self):
        starting_end_state = self.initial_element.state
        ending_end_state = self.ending_element.state

        self.state = starting_end_state or ending_end_state