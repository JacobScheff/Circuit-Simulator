import pygame
import math
from config import *
from simulation import *
from menu import *
from new_element import *
from wire import *
from elements import *

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Circuit Simulator")
clock = pygame.time.Clock()
running = True
paused = False

# List of all element types and their names for the menu
element_types = [Light, OrGate, AndGate, XorGate, NotGate, NorGate, NandGate, XnorGate]
element_names = ["Light", "Or", "And", "Xor", "Not", "Nor", "Nand", "Xnor"]

# Create gate off images
OR_GATE_OFF_IMAGE.fill((80, 80, 80, 255), None, pygame.BLEND_RGBA_MULT)
NOR_GATE_OFF_IMAGE.fill((80, 80, 80, 255), None, pygame.BLEND_RGBA_MULT)
AND_GATE_OFF_IMAGE.fill((80, 80, 80, 255), None, pygame.BLEND_RGBA_MULT)
NAND_GATE_OFF_IMAGE.fill((80, 80, 80, 255), None, pygame.BLEND_RGBA_MULT)
XOR_GATE_OFF_IMAGE.fill((80, 80, 80, 255), None, pygame.BLEND_RGBA_MULT)
XNOR_GATE_OFF_IMAGE.fill((80, 80, 80, 255), None, pygame.BLEND_RGBA_MULT)
NOT_GATE_OFF_IMAGE.fill((80, 80, 80, 255), None, pygame.BLEND_RGBA_MULT)

main_simulation = Simulation(screen, element_types, element_names, 4) # The main, displayed simulation
running_simulations = [] # The small undisplayed simulations that are running in the background

while running:
    main_simulation.tick()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()