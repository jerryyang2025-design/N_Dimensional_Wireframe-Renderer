"""
Module for handling the command panel interface in the N-Dimensional Wireframe Renderer.

Provides functions to process user input for modifying the wireframe, such as adding
or removing lines, changing dimensions, adjusting rotation settings, toggling logging,
loading and saving files, and applying preset shapes. The main panel loop allows
interactive command execution while pausing the display.
"""

import utils
import render
import data
import presets
import os

def actions():
    """Display a list of all keyboard controls and their functions."""
    print("\n" + "─" * 70)
    print("Keyboard Controls".center(70))
    print("─" * 70)

    print("\n[ Navigation & Rotation ]")
    print("  → / ←     Rotate object in current plane")
    print("  ↑ / ↓     Cycle through rotation planes")
    print("  R         Toggle auto-rotation")
    print("  Q         Toggle scale-correction")

    print("\n[ Perspective & Speed ]")
    print("  + / -     Increase or decrease perspective depth (0 - 5)")
    print("  [ / ]     Adjust rotation speed (0.6x - 5x)")

    print("\n[ Display & Info ]")
    print("  TAB       Toggle object info overlay")
    print("  P         Cycle through color palettes")
    print("  CTRL+S    Save a screenshot to the 'screenshots' folder")

    print("\n[ Commands & Program ]")
    print("  /         Open command panel (pauses display)")
    print("  ESC       Quit the program")

def command_options():
    """Display all available command panel commands and their descriptions."""
    print("\n" + "─" * 70)
    print("Command Panel Commands".center(70))
    print("─" * 70)

    for command, description in data.wireframe.commands.items():
        print("  " + command.ljust(15) + description)

    print("─" * 70)
    print("Tip: Type '/' to cancel a prompt or return to the main display.")
    print("─" * 70 + "\n")
    
def handle_add():
    """Prompt the user to add a line by specifying two points."""
    while True:
        user_input = input("Enter the coordinates of point 1: ")
        if user_input == "/":
            break
        point_one = user_input.split()
        if not utils.valid_input(point_one,data.states.dimensions):
            print("Invalid coordinates!")
            continue
        while True:
            user_input = input("Enter the coordinates of point 2: ")
            if user_input == "/":
                break
            point_two = user_input.split()
            if (not utils.valid_input(point_two,data.states.dimensions)):
                print("Invalid coordinates!")
                continue
            for i in range(data.states.dimensions):
                point_one[i] = float(point_one[i])
                point_two[i] = float(point_two[i])
            if point_two == point_one:
                print("Invalid coordinates!")
                continue
            render.add_line(point_one,point_two)
            render.redraw()
            if data.states.log:
                print("[LOG:VIEW] Added one line.")
            break
        break

def handle_remove():
    """Prompt the user to remove a line by specifying two points."""
    while True:
        removed = False
        user_input = input("Enter the coordinates of point 1: ")
        if user_input == "/":
            break
        point_one = user_input.split()
        if not utils.valid_input(point_one,data.states.dimensions):
            print("Invalid coordinates!")
            continue
        while True:
            user_input = input("Enter the coordinates of point 2: ")
            if user_input == "/":
                break
            point_two = user_input.split()
            if (not utils.valid_input(point_two,data.states.dimensions)):
                print("Invalid coordinates!")
                continue
            for i in range(data.states.dimensions):
                point_one[i] = float(point_one[i])
                point_two[i] = float(point_two[i])
            if point_two == point_one:
                print("Invalid coordinates!")
                continue
            remove_line = (point_one,point_two)
            removed = False
            lines = data.wireframe.lines[:]
            for line in lines:
                if utils.lines_equal(remove_line,line):
                    data.wireframe.lines.remove(line)
                    removed = True
            if not removed:
                print("Line not found!")
                print("     Enter 'view lines' to view current lines.")
                break
            render.redraw()
            if data.states.log:
                print("[LOG:VIEW] Removed one line.")
            break
        if removed or user_input == "/":
            break

