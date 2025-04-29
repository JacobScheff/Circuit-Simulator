import pygame
import math
from config import *

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
        pygame.draw.line(self.screen, (255, 255, 255), self.initial_element.wire_connectors[self.initial_element], self.ending_element.wire_connectors[self.ending_index], 5)