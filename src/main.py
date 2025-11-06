"""
N-D Wireframe Renderer
Author: Jerry Yang

A Pygame-based visualization tool for rendering and exploring geometric wireframes
in arbitrary dimensions (2D and higher). Objects are projected from N-dimensional
space onto a 2D plane using perspective projection, allowing interactive rotation,
custom line definitions, and preset shapes such as hypercubes and hyperpyramids.

Includes features for command-based editing, file I/O, and real-time visual controls.
Designed for experimentation, visualization, and learning about higher-dimensional geometry.
"""
 #TODO: fix this description thingy idk

# === SETUP ===
import math
import pygame
import os

#TODO: take more screenshots to demo
class Display: #TODO: maybe reorganize and add more classes and maybe data classes
    """description"""
    def __init__(self,SIDE = 800): #TODO: split file into multiple files
        pygame.init() #TODO: put other classes into another class so only one parameter is needed
        self.screen = pygame.display.set_mode((SIDE, SIDE))
        pygame.display.set_caption("Wireframe Renderer")
        self.spacing = 20
        self.font = pygame.font.SysFont("arial",20)
        self.side = SIDE
        self.half_side = SIDE / 2
        self.palettes = [[(5, 10, 20), (0, 255, 128), (0, 200, 255)],
                         [(10, 0, 25), (255, 60, 180), (0, 255, 255)],
                         [(10, 25, 50), (180, 220, 255), (255, 255, 255)]]
        self.current_palette = 0
        self.screen_color = self.palettes[self.current_palette][0]
        self.line_color = self.palettes[self.current_palette][1]
        self.font_color = self.palettes[self.current_palette][2]
        self.fps = 30
        self.log = False

class Wireframe:
    """description"""
    # Well on its way to ascending to a God class
    def __init__(self):
        self.plane = [0,2]
        self.theta = math.pi / 72
        self.angle_rotated = 0
        self.side = 100
        self.dimensions = 3
        self.perspective = 1
        self.speed = 1
        self.center = [0,0]
        self.lines = []
        self.scale_correction = True
        self.info = False

def initialize(): #TODO: reorder function locations for neatness
    """description"""
    # Initialize classes
    display = Display()
    wireframe = Wireframe()
    display.screen.fill(display.screen_color) #TODO: add helpful comments to organize long code and explain logic, and docstrings
    
    # Welcome Message
    print("\n" + "=" * 60)
    print("N-Dimensional Wireframe Renderer".center(60))
    print("— Description or something —".center(60))
    print("=" * 60 + "\n") #TODO: update all print statements and make them more descriptive and helpful
    actions()
    print("Here is the list of commands:")
    command_options()
    
    text = display.font.render("Press '/' to open command panel",True,display.font_color)
    display.screen.blit(text,(display.spacing,display.side - 2 * display.spacing))
    return display, wireframe

# === UTILITY FUNCTIONS ===
def actions():
    print("Use the arrow keys, wasd, and ijkl to rotate the object.")
    print("Press '/' to open the control panel.")

def command_options(): #TODO: turn into dictionary in class and use in panel as well
    print("    add - Add a line")
    print("    preset - Apply a preset")
    print("    center - Center around a point")
    print("    plane - Set the plane of rotation")
    print("    / - Exit the panel")
    print("    clear - Clear all lines")
    print("    load - Load an object from a file")
    print("    save - Save the current object to a file")
    print("    keys - View actions")
    print("    help - View command list")

def pythag(rx,ry):
    return math.sqrt(rx ** 2 + ry ** 2)

def bound_TR(d,display,wireframe):
    if d >= wireframe.side + display.side / wireframe.perspective:
        return None
    return -wireframe.perspective * (d - wireframe.side) + display.side

def project(point,scale,display,wireframe):
    projected_point = bound_TR(float(scale),display,wireframe)
    if projected_point is None:
        return None
    elif abs(projected_point) < 0.1:
        return None
    return display.half_side * float(point) / float(projected_point)

