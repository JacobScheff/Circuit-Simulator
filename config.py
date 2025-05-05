import pygame

SCREEN_SIZE = (1200, 600)
GRID_SIZE = 25 # Grid size when grid is enabled
FPS = 60

WIRE_RADIUS = 5 # Radius of the wire
WIRE_CONNECOR_RADIUS = 5 # Radius of the wire connector
WIRE_ON_COLOR = (255, 255, 255) # Color of the wire when on
WIRE_OFF_COLOR = (100, 100, 100) # Color of the wire when off

### --- Symbols --- ###
OR_GATE_IMAGE = pygame.image.load("symbols/or_gate.tiff")
OR_GATE_OFF_IMAGE = pygame.image.load("symbols/or_gate.tiff").copy()