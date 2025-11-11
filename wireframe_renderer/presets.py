"""
Module for generating predefined N-dimensional wireframe objects.

Provides functions to create common geometric shapes such as hypercubes 
and hyperpyramids, automatically adding their edges to the wireframe 
for rendering in the N-Dimensional Wireframe Renderer.
"""

import render
import data

def hypercube(dimensions):
    """Create a hypercube of the given dimensions and add its edges to the wireframe."""
    points = []
    second_points = []
    number_of_points = 2 ** dimensions
    for i in range(number_of_points - 1):
        point = []
        i += 1
        for j in range(dimensions):
            j = dimensions - j - 1
            # Uses binary logic to find the points of the hypercube, subtracting the largest values first to determine the binary sequence
            if (i - (2 ** j)) >= 0:
                point.append(data.wireframe.side)
                i = i - (2 ** j)
            else:
                point.append(-data.wireframe.side)
        points.append(point)
        second_points.append(point)
    # Adds the last point manually
    point = [-data.wireframe.side] * dimensions
    points.append(point)
    second_points.append(point)
    for i in points:
        second_points.remove(i)
        for j in second_points:
            different = 0
            # Add lines between points with a single differing coordinate
            for k in range(dimensions):
                if i[k] != j[k]:
                    different += 1
            if different == 1:
                render.add_line(i,j)
                
def hyperpyramid(dimensions):
    """Create a hyperpyramid of the given dimensions and add its edges to the wireframe (requires dimensions >= 3)."""
    if data.states.dimensions == 2:
        print("[NOTICE] Action terminated.")
        print("     Reason: Hyperpyramid requires dimensions >= 3.")
        return
    points = []
    second_points = []
    # Creates a hypercube in dimension - 1
    dimensions += -1
    number_of_points = 2 ** dimensions
    for i in range(number_of_points - 1):
        point = []
        i += 1
        for j in range(dimensions):
            # Hardcodes the y coordinate to -side length
            if j == 1:
                point.append(-data.wireframe.side)
            j = dimensions - j - 1
            if (i - (2 ** j)) >= 0:
                point.append(data.wireframe.side)
                i = i - (2 ** j)
            else:
                point.append(-data.wireframe.side)
        points.append(point)
        second_points.append(point)
    point = [-data.wireframe.side] * (dimensions + 1)
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
                render.add_line(i,j)
    # Adds the apex point and connects every other point to it
    point = [0,data.wireframe.side] + [0] * (dimensions - 1)
    for i in points:
        render.add_line(i,point)