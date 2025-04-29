import pygame
import math
from config import *
from menu import Menu

class Input:
    def __init__(self, screen, pos, state):
        self.screen = screen
        self.pos = pos
        self.state = state
        size = (50, 20)
        self.rect = pygame.Rect(pos[0] - size[0] / 2, pos[1] - size[1] / 2, size[0], size[1])
        self.wire_connectors = [(pos[0] + size[0] / 2, pos[1])]
        self.deleted = False # Whether to delete the element next frame

    def draw(self):
        # Draw the input box
        color = (255, 255, 255) if self.state == 1 else (100, 100, 100)
        pygame.draw.rect(self.screen, color, self.rect)

        # Draw the text
        font = pygame.font.Font(None, 22)
        text = font.render(str(self.state), True, (0, 0, 0) if self.state == 1 else (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)

        # Draw the wire connector
        pygame.draw.circle(self.screen, (0, 0, 255), self.wire_connectors[0], WIRE_CONNECOR_RADIUS)

    def set_pos(self, pos):
        # Set the position of the input box
        self.rect.x = pos[0] - self.rect.width / 2
        self.rect.y = pos[1] - self.rect.height / 2
        self.wire_connectors[0] = (pos[0] + self.rect.width / 2, pos[1])

    # Return True if the input box was clicked
    def handle_click(self, mouse_pos):
        # Check if the input box is clicked
        if self.rect.collidepoint(mouse_pos):
            # Toggle the state
            self.state = 1 - self.state
            return True
        return False

    def handle_menu_create(self, mouse_pos):
        # Check if the input box is clicked
        if self.rect.collidepoint(mouse_pos):
            def delete_input():
                self.deleted = True
                return True # Close the menu after deleting the input
            
            menu = Menu(self.screen, mouse_pos, ["Delete"], [delete_input])
            return menu
        
    def create_new_element(self, mouse_pos):
        new_element = Input(self.screen, mouse_pos, 0)
        return new_element