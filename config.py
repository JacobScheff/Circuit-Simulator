import pygame

SCREEN_SIZE = (1200, 600)
GRID_SIZE = 25 # Grid size when grid is enabled
FPS = 60

WIRE_WIDTH = 5 # Width of the wire
WIRE_CONNECOR_RADIUS = 5 # Radius of the wire connector
WIRE_ON_COLOR = (255, 255, 255) # Color of the wire when on
WIRE_OFF_COLOR = (100, 100, 100) # Color of the wire when off
WIRE_CURRENT = 2 # How fast the current flows through the wire

LIGHT_RADIUS = 30 # Radius of the light bulb

INPUT_SIZE = (50, 20) # Size of the input box

### --- Symbols --- ###
OR_GATE_IMAGE = pygame.image.load("symbols/or_gate.tiff")
OR_GATE_OFF_IMAGE = pygame.image.load("symbols/or_gate.tiff").copy()

NOR_GATE_IMAGE = pygame.image.load("symbols/nor_gate.tiff")
NOR_GATE_OFF_IMAGE = pygame.image.load("symbols/nor_gate.tiff").copy()

AND_GATE_IMAGE = pygame.image.load("symbols/and_gate.tiff")
AND_GATE_OFF_IMAGE = pygame.image.load("symbols/and_gate.tiff").copy()

NAND_GATE_IMAGE = pygame.image.load("symbols/nand_gate.tiff")
NAND_GATE_OFF_IMAGE = pygame.image.load("symbols/nand_gate.tiff").copy()

XOR_GATE_IMAGE = pygame.image.load("symbols/xor_gate.tiff")
XOR_GATE_OFF_IMAGE = pygame.image.load("symbols/xor_gate.tiff").copy()

XNOR_GATE_IMAGE = pygame.image.load("symbols/xor_gate.tiff")
XNOR_GATE_OFF_IMAGE = pygame.image.load("symbols/xnor_gate.tiff").copy()

NOT_GATE_IMAGE = pygame.image.load("symbols/not_gate.tiff")
NOT_GATE_OFF_IMAGE = pygame.image.load("symbols/not_gate.tiff").copy()

def lerp(start, end, t):
    return start + (end - start) * t