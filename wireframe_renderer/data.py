"""
Module for storing global data classes and runtime instances 
used by the N-Dimensional Wireframe Renderer.

Contains classes for managing the display, rotation parameters, 
application state, and wireframe geometry. Also provides global 
instances of these classes for easy access throughout the program.
"""

import pygame
import math
    
class Display:
    """Initializes and manages the Pygame window, fonts, and color palettes."""
    def __init__(self,SIDE = 800):
        self.spacing = 20
        self.side = SIDE
        self.half_side = SIDE / 2
        self.palettes = [[(5, 10, 20), (0, 255, 128), (0, 200, 255)],
                         [(10, 0, 25), (255, 60, 180), (0, 255, 255)],
                         [(10, 25, 50), (180, 220, 255), (255, 255, 255)]]
        self.current_palette = 0
        self.screen_color = self.palettes[self.current_palette][0]
        self.line_color = self.palettes[self.current_palette][1]
        self.font_color = self.palettes[self.current_palette][2]
    
    def initialize_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.side, self.side))
        pygame.display.set_caption("Wireframe Renderer")
        self.font = pygame.font.SysFont("arial",20)

class Rotation:
    """Stores rotation parameters and state for N-dimensional transformations."""
    def __init__(self):
        self.speed = 30
        self.speed_multiplier = 1
        self.plane = [0,2]
        self.theta = math.pi / 72
        self.angle_rotated = 0
        self.auto_rotate = False
        self.center = [0,0]

class States:
    """Holds runtime states and rendering options."""
    def __init__(self):
        self.dimensions = 3
        self.perspective = 1
        self.scale_correction = True
        self.info = False
        self.log = False
        self.quit = False

class Wireframe:
    """Contains wireframe geometry and available user commands."""
    def __init__(self):
        self.side = 100
        self.lines = []
        self.commands = {
            "add": "Add a new line by entering two N-dimensional points.",
            "remove": "Remove a specific line using its two end points.",
            "view lines": "Display a list of all current lines on screen.",
            "clear": "Clear all lines from the display.",
            "center": "Set the rotation center (2D coordinates).",
            "plane": "Change the active rotation plane (two dimension indices).",
            "preset": "Load a preset object (e.g., hypercube, hyperpyramid).",
            "dimensions": "Set the number of dimensions for the wireframe.",
            "save": "Save the current wireframe to a file.",
            "load": "Load a wireframe from a saved file.",
            "log": "Toggle console logging on or off.",
            "keys": "Show a list of keyboard controls.",
            "help": "Display all available commands.",
            "quit": "Close the program."
        }

display = Display()
rotation = Rotation()
states = States()
wireframe = Wireframe()