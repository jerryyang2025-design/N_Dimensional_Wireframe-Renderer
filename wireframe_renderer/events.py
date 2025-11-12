"""
Module for handling user input events in the N-Dimensional Wireframe Renderer.

Processes keyboard and window events, manages rotation planes, rotation 
actions, color palette changes, screenshots, and other runtime commands.
"""

import pygame
import data
import panel
import math
import os
import utils
import render

def swap_plane(event):
    """Update the current rotation plane based on arrow key input."""
    axis_1 = data.rotation.plane[0]
    axis_2 = data.rotation.plane[1]
    # Cycles the plane values up or down 1
    if event == "up":
        if axis_1 == data.states.dimensions - 1:
            axis_1 = 0
        else:
            axis_1 += 1
        if axis_2 == data.states.dimensions - 1:
            axis_2 = 0
        else:
            axis_2 += 1
    else:
        if axis_1 == 0:
            axis_1 = data.states.dimensions - 1
        else:
            axis_1 += -1
        if axis_2 == 0:
            axis_2 = data.states.dimensions - 1
        else:
            axis_2 += -1
    data.rotation.plane[0] = axis_1
    data.rotation.plane[1] = axis_2
    data.rotation.center = [0,0]

def rotate(event):
    """Rotate all wireframe lines in the current plane."""
    # Clear the current screen and lines, while copying the line values
    data.display.screen.fill(data.display.screen_color)
    center = data.rotation.center
    lines = data.wireframe.lines[:]
    data.wireframe.lines.clear()
    # Records the angle rotated in degrees
    if event == "right":
        data.rotation.angle_rotated += data.rotation.theta * 180 / math.pi
    else:
        data.rotation.angle_rotated -= data.rotation.theta * 180 / math.pi
    for line in lines:
        new_line = [line[0][:], line[1][:]]
        for i in range(2):
            # For each line, find the distance and angle from the center, add or subtract theta, and find the new coordinates
            point= [line[i][min(data.rotation.plane)],line[i][max(data.rotation.plane)]]
            dist = utils.pythag(point[0] - center[0], point[1] - center[1])
            theta = math.atan2(point[0] - center[0], point[1] - center[1])
            if event == "right":
                point[0] = center[0] + dist * math.sin(theta + data.rotation.theta)
                point[1] = center[1] + dist * math.cos(theta + data.rotation.theta)
            else:
                point[0] = center[0] + dist * math.sin(theta - data.rotation.theta)
                point[1] = center[1] + dist * math.cos(theta - data.rotation.theta)
            new_line[i][min(data.rotation.plane)] = point[0]
            new_line[i][max(data.rotation.plane)] = point[1]
        # Add the lines with the new coordinates
        render.add_line(new_line[0],new_line[1])

def handle_slash():
    """Pause display and open command panel."""
    print("[INFO] The display is paused while the command panel is open.")
    panel.panel()

def handle_escape():
    """Quit the application."""
    data.states.quit = True
    
def handle_up():
    """Rotate the plane selection up."""
    swap_plane("up")
    if data.states.info:
        render.redraw()
    if data.states.log:
        if not data.rotation.angle_rotated == 0 and not len(data.wireframe.lines) == 0:
            print("[LOG:ROTATE] Rotated " + str(data.rotation.angle_rotated) + " degrees in the (" + str(min(data.rotation.plane)) + "," + str(max(data.rotation.plane)) + ") plane.")
            data.rotation.angle_rotated = 0
        print("[LOG:STATE] Rotation plane set to (" + str(min(data.rotation.plane)) + "," + str(max(data.rotation.plane)) + ").")
    
def handle_down():
    """Rotate the plane selection down."""
    swap_plane("down")
    if data.states.info:
        render.redraw()
    if data.states.log:
        if not data.rotation.angle_rotated == 0 and not len(data.wireframe.lines) == 0:
            print("[LOG:ROTATE] Rotated " + str(data.rotation.angle_rotated) + " degrees in the (" + str(min(data.rotation.plane)) + "," + str(max(data.rotation.plane)) + ") plane.")
            data.rotation.angle_rotated = 0
        print("[LOG:STATE] Rotation plane set to (" + str(min(data.rotation.plane)) + "," + str(max(data.rotation.plane)) + ").")

def handle_screenshot():
    """Save a screenshot of the current display."""
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
        print("[INFO] Created missing folder: 'screenshots'.")
    screenshot_name = "screenshots/Screenshot.png"
    number_of_pngs = 1
    while os.path.exists(screenshot_name):
        screenshot_name = "screenshots/Screenshot" + str(number_of_pngs) + ".png"
        number_of_pngs += 1
    pygame.image.save(data.display.screen,screenshot_name)
    print("[SUCCESS] Saved screenshot as {" + screenshot_name + "}.")

