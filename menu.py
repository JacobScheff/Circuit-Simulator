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
        for i, option in enumerate(self.options):
            background_color = (120, 120, 120)
            text_color = (255, 255, 255)
            text_to_border_padding = 5
            text_line_spacing = 5
            text_surface = self.font.render(option, True, text_color)
            max_text_x = -99999
            for option in self.options:
                text_rect = text_surface.get_rect(center=(self.position[0] + text_to_border_padding, self.position[1] + i * text_line_spacing))
                max_text_x = max(max_text_x, text_rect.width)
            text_rect = text_surface.get_rect(center=(self.position[0] + max_text_x / 2, self.position[1] + i * text_line_spacing))
            # Draw background rectangle
            pygame.draw.rect(self.screen, background_color, text_rect.inflate(text_to_border_padding * 2, text_to_border_padding * 2))
            # Draw text
            self.screen.blit(text_surface, text_rect)