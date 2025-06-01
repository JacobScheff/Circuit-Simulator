import pygame
import math
import pickle
from config import *

# Renders and operates the load menu, which allows the user to select a simulation to load. Returns the simulation to load
def load_menu(clock, screen):
    position = (screen.get_width() // 2, screen.get_height() // 2)
    background_color = (120, 120, 120)
    size = (600, 400)