def project_to_2d(point_1,point_2,display,wireframe):
    position_1, position_2 = point_1[:], point_2[:]
    while len(position_1) > 2:
        for i in range(len(position_1) - 1):
            position_1[i] = project(position_1[i],position_1[-1],display,wireframe)
            position_2[i] = project(position_2[i],position_2[-1],display,wireframe)
            if position_1[i] is None or position_2[i] is None:
                return None
        position_1.pop()
        position_2.pop()
    return (position_1,position_2)
    
# === RENDERING ===
def add_line(position_1,position_2,display,wireframe):
    wireframe.lines.append((position_1,position_2))
    scale_factor = 1
    if wireframe.scale_correction:
        scale_factor = (2 + 0.25 * wireframe.perspective) ** (wireframe.dimensions - 2)
    if wireframe.perspective > 0:
        positions = project_to_2d(position_1,position_2,display,wireframe)
    else:
        positions = (position_1[:2],position_2[:2])
        scale_factor = 1
    if positions is None:
        return
    x_one = display.half_side + positions[0][0] * scale_factor
    y_one = display.half_side - positions[0][1] * scale_factor
    x_two = display.half_side + positions[1][0] * scale_factor
    y_two = display.half_side - positions[1][1] * scale_factor
    pygame.draw.line(display.screen, display.line_color, (x_one, y_one), (x_two, y_two), 1)

def info(display,wireframe):
    shown_info = ["Dimensions: " + str(wireframe.dimensions),
                  "Perspective Depth: " + str(wireframe.perspective),
                  "Rotation Plane: [" + str(min(wireframe.plane)) + "," + str(max(wireframe.plane)) + "]",
                  "Rotation Center: " + str(wireframe.center),
                  "Edges: " + str(len(wireframe.lines)),
                  "Speed Multiplier: " + str(wireframe.speed) + "x",
                  "Scale Correction Toggle: " + str(wireframe.scale_correction),
                  "Keep Log: " + str(display.log)] #TODO: Make it look fancier
    y = display.spacing
    for i in range(len(shown_info)):
        text = display.font.render(shown_info[i],True,display.font_color)
        display.screen.blit(text,(y,y * (i + 1)))
    wireframe.info = True

def redraw(display,wireframe):
    display.screen.fill(display.screen_color)
    lines = wireframe.lines[:]
    wireframe.lines.clear()
    for line in lines:
        add_line(line[0],line[1],display,wireframe)
    if wireframe.info:
        info(display,wireframe)
    text = display.font.render("Press '/' to open command panel",True,display.font_color)
    display.screen.blit(text,(display.spacing,display.side - 2 * display.spacing))
        
# === ROTATION ===
def swap_plane(event,wireframe):
    axis_1 = wireframe.plane[0]
    axis_2 = wireframe.plane[1]
    if event == pygame.K_UP:
        if axis_1 == wireframe.dimensions - 1:
            axis_1 = 0
        else:
            axis_1 += 1
        if axis_2 == wireframe.dimensions - 1:
            axis_2 = 0
        else:
            axis_2 += 1
    else:
        if axis_1 == 0:
            axis_1 = wireframe.dimensions - 1
        else:
            axis_1 += -1
        if axis_2 == 0:
            axis_2 = wireframe.dimensions - 1
        else:
            axis_2 += -1
    wireframe.plane[0] = axis_1
    wireframe.plane[1] = axis_2
    wireframe.center = [0,0]

def rotate(event,display,wireframe):
    display.screen.fill(display.screen_color)
    center = wireframe.center
    lines = wireframe.lines[:]
    wireframe.lines.clear()
    if event == "right":
        wireframe.angle_rotated += wireframe.theta * 180 / math.pi
    else:
        wireframe.angle_rotated -= wireframe.theta * 180 / math.pi
    round(wireframe.angle_rotated,1)
    for line in lines:
        new_line = [line[0][:], line[1][:]]
        for i in range(2):
            point= [line[i][min(wireframe.plane)],line[i][max(wireframe.plane)]]
            dist = pythag(point[0] - center[0], point[1] - center[1])
            theta = math.atan2(point[0] - center[0], point[1] - center[1])
            if event == "right":
                point[0] = center[0] + dist * math.sin(theta + wireframe.theta)
                point[1] = center[1] + dist * math.cos(theta + wireframe.theta)
            else:
                point[0] = center[0] + dist * math.sin(theta - wireframe.theta)
                point[1] = center[1] + dist * math.cos(theta - wireframe.theta)
            new_line[i][min(wireframe.plane)] = point[0]
            new_line[i][max(wireframe.plane)] = point[1]
        add_line(new_line[0],new_line[1],display,wireframe)
        