def handle_dimensions():
    """Prompt the user to set the dimensionality of the wireframe and reset related settings."""
    while True:
        user_input = input("Enter the dimension: ")
        if user_input == "/":
            break
        if not utils.valid_input(user_input.split(),1) or int(user_input) < 2:
            print("Invalid dimension!")
            continue
        user_input = int(user_input)
        if user_input >= 10:
            print("[NOTICE] High-dimensional objects may render slowly on some machines.")
            confirm = input("    Are you sure you want to proceed? (y/n) ").lower()
            if confirm == "/":
                break
            elif confirm == "n":
                continue
            elif confirm == "y":
                pass
            else:
                print("ಠ_ಠ  ...Your response has been set to 'no'.")
                continue
        data.states.dimensions = user_input
        if data.states.log:
            print("[LOG:STATE] Dimension set to " + str(data.states.dimensions) + "D.")
        data.rotation.center = [0,0]
        if data.states.dimensions == 2:
            data.rotation.plane = [0,1]
        else:
            data.rotation.plane = [0,2]
        data.wireframe.lines.clear()
        render.redraw()
        break

def handle_clear():
    """Clear all lines from the wireframe and refresh the display."""
    data.wireframe.lines.clear()
    render.redraw()
    if data.states.log:
        print("[LOG:VIEW] Screen cleared.")

def handle_log():
    """Toggle logging of actions and state changes on or off."""
    data.states.log = not data.states.log
    print("[INFO] Logging set to " + str(data.states.log) + ".")
    render.redraw()

def handle_view_lines():
    """Display all current lines in the wireframe."""
    if len(data.wireframe.lines) == 0:
        print("[INFO] No lines currently present on the screen.")
    else:
        proceed = True
        lines_before_warning = 50
        if len(data.wireframe.lines) >= lines_before_warning:
            print("[NOTICE] Large number of lines present.")
            while True:
                user_input = input("    You are about to print " + str(len(data.wireframe.lines)) + " lines. Are you sure you want to proceed? (y/n) ")
                if user_input == "/" or user_input.lower() == "n":
                    proceed = False
                    break
                elif user_input.lower() == "y":
                    break
                else:
                    print("Invalid response!")
        if proceed:
            i = 1
            for line in data.wireframe.lines:
                print("Line " + str(i) + ": (" + " ".join(map(str, line[0])) + ") - (" + " ".join(map(str, line[1])) + ")")
                i += 1

def handle_center():
    """Prompt the user to set the center of the rotation plane."""
    while True:
        user_input = input("Enter the center of the rotation plane: ")
        if user_input == "/":
            break
        center_point = user_input.split()
        if not utils.valid_input(center_point,2):
            print("Invalid coordinates!")
            continue
        data.rotation.center = [float(center_point[0]),float(center_point[1])]
        render.redraw()
        if data.states.log:
            print("[LOG:STATE] Rotation center set to (" + str(data.rotation.center[0]) + "," + str(data.rotation.center[1]) + ").")
        break

def handle_plane():
    """Prompt the user to set the rotation plane."""
    while True:
        user_input = input("Enter the plane of rotation: ")
        if user_input == "/":
            break
        plane = user_input.split()
        if (not utils.valid_input(plane,2)) or int(plane[0]) == int(plane[-1]) or int(plane[0]) >= data.states.dimensions or int(plane[1]) >= data.states.dimensions or int(plane[0]) < 0 or int(plane[1]) < 0:
            print("Invalid plane!")
            continue
        plane[0] = int(plane[0])
        plane[1] = int(plane[1])
        data.rotation.plane = plane
        render.redraw()
        if data.states.log:
            print("[LOG:STATE] Rotation plane set to (" + str(min(data.rotation.plane)) + "," + str(max(data.rotation.plane)) + ").")
        break

