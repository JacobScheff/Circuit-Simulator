import pygame
import math

class Menu:
    def __init__(self, screen, position, options):
        self.screen = screen
        self.position = position
        self.options = options
        self.selected_option = 0
        self.font = pygame.font.Font(None, 36)

        self.background_color = (120, 120, 120)
        self.text_color = (255, 255, 255)
        self.text_to_border_padding = 5
        self.text_line_spacing = 40
        self.max_text_x = -99999
        self.text_surfaces = []
        self.text_rects = []

        # Precalculate text surfaces
        for i, option in enumerate(self.options):
            text_surface = self.font.render(option, True, self.text_color)
            surface_size = text_surface.get_size()
            self.max_text_x = max(self.max_text_x, surface_size[0])
            self.text_surfaces.append(text_surface)

        # Precalculate text rects
        for i, option in enumerate(self.options):
            text_rect = self.text_surfaces[i].get_rect(center=(self.position[0] + self.max_text_x / 2, self.position[1] + i * self.text_line_spacing))
            self.text_rects.append(text_rect)

    def draw(self):
        # Draw the text
        for i in range(len(self.text_rects)):
            text_rect = self.text_rects[i]
            text_surface = self.text_surfaces[i]
            self.screen.blit(text_surface, text_rect)

        # Draw background behind entire menu
        # menu_rect = pygame.Rect(self.position[0] - text_to_border_padding, self.position[1] - text_to_border_padding, max_text_x + text_to_border_padding, len(self.options) * text_line_spacing + text_to_border_padding)
        # pygame.draw.rect(self.screen, background_color, menu_rect)