# Check Input Coordinates
def valid_input(position,length):
    if len(position) == length:
        try:
            for value in position:
                float(value)
            return True
        except ValueError:
            return False
    else:
        return False

def valid_file(file_name,wireframe):
    try:
        file_pointer = open(file_name,"r")
        for line in file_pointer:
            test_line = line.split()
            if len(test_line) == 0 or test_line[0] == "#":
                continue
            if len(test_line) != wireframe.dimensions * 2:
                file_pointer.close()
                print("[ERROR] File is not supported for " + str(wireframe.dimensions) + " dimensions.")
                return False
            point_one = test_line[:wireframe.dimensions]
            point_two = test_line[wireframe.dimensions:]
            if not valid_input(point_one,wireframe.dimensions) or not valid_input(point_two,wireframe.dimensions):
                file_pointer.close()
                print("[ERROR] File contains unrecognized characters.")
                return False
        file_pointer.close()
        return True
    except FileNotFoundError:
        print("[ERROR] File name not recognized.")
        return False

# === PRESET SHAPES ===
def hypercube(dimensions,display,wireframe):
    points = []
    second_points = []
    number_of_points = 2 ** dimensions
    for i in range(number_of_points - 1):
        point = []
        i += 1
        for j in range(dimensions):
            j = dimensions - j - 1
            if (i - (2 ** j)) >= 0:
                point.append(wireframe.side)
                i = i - (2 ** j)
            else:
                point.append(-wireframe.side)
        points.append(point)
        second_points.append(point)
    point = [-wireframe.side] * dimensions
    points.append(point)
    second_points.append(point)
    for i in points:
        second_points.remove(i)
        for j in second_points:
            different = 0
            for k in range(dimensions):
                if i[k] != j[k]:
                    different += 1
            if different == 1:
                add_line(i,j,display,wireframe)
                
def hyperpyramid(dimensions,display,wireframe):
    if wireframe.dimensions == 2:
        print("[NOTICE] Action terminated.")
        print("     Reason: Hyperpyramid requires dimensions >= 3.")
        return
    points = []
    second_points = []
    dimensions += -1
    number_of_points = 2 ** dimensions
    for i in range(number_of_points - 1):
        point = []
        i += 1
        for j in range(dimensions):
            if j == 1:
                point.append(-wireframe.side)
            j = dimensions - j - 1
            if (i - (2 ** j)) >= 0:
                point.append(wireframe.side)
                i = i - (2 ** j)
            else:
                point.append(-wireframe.side)
        points.append(point)
        second_points.append(point)
    point = [-wireframe.side] * (dimensions + 1)
    points.append(point)
    second_points.append(point)
    for i in points:
        second_points.remove(i)
        for j in second_points:
            different = 0
            for k in range(dimensions + 1):
                if i[k] != j[k]:
                    different += 1
            if different == 1:
                add_line(i,j,display,wireframe)
    point = [0,wireframe.side] + [0] * (dimensions - 1)
    for i in points:
        add_line(i,point,display,wireframe)

