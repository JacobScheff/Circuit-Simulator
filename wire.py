import pygame
import math

class Wire:
    def __init__(self, screen, initial_element, ending_element, state):
        self.screen = screen
        self.initial_element = initial_element
        self.ending_element = ending_element
        self.state = state
        self.deleted = False

    def draw(self):
        # Draw a line from the initial element to the ending element
        pygame.draw.line(self.screen, (255, 255, 255), self.initial_element.pos, self.ending_element.pos, 2)