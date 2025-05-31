import pygame
import math
from config import *
from menu import Menu
from elements.element import Element

class Input(Element):
    def __init__(self, screen, pos):
        super().__init__(screen, pos)

        self.rect = pygame.Rect(pos[0] - INPUT_SIZE[0] / 2, pos[1] - INPUT_SIZE[1] / 2, INPUT_SIZE[0], INPUT_SIZE[1])
        self.wire_connectors = [((INPUT_SIZE[0] / 2, 0), False)] # (pos, is_input)

    def draw(self):
        # Draw the input box
        color = (255, 255, 255) if self.state == 1 else (100, 100, 100)
        pygame.draw.rect(self.screen, color, self.rect)

        # Draw the text
        font = pygame.font.Font(None, 22)
        text = font.render(str(self.state), True, (0, 0, 0) if self.state == 1 else (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)

        # Draw the wire connectors
        self.draw_wire_connectors()

    def update(self):
        # self.state should not update from the inputted elements since the inputs themselves are what changes the entire state of the circuit
        return

    def set_pos(self, pos):
        # Set the position of the input box
        self.pos = pos
        self.rect.x = pos[0] - self.rect.width / 2
        self.rect.y = pos[1] - self.rect.height / 2

    # Return True if the input box was clicked
    def handle_click(self, mouse_pos):
        # Check if the input box is clicked
        if self.rect.collidepoint(mouse_pos):
            # Toggle the state
            self.state = 1 - self.state
            return True
        return False

    def handle_menu_create(self, mouse_pos):
        return # Inputs should not be deletable
        
    def create_new_element(self, mouse_pos):
        new_element = Input(self.screen, mouse_pos)
        return new_element