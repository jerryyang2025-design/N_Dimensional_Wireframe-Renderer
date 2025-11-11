"""
Module for managing wireframe drawing and display updates in the N-Dimensional Wireframe Renderer.

Provides functions to add lines to the wireframe, redraw the display, and show
an informational overlay of the current state, including dimensions, rotation,
perspective, and other settings. Handles scaling and 2D projection for rendering
higher-dimensional objects.
"""

import pygame
import utils
import data

def add_line(position_1,position_2):
    """Add a line between two points to the wireframe and draw it on the display."""
    data.wireframe.lines.append((position_1,position_2))
    scale_factor = 1
    if data.states.scale_correction:
        # Scale correction approxamated from the projection equation to undo the scaling effects
        scale_factor = (2 + 0.25 * data.states.perspective) ** (data.states.dimensions - 2)
    if data.states.perspective > 0:
        positions = utils.project_to_2d(position_1,position_2)
    else:
        # Use the x and y coordinates without projecting if in orthogonal view
        positions = (position_1[:2],position_2[:2])
        scale_factor = 1
    # Don't create line if a point is outside the bounds
    if positions is None:
        return
    x_one = data.display.half_side + positions[0][0] * scale_factor
    y_one = data.display.half_side - positions[0][1] * scale_factor
    x_two = data.display.half_side + positions[1][0] * scale_factor
    y_two = data.display.half_side - positions[1][1] * scale_factor
    pygame.draw.line(data.display.screen, data.display.line_color, (x_one, y_one), (x_two, y_two), 1)

def info():
    """Display current wireframe and state information on the screen overlay."""
    shown_info = ["Dimensions: " + str(data.states.dimensions),
                  "Perspective Depth: " + str(data.states.perspective),
                  "Rotation Plane: [" + str(min(data.rotation.plane)) + "," + str(max(data.rotation.plane)) + "]",
                  "Rotation Center: " + str(data.rotation.center),
                  "Edges: " + str(len(data.wireframe.lines)),
                  "Speed Multiplier: " + str(data.rotation.speed_multiplier) + "x",
                  "Scale Correction Toggle: " + str(data.states.scale_correction),
                  "Auto Rotation Toggle: " + str(data.rotation.auto_rotate),
                  "Keep Log: " + str(data.states.log)]
    y = data.display.spacing
    for i in range(len(shown_info)):
        text = data.display.font.render(shown_info[i],True,data.display.font_color)
        data.display.screen.blit(text,(y,y * (i + 1)))
    data.states.info = True

def redraw():
    """Clear the screen and redraw all lines and the info overlay if enabled."""
    data.display.screen.fill(data.display.screen_color)
    lines = data.wireframe.lines[:]
    data.wireframe.lines.clear()
    for line in lines:
        add_line(line[0],line[1])
    if data.states.info:
        info()
    text = data.display.font.render("Press '/' to open command panel",True,data.display.font_color)
    data.display.screen.blit(text,(data.display.spacing,data.display.side - 2 * data.display.spacing))