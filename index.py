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

def start():
    print("User pressed start")
def load():
    print("User pressed load")
def exit():
    print("User pressed exit")
    return True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                mouse_pos = pygame.mouse.get_pos()
                menus.append(Menu(screen, mouse_pos, ["Start Simulation", "Load Circuit", "Exit"], [start, load, exit]))
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mos_pos = pygame.mouse.get_pos()

            # Handle menu clicks
            for menu in menus:
                if event.button == 1:
                    # If handle_click returns True, close the menu
                    if menu.handle_click(mos_pos):
                        menus.remove(menu)
                        break

    screen.fill((0, 0, 0))

    # Draw the menus
    for menu in menus:
        menu.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