def handle_q():
    """Toggle scale correction."""
    data.states.scale_correction = not data.states.scale_correction
    render.redraw()
    if data.states.log:
        print("[LOG:VIEW] Scale correction toggle set to " + str(data.states.scale_correction) + ".")

def handle_r():
    """Toggle auto-rotation."""
    data.rotation.auto_rotate = not data.rotation.auto_rotate
    render.redraw()
    if data.states.log:
        print("[LOG:ROTATE] Auto rotate toggle set to " + str(data.rotation.auto_rotate) + ".")

def handle_plus():
    """Increase perspective depth."""
    if data.states.perspective < 5:
        data.states.perspective += 0.2
        data.states.perspective = round(data.states.perspective, 1)
        render.redraw()
        if data.states.log:
            print("[LOG:VIEW] Perspective depth set to " + str(data.states.perspective) + ".")
    else:
        print("[NOTICE] Perspective depth max limit at 5.")

def handle_minus():
    """Decrease perspective depth."""
    if data.states.perspective > 0:
        data.states.perspective += -0.2
        data.states.perspective = round(data.states.perspective, 1)
        render.redraw()
        if data.states.log:
            print("[LOG:VIEW] Perspective depth set to " + str(data.states.perspective) + ".")
    else:
        print("[NOTICE] Perspective depth min limit at 0.")

def handle_left_bracket():
    """Decrease rotation speed."""
    if data.rotation.speed_multiplier > 0.6:
        data.rotation.speed_multiplier += -0.2
        data.rotation.speed_multiplier = round(data.rotation.speed_multiplier, 1)
        render.redraw()
        if data.states.log:
            print("[LOG:VIEW] Rotation speed set to " + str(data.rotation.speed_multiplier) + "x.")
    else:
        print("[NOTICE] Rotation speed min limit at 0.6x.")

def handle_right_bracket():
    """Increase rotation speed."""
    if data.rotation.speed_multiplier < 5:
        data.rotation.speed_multiplier += 0.2
        data.rotation.speed_multiplier = round(data.rotation.speed_multiplier, 1)
        render.redraw()
        if data.states.log:
            print("[LOG:VIEW] Rotation speed set to " + str(data.rotation.speed_multiplier) + "x.")
    else:
        print("[NOTICE] Rotation speed max limit at 5x.")

def handle_p():
    """Cycle through color palettes."""
    palette = data.display.current_palette
    if palette == len(data.display.palettes) - 1:
        palette = 0
    else:
        palette += 1
    data.display.current_palette = palette
    data.display.screen_color = data.display.palettes[palette][0]
    data.display.line_color = data.display.palettes[palette][1]
    data.display.font_color = data.display.palettes[palette][2]
    render.redraw()
    if data.states.log:
        print("[LOG:VIEW] Color palette swapped to index " + str(data.display.current_palette) + ".")

def handle_tab():
    """Toggle info panel visibility."""
    if not data.states.info:
        render.info()
    else:
        data.states.info = False
        render.redraw()

def handle_rotate(direction):
    """Rotate wireframe in the given direction."""
    rotate(direction)
    if data.states.info:
        render.info()
    text = data.display.font.render("Press '/' to open command panel",True,data.display.font_color)
    data.display.screen.blit(text,(data.display.spacing,data.display.side - 2 * data.display.spacing))

def handle_events():
    """Check for and respond to Pygame events."""
    events = {
        pygame.K_SLASH: handle_slash,
        pygame.K_ESCAPE: handle_escape,
        pygame.K_UP: handle_up,
        pygame.K_DOWN: handle_down,
        pygame.K_q: handle_q,
        pygame.K_r: handle_r,
        pygame.K_EQUALS: handle_plus,
        pygame.K_MINUS: handle_minus,
        pygame.K_LEFTBRACKET: handle_left_bracket,
        pygame.K_RIGHTBRACKET: handle_right_bracket,
        pygame.K_p: handle_p,
        pygame.K_TAB: handle_tab
    }
    
    clock = pygame.time.Clock()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            data.states.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                handle_screenshot()
            elif event.key in events:
                events[event.key]()
    key = pygame.key.get_pressed()
    if len(data.wireframe.lines) != 0 and not data.rotation.auto_rotate:
        # Print the log after the user releases the arrow keys and reset angle rotated to 0
        if not key[pygame.K_RIGHT] and not key[pygame.K_LEFT]:
            if data.states.log and data.rotation.angle_rotated != 0:
                print("[LOG:ROTATE] Rotated " + str(data.rotation.angle_rotated) + " degrees in the (" + str(min(data.rotation.plane)) + "," + str(max(data.rotation.plane)) + ") plane.")
            data.rotation.angle_rotated = 0
        if key[pygame.K_RIGHT]:
            handle_rotate("right")
        elif key[pygame.K_LEFT]:
            handle_rotate("left")
    if data.rotation.auto_rotate:
        handle_rotate("right")
    pygame.display.flip()
    clock.tick(data.rotation.speed * data.rotation.speed_multiplier)