# === INTERACTIVE CONTROLS ===
def panel(display,wireframe):
    commands = ["add","remove","view lines","preset","center","clear","help","keys","plane","save","load","log","dimensions"] #TODO: move these to classes
    #TODO: clean up all the checks in the if statements/split into multiple if statements with more descriptive error messages once in separate functions
    presets = ["hypercube","hyperpyramid"]
    command = ""
    while True:
        command = input("Enter a command: ")
        if command == "/":
            break
        if command not in commands:
            print("Invalid command!")
            print("Enter 'help' to view available commands.")
            continue
        if command == "add":
            while True:
                user_input = input("Enter the coordinates of point 1: ")
                if user_input == "/":
                    break
                point_one = user_input.split()
                if not valid_input(point_one,wireframe.dimensions):
                    print("Invalid coordinates!")
                    continue
                while True:
                    user_input = input("Enter the coordinates of point 2: ")
                    if user_input == "/":
                        break
                    point_two = user_input.split()
                    if (not valid_input(point_two,wireframe.dimensions)) or point_two == point_one:
                        print("Invalid coordinates!")
                        continue
                    for i in range(wireframe.dimensions):
                        point_one[i] = float(point_one[i])
                        point_two[i] = float(point_two[i])
                    add_line(point_one,point_two,display,wireframe)
                    redraw(display,wireframe)
                    if display.log:
                        print("[LOG:VIEW] Added one line.")
                    break
                break
        if command == "remove":
            while True:
                user_input = input("Enter the coordinates of point 1: ")
                if user_input == "/":
                    break
                point_one = user_input.split()
                if not valid_input(point_one,wireframe.dimensions):
                    print("Invalid coordinates!")
                    continue
                while True:
                    user_input = input("Enter the coordinates of point 2: ")
                    if user_input == "/":
                        break
                    point_two = user_input.split()
                    if (not valid_input(point_two,wireframe.dimensions)) or point_two == point_one:
                        print("Invalid coordinates!")
                        continue
                    for i in range(wireframe.dimensions):
                        point_one[i] = float(point_one[i])
                        point_two[i] = float(point_two[i])
                    remove_line = (point_one,point_two)
                    removed = False
                    lines = wireframe.lines[:]
                    for line in lines:
                        if remove_line == line:
                            wireframe.lines.remove(remove_line)
                            removed = True
                    if not removed:
                        print("Line not found!")
                        break
                    redraw(display,wireframe)
                    if display.log:
                        print("[LOG:VIEW] Removed one line.")
                    break
                if removed:
                    break
        elif command == "dimensions":
            while True:
                user_input = input("Enter the dimension: ")
                if user_input == "/":
                    break
                if not valid_input(user_input.split(),1) or int(user_input) < 2:
                    print("Invalid dimension!")
                    continue
                wireframe.dimensions = int(user_input)
                if display.log:
                    print("[LOG:STATE] Dimension set to " + str(wireframe.dimensions) + "D.")
                if wireframe.dimensions >= 10:
                    print("[NOTICE] High-dimensional objects may render slowly on some machines.")
                wireframe.center = [0,0]
                if wireframe.dimensions == 2:
                    wireframe.plane = [0,1]
                else:
                    wireframe.plane = [0,2]
                wireframe.lines.clear()
                redraw(display,wireframe)
                break
        elif command == "clear":
            wireframe.lines.clear()
            redraw(display,wireframe)
            if display.log:
                print("[LOG:VIEW] Screen cleared.")
        elif command == "log":
            display.log = not display.log
            redraw(display,wireframe)
        elif command == "view lines":
            if len(wireframe.lines) == 0:
                print("[INFO] No lines currently present on the screen.")
            else:
                proceed = True
                lines_before_warning = 50
                if len(wireframe.lines) >= lines_before_warning:
                    print("[NOTICE] Large number of lines present.")
                    while True:
                        user_input = input("    You are about to print " + str(len(wireframe.lines)) + " lines. Are you sure you want to proceed? (y/n) ")
                        if user_input == "/" or user_input.lower() == "n":
                            proceed = False
                            break
                        elif user_input.lower() == "y":
                            break
                        else:
                            print("Invalid response!")
                if proceed:
                    i = 1
                    for line in wireframe.lines:
                        print("Line " + str(i) + ": (" + " ".join(map(str, line[0])) + ") - (" + " ".join(map(str, line[1])) + ")")
                        i += 1
        elif command == "center":
            while True:
                user_input = input("Enter the center of the rotation plane: ")
                if user_input == "/":
                    break
                center_point = user_input.split()
                if not valid_input(center_point,2):
                    print("Invalid coordinates!")
                    continue
                wireframe.center = [float(center_point[0]),float(center_point[1])]
                redraw(display,wireframe)
                if display.log:
                    print("[LOG:STATE] Rotation center set to (" + str(wireframe.center[0]) + "," + str(wireframe.center[1]) + ").")
                break
        elif command == "plane":
            while True:
                user_input = input("Enter the plane of rotation: ")
                if user_input == "/":
                    break
                plane = user_input.split()
                if (not valid_input(plane,2)) or plane[0] == plane[-1] or int(plane[0]) >= wireframe.dimensions or int(plane[1]) >= wireframe.dimensions or int(plane[0]) < 0 or int(plane[1]) < 0:
                    print("Invalid plane!")
                    continue
                plane[0] = int(plane[0])
                plane[1] = int(plane[1])
                wireframe.plane = plane
                redraw(display,wireframe)
                if display.log:
                    print("[LOG:STATE] Rotation plane set to (" + str(min(wireframe.plane)) + "," + str(max(wireframe.plane)) + ").")
                break
        elif command == "load":
            while True:
                user_input = input("Enter the file name: ")
                if user_input == "/":
                    break
                file_name = "file_shapes/" + user_input + ".txt"
                if valid_file(file_name,wireframe):
                    file_pointer = open(file_name,"r")
                    lines = 0
                    for line in file_pointer:
                        test_line = line.split()
                        if len(test_line) == 0 or test_line[0] == "#":
                            continue
                        point_one = test_line[:wireframe.dimensions]
                        point_two = test_line[wireframe.dimensions:]
                        for i in range(wireframe.dimensions):
                            point_one[i] = float(point_one[i])
                            point_two[i] = float(point_two[i])
                        add_line(point_one,point_two,display,wireframe)
                        lines += 1
                    file_pointer.close()
                    print("[SUCCESS] " + str(lines) + " lines loaded from file {" + file_name + "}.")
                    break
        elif command == "save":
            while True:
                invalid_characters = " \\/.<>?*:|\""
                user_input = input("Enter the file name: ")
                if user_input == "/":
                    break
                if user_input == "" or any (ch in invalid_characters for ch in user_input):
                    print("Invalid file name!")
                    continue
                file_name = "file_shapes/" + user_input + ".txt"
                file_pointer = open(file_name,"w")
                file_pointer.write("# === Saved Wireframe ===\n")
                file_pointer.write("#   Required Dimensions: " + str(wireframe.dimensions) + "\n")
                file_pointer.write("#   Lines: " + str(len(wireframe.lines)) + "\n")
                file_pointer.write("\n\n\n")
                for line in wireframe.lines:
                    for point in line:
                        for coordinate in point:
                            file_pointer.write(str(coordinate) + " ")
                    file_pointer.write("\n")
                file_pointer.close()
                print("[SUCCESS] " + str(len(wireframe.lines)) + " lines saved to file {" + file_name + "}.")
                break
        elif command == "help":
            command_options()
        elif command == "keys":
            actions()
        elif command == "preset":
            while True:
                user_input = input("Enter a preset: ")
                if user_input == "/":
                    break
                if user_input not in presets:
                    print("Not a preset!")
                    print("Available presets:")
                    for preset in presets:
                        print("     " + preset)
                    continue
                if user_input == "hypercube":
                    hypercube(wireframe.dimensions,display,wireframe)
                    if display.log:
                        print("[LOG:LOAD] Object hypercube loaded in " + str(wireframe.dimensions) + " dimensions.")
                if user_input == "hyperpyramid":
                    hyperpyramid(wireframe.dimensions,display,wireframe)
                    if display.log:
                        print("[LOG:LOAD] Object hyperpyramid loaded in " + str(wireframe.dimensions) + " dimensions.")
                redraw(display,wireframe)
                break

