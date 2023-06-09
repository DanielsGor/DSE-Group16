import numpy as np

def scale_coordinates(filename, chord):
    # Open the file for reading
    with open(filename, 'r') as file:
        # Read the lines from the file
        lines = file.readlines()

    # Create an empty list to store the scaled coordinates
    scaled_coordinates = []

    # Iterate over each line
    for line in lines:
        # Split the line into two coordinates
        x, y = map(float, line.strip().split())

        # Scale the coordinates by the factor
        scaled_x = x * chord
        scaled_y = y * chord

        # Add the scaled coordinates to the list
        scaled_coordinates.append((scaled_x, scaled_y))

    # Return the scaled coordinates
    return scaled_coordinates

# Example usage
filename = 'NACA642-015A.txt'
chord = 1/(2.862864*10*6)   #in mm

scaled_coords = scale_coordinates(filename, chord)
print(scaled_coords)
np.savetxt('NACA642-015A.txt', scaled_coords)
