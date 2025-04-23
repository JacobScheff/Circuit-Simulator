import pygame
import math

class Menu:
    def __init__(self, screen, position, options):
        self.screen = screen
        self.position = position
        self.options = options
        self.selected_option = 0
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        background_color = (120, 120, 120)
        text_color = (255, 255, 255)
        text_to_border_padding = 5
        text_line_spacing = 40
        max_text_x = -99999

        for i, option in enumerate(self.options):
            text_surface = self.font.render(option, True, text_color)
            text_rect = text_surface.get_rect(center=(self.position[0] + text_to_border_padding, self.position[1] + i * text_line_spacing))
            size_x = text_surface.get_size()[0]
            max_text_x = max(max_text_x, size_x)
            text_rect = text_surface.get_rect(center=(self.position[0] + size_x / 2, self.position[1] + i * text_line_spacing))

            # Draw text
            self.screen.blit(text_surface, text_rect)

        # Draw background behind entire menu
        # menu_rect = pygame.Rect(self.position[0] - text_to_border_padding, self.position[1] - text_to_border_padding, max_text_x + text_to_border_padding, len(self.options) * text_line_spacing + text_to_border_padding)
        # pygame.draw.rect(self.screen, background_color, menu_rect)