def main(): #TODO: move event checks to another function and add more helper functions for each event, and for panel().
    #Maybe dictionary with command and corresponding function: handler = dictionary.get(user_input) then handler(arguments)
    display, wireframe = initialize()
    panel(display,wireframe)
    clock = pygame.time.Clock()
    
    # Check for inputs
    running = True
    while running:#TODO: make another function to handle all events (similar to panel) and smaller functions within for each event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SLASH:
                    panel(display,wireframe)
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    swap_plane(event.key,wireframe)
                    if wireframe.info:
                        redraw(display,wireframe)
                    if display.log:
                        print("[LOG:STATE] Rotation plane set to (" + str(min(wireframe.plane)) + "," + str(max(wireframe.plane)) + ").")
                elif event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    number_of_pngs = len([f for f in os.listdir("screenshots") if f.endswith(".png")])
                    screenshot_name = "screenshots/Screenshot" + str(number_of_pngs + 1) + ".png"
                    pygame.image.save(display.screen,screenshot_name)
                    print("[SUCCESS] Saved screenshot as {" + screenshot_name + "}.")
                elif event.key == pygame.K_q:
                    wireframe.scale_correction = not wireframe.scale_correction
                    redraw(display,wireframe)
                    if display.log:
                        print("[LOG:VIEW] Scale correction toggle set to " + str(wireframe.scale_correction) + ".")
                elif event.key == pygame.K_EQUALS:
                    if wireframe.perspective < 5:
                        wireframe.perspective += 0.2
                        wireframe.perspective = round(wireframe.perspective, 1)
                        redraw(display,wireframe)
                        if display.log:
                            print("[LOG:VIEW] Perspective depth set to " + str(wireframe.perspective) + ".")
                    else:
                        print("[NOTICE] Perspective depth max limit at 5.")
                elif event.key == pygame.K_MINUS:
                    if wireframe.perspective > 0:
                        wireframe.perspective += -0.2
                        wireframe.perspective = round(wireframe.perspective, 1)
                        redraw(display,wireframe)
                        if display.log:
                            print("[LOG:VIEW] Perspective depth set to " + str(wireframe.perspective) + ".")
                    else:
                        print("[NOTICE] Perspective depth min limit at 0.")
                elif event.key == pygame.K_LEFTBRACKET:
                    if wireframe.speed > 0.6:
                        wireframe.speed += -0.2
                        wireframe.speed = round(wireframe.speed, 1)
                        redraw(display,wireframe)
                        if display.log:
                            print("[LOG:VIEW] Rotation speed set to " + str(wireframe.speed) + "x.")
                    else:
                        print("[NOTICE] Rotation speed min limit at 0.6x.")
                elif event.key == pygame.K_RIGHTBRACKET:
                    if wireframe.speed < 5:
                        wireframe.speed += 0.2
                        wireframe.speed = round(wireframe.speed, 1)
                        redraw(display,wireframe)
                        if display.log:
                            print("[LOG:VIEW] Rotation speed set to " + str(wireframe.speed) + "x.")
                    else:
                        print("[NOTICE] Rotation speed max limit at 5x.")
                elif event.key == pygame.K_p:
                    palette = display.current_palette
                    if palette == len(display.palettes) - 1:
                        palette = 0
                    else:
                        palette += 1
                    display.current_palette = palette
                    display.screen_color = display.palettes[palette][0]
                    display.line_color = display.palettes[palette][1]
                    display.font_color = display.palettes[palette][2]
                    redraw(display,wireframe)
                    if display.log:
                        print("[LOG:VIEW] Color palette swapped to index " + str(display.current_palette) + ".")
                elif event.key == pygame.K_TAB:
                    if not wireframe.info:
                        info(display,wireframe)
                    else:
                        wireframe.info = False
                        redraw(display,wireframe)
        key = pygame.key.get_pressed()
        if len(wireframe.lines) != 0:
            if not key[pygame.K_RIGHT] and not key[pygame.K_LEFT]:
                if display.log and wireframe.angle_rotated != 0:
                    print("[LOG:ROTATE] Rotated " + str(wireframe.angle_rotated) + " degrees in the (" + str(min(wireframe.plane)) + "," + str(max(wireframe.plane)) + ") plane.")
                wireframe.angle_rotated = 0
            if key[pygame.K_RIGHT]:
                rotate("right",display,wireframe)
                if wireframe.info:
                    info(display,wireframe)
                text = display.font.render("Press '/' to open command panel",True,display.font_color)
                display.screen.blit(text,(display.spacing,display.side - 2 * display.spacing))
            elif key[pygame.K_LEFT]:
                rotate("left",display,wireframe)
                if wireframe.info:
                    info(display,wireframe)
                text = display.font.render("Press '/' to open command panel",True,display.font_color)
                display.screen.blit(text,(display.spacing,display.side - 2 * display.spacing))
        pygame.display.flip()
        clock.tick(display.fps * wireframe.speed)
    pygame.quit()

# === START PROGRAM ===
if __name__ == "__main__":
    main()