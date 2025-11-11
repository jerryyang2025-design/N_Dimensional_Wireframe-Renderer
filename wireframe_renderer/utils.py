"""
Module providing utility functions for the N-Dimensional Wireframe Renderer.

Includes functions for geometric calculations, 2D projection of 
N-dimensional points, equality checks, input validation, and file validation 
for wireframe data.
"""

import math
import data

def points_equal(p1, p2, tol=1e-6):
    """Return True if two points are equal within a specified tolerance."""
    return all(math.isclose(a, b, abs_tol=tol) for a, b in zip(p1, p2))

def lines_equal(l1, l2, tol=1e-6):
    """Return True if two lines (pairs of points) are equal."""
    return ((points_equal(l1[0], l2[0], tol) and points_equal(l1[1], l2[1], tol)) or 
            (points_equal(l1[0], l2[1], tol) and points_equal(l1[1], l2[0], tol)))

def pythag(rx,ry):
    """Return the Euclidean distance (hypotenuse) for a right triangle with sides rx and ry."""
    return math.sqrt(rx ** 2 + ry ** 2)

def bound_TR(d):
    """Return the transformed coordinate for perspective projection, or None if out of bounds."""
    if d >= data.wireframe.side + data.display.side / data.states.perspective:
        return None
    # Equation representing the FOV bounds with a slope of perspective and centered so presets fit screen
    return -data.states.perspective * (d - data.wireframe.side) + data.display.side

def project(point,scale):
    """Project a single coordinate to 2D based on perspective and scaling, or return None if invalid."""
    projected_point = bound_TR(float(scale))
    if projected_point is None:
        return None
    elif abs(projected_point) < 0.1:
        # Don't draw the line if it will result in a divide by 0 or near 0 error
        return None
    # Calculates the screen coordinate position based on the screen size and FOV bound size its true coordinate position (the last coordinate value)
    return data.display.half_side * float(point) / float(projected_point)

def project_to_2d(point_1,point_2):
    """Project two N-dimensional points to 2D coordinates for rendering, or return None if not visible."""
    position_1, position_2 = point_1[:], point_2[:]
    # Continuously projects down a dimension until it reaches 2D
    while len(position_1) > 2:
        for i in range(len(position_1) - 1):
            position_1[i] = project(position_1[i],position_1[-1])
            position_2[i] = project(position_2[i],position_2[-1])
            if position_1[i] is None or position_2[i] is None:
                return None
        position_1.pop()
        position_2.pop()
    return (position_1,position_2)

def valid_input(position,length):
    """Return True if a list of coordinates has the correct length and all elements are numeric."""
    if len(position) == length:
        try:
            for value in position:
                float(value)
            return True
        except ValueError:
            return False
    else:
        return False

def valid_file(file_name):
    """Return True if a file contains valid lines for the current dimension, False otherwise, with error messages."""
    try:
        with open(file_name,"r") as file_pointer:
            index = 0
            for line in file_pointer:
                index += 1
                test_line = line.split()
                if len(test_line) == 0 or test_line[0] == "#":
                    continue
                if len(test_line) != data.states.dimensions * 2:
                    print("[ERROR] File is not supported for " + str(data.states.dimensions) + " dimensions.")
                    return False
                point_one = test_line[:data.states.dimensions]
                point_two = test_line[data.states.dimensions:]
                if not valid_input(point_one,data.states.dimensions) or not valid_input(point_two,data.states.dimensions):
                    print("[ERROR] File contains unrecognized characters at line " + str(index) + ".")
                    return False
            return True
    except FileNotFoundError:
        print("[ERROR] File name not recognized.")
        print("     Ensure that the file exists and is placed in the 'file_shapes' folder.")
        return False