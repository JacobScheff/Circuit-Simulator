import pygame
import math

class Input:
    def __init__(self, screen, pos, state):
        self.screen = screen
        self.pos = pos
        self.state = state
        size = (50, 20)
        self.rect = pygame.Rect(pos[0] - size[0] / 2, pos[1] - size[1] / 2, size[0], size[1])

    def draw(self):
        # Draw the input box
        color = (255, 255, 255) if self.state == 1 else (100, 100, 100)
        pygame.draw.rect(self.screen, color, self.rect)

    def handle_click(self, mouse_pos):
        # Check if the input box is clicked
        if self.rect.collidepoint(mouse_pos):
            # Toggle the state
            self.state = 1 - self.state
