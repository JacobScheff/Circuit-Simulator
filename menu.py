import pygame
import math

class Menu:
    def __init__(self, screen, position, options, callbacks, close_on_click=True, closing_callback=lambda: None):
        self.screen = screen
        self.position = position
        self.options = options
        self.callbacks = callbacks
        self.font = pygame.font.Font(None, 36)
        self.close_on_click = close_on_click # Whether to close the menu when something other than the menu is clicked
        self.closing_callback = closing_callback # Callback to call when the menu is closed NOTE: This is purely for storage, it must be called by whatever closes the menu

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

        self.bg_rect = pygame.Rect(self.position[0] - self.text_to_border_padding, self.position[1] - self.text_to_border_padding - self.text_line_spacing / 2, self.max_text_x + self.text_to_border_padding * 2, len(self.options) * self.text_line_spacing + self.text_to_border_padding * 2)

    def draw(self):
        # Draw background behind entire menu
        pygame.draw.rect(self.screen, self.background_color, self.bg_rect, border_radius=10)

        # Get mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # Draw the text
        for i in range(len(self.text_rects)):
            text_rect = self.text_rects[i]
            text_surface = self.text_surfaces[i]
            if text_rect.collidepoint(mouse_pos):
                # Highlight the text if the mouse is over it
                text_surface = self.font.render(self.options[i], True, (150, 150, 150))
            self.screen.blit(text_surface, text_rect)

    # Returns True if menu should close
    def handle_click(self, mouse_pos):
        for i, text_rect in enumerate(self.text_rects):
            if text_rect.collidepoint(mouse_pos):
                # Call the corresponding callback function
                if self.callbacks[i] is not None:
                    return self.callbacks[i]()
                break