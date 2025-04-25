import pygame
import math
from menu import Menu

class NewElementButton:
    def __init__(self, screen, pos, radius, padding):
        self.screen = screen
        self.pos = pos
        self.radius = radius
        self.padding = padding

    def draw(self):
        pygame.draw.circle(self.screen, (160, 160, 160), self.pos, self.radius)

        # Draw the plus sign
        pygame.draw.line(self.screen, (255, 255, 255), (self.pos[0] - self.radius + self.padding, self.pos[1]), (self.pos[0] + self.radius - self.padding, self.pos[1]), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (self.pos[0], self.pos[1] - self.radius + self.padding), (self.pos[0], self.pos[1] + self.radius - self.padding), 2)

    def collidepoint(self, mouse_pos):
        # Check if the mouse position is inside the button
        if math.sqrt((mouse_pos[0] - self.pos[0]) ** 2 + (mouse_pos[1] - self.pos[1]) ** 2) <= self.radius:
            return True
        return False

    def handle_menu_create(self, mouse_pos):
        menu = Menu(self.screen, mouse_pos, [], [None])
        return menu