def handle_load():
    """Prompt the user to load lines from a file."""
    while True:
        user_input = input("Enter the file name: ")
        if user_input == "/":
            break
        if not os.path.exists("file_shapes"):
            os.makedirs("file_shapes")
            print("[INFO] Created missing folder: 'file_shapes'.")
        file_name = "file_shapes/" + user_input + ".txt"
        if utils.valid_file(file_name):
            with open(file_name,"r") as file_pointer:
                lines = 0
                for line in file_pointer:
                    test_line = line.split()
                    # Don't compute empty lines or comments
                    if len(test_line) == 0 or test_line[0] == "#":
                        continue
                    point_one = test_line[:data.states.dimensions]
                    point_two = test_line[data.states.dimensions:]
                    for i in range(data.states.dimensions):
                        point_one[i] = float(point_one[i])
                        point_two[i] = float(point_two[i])
                    render.add_line(point_one,point_two)
                    lines += 1
                print("[SUCCESS] " + str(lines) + " lines loaded from file {" + file_name + "}.")
                break

def handle_save():
    """Prompt the user to save all current lines to a file."""
    while True:
        proceed = True
        invalid_characters = " \\/.<>?*:|\""
        user_input = input("Enter the file name: ")
        if user_input == "/":
            break
        if user_input == "" or any (ch in invalid_characters for ch in user_input):
            print("Invalid file name!")
            continue
        if not os.path.exists("file_shapes"):
            os.makedirs("file_shapes")
            print("[INFO] Created missing folder: 'file_shapes'.")
        file_name = "file_shapes/" + user_input + ".txt"
        if os.path.exists(file_name):
            while True:
                print("[NOTICE] '" + user_input + ".txt' already exists in folder 'file_shapes'.")
                overwrite = input("     Are you sure you want to overwrite the existing file? (y/n) ")
                if overwrite == "/" or overwrite.lower() == "n":
                    proceed = False
                    break
                elif overwrite.lower() == "y":
                    break
                else:
                    print("Invalid response!")
        # Ensures that the object won't be saved if the user decides not to overwrite a file
        if proceed:
            with open(file_name,"w") as file_pointer:
                file_pointer.write("# === Saved Wireframe ===\n")
                file_pointer.write("#   Required Dimensions: " + str(data.states.dimensions) + "\n")
                file_pointer.write("#   Lines: " + str(len(data.wireframe.lines)) + "\n")
                file_pointer.write("\n\n\n")
                for line in data.wireframe.lines:
                    for point in line:
                        for coordinate in point:
                            file_pointer.write(str(coordinate) + " ")
                    file_pointer.write("\n")
                print("[SUCCESS] " + str(len(data.wireframe.lines)) + " lines saved to file {" + file_name + "}.")
                break

def handle_preset():
    """Prompt the user to load a preset object (e.g., hypercube or hyperpyramid)."""
    available_presets = ["hypercube","hyperpyramid"]
    while True:
        user_input = input("Enter a preset: ")
        if user_input == "/":
            break
        if user_input not in available_presets:
            print("Not a preset!")
            print("Available presets:")
            for preset in available_presets:
                print("     " + preset)
            continue
        if user_input == "hypercube":
            presets.hypercube(data.states.dimensions)
            if data.states.log:
                print("[LOG:LOAD] Object hypercube loaded in " + str(data.states.dimensions) + " dimensions.")
        if user_input == "hyperpyramid":
            presets.hyperpyramid(data.states.dimensions)
            if data.states.log:
                print("[LOG:LOAD] Object hyperpyramid loaded in " + str(data.states.dimensions) + " dimensions.")
        render.redraw()
        break

def panel():
    """Main command panel loop: prompts the user for commands and executes the corresponding handlers."""
    command_handler = {
        "add": handle_add,
        "remove": handle_remove,
        "dimensions": handle_dimensions,
        "clear": handle_clear,
        "log": handle_log,
        "view lines": handle_view_lines,
        "center": handle_center,
        "plane": handle_plane,
        "load": handle_load,
        "save": handle_save,
        "help": command_options,
        "keys": actions,
        "preset": handle_preset
    }
    command = ""
    while True:
        command = input("Enter a command: ").lower()
        if command == "/":
            break
        elif command == "quit":
            data.states.quit = True
            break
        if command not in command_handler:
            print("Invalid command!")
            print("     Enter 'help' to view available commands.")
            continue
        command_handler[command]()