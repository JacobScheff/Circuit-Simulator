import pygame
import math
from menu import Menu

class Input:
    def __init__(self, screen, pos, state, is_sample_element=False):
        self.screen = screen
        self.pos = pos
        self.state = state
        size = (50, 20)
        self.rect = pygame.Rect(pos[0] - size[0] / 2, pos[1] - size[1] / 2, size[0], size[1])
        self.deleted = False # Whether to delete the input box next frame
        self.is_sample_element = is_sample_element

    def draw(self, mos_pos=(None, None)):
        # If it is a sample element, move it to the mouse position
        if self.is_sample_element:
            self.rect.x = mos_pos[0] - self.rect.width / 2
            self.rect.y = mos_pos[1] - self.rect.height / 2
            self.rect.center = (mos_pos[0], mos_pos[1])

        # Draw the input box
        color = (255, 255, 255) if self.state == 1 else (100, 100, 100)
        pygame.draw.rect(self.screen, color, self.rect)

        # Draw the text
        font = pygame.font.Font(None, 22)
        text = font.render(str(self.state), True, (0, 0, 0) if self.state == 1 else (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)

    def handle_click(self, mouse_pos):
        # Check if the input box is clicked
        if self.rect.collidepoint(mouse_pos):
            # Toggle the state
            self.state = 1 - self.state

    def handle_menu_create(self, mouse_pos):
        # Check if the input box is clicked
        if self.rect.collidepoint(mouse_pos):
            def delete_input():
                self.deleted = True
                return True # Close the menu after deleting the input
            
            menu = Menu(self.screen, mouse_pos, ["Delete"], [delete_input])
            return menu