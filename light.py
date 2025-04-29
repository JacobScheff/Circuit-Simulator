import pygame
import math
from menu import Menu

class Light:
    def __init__(self, screen, pos):
        self.screen = screen
        self.pos = pos
        self.size = 30
        self.state = False
        self.deleted = False # Whether to delete the element next frame

    def draw(self):
        # Draw the light bulb
        color = (255, 255, 0) if self.state else (100, 100, 100)
        pygame.draw.circle(self.screen, color, self.pos, self.size)

    def set_pos(self, pos):
        # Set the position of the light bulb
        self.pos = pos

    # Return True if the light bulb was clicked
    def handle_click(self, mouse_pos):
        if math.hypot(self.pos[0] - mouse_pos[0], self.pos[1] - mouse_pos[1]) < self.size:
            return True
        return False

    def handle_menu_create(self, mouse_pos):
        # Check if the input box is clicked
        if math.hypot(self.pos[0] - mouse_pos[0], self.pos[1] - mouse_pos[1]) < self.size:
            def delete_input():
                self.deleted = True
                return True # Close the menu after deleting the input
            
            menu = Menu(self.screen, mouse_pos, ["Delete"], [delete_input])
            return menu
        
    def create_new_element(self, mouse_pos):
        new_element = Light(self.screen, mouse_pos)
        return new_element