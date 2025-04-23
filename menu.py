import pygame
import math

class Menu:
    def __init__(self, screen, position, size):
        self.screen = screen
        self.position = position
        self.options = ["Start Simulation", "Load Circuit", "Exit"]
        self.selected_option = 0

    def draw(self):
        self.screen.fill((0, 0, 0))
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 200 + i * 50))
            self.screen.blit(text_surface, text_rect)

    # Highlight options when hovered
    def update_display(self):
        a=1