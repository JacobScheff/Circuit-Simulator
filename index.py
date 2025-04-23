import pygame
import math
from menu import Menu

SCREEN_SIZE = (1200, 600)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Circuit Simualtor")
clock = pygame.time.Clock()
FPS = 60
running = True

menus = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            menus.append(Menu(screen, event.pos, ["Start Simulation", "Load Circuit", "Exit"]))

    screen.fill((0, 0, 0))

    # Draw the menus
    for menu in menus:
        menu.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
