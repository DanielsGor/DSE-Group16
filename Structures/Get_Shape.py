#LIBRARY-------------------------------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import math
#inpute: amount of spars, skin geometry, spar thickness
#Output: type, dimensions, Ixx, Iyy, Ixy, J

#FUNCTIONS-------------------------------------------------------------------------------------------------------
# Open the text document
x_airfoil = []
y_airfoil = []
with open("AirfoilData/NACA0012.txt", "r") as file:
    for line in file:
        # Read the contents of the file
        x, y = map(float, line.strip().split())

        # Append coordinates to the lists
        x_airfoil.append(x)
        y_airfoil.append(y)
    x_airfoil = [value * .001 for value in x_airfoil]
    y_airfoil = [value * .001 for value in y_airfoil]

    plt.plot(x_airfoil, y_airfoil, 'bo')  # 'bo' specifies blue color and circle markers
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Check general airfoil geometry')
    plt.axis('equal')
    plt.grid(True)
    plt.show()


#giving wing crossection for given span_x and airfoil geometry-------------------------------
def get_spanwisegeom(span_x, x_airfoil, y_airfoil, C_root, C_tip, span):
    factor = C_root - ((span_x / span) * (C_root - C_tip))
    newx_airfoil = [value * factor for value in x_airfoil]
    newy_airfoil = [value * factor for value in y_airfoil]
    return newx_airfoil, newy_airfoil, factor

def find_closest_number_indices(lst, target):
    closest_numbers = sorted(lst, key=lambda x: abs(x - target))[:2]
    closest_indices = [i for i, num in enumerate(lst) if num in closest_numbers]
    return closest_indices

def get_cg(x_spars, y_spars, spar_w, spar_t):
    x_areaxdistance = 0
    y_areaxdistance = 0
    area = 0
    #define cg of all flanges together
    for i in range(len(x_spars)):
        area += spar_w*spar_t
        x_areaxdistance += (spar_w*spar_t)*x_spars[i]
        y_areaxdistance += (spar_w*spar_t)*y_spars[i]
    rangi = np.arange(0, len(x_spars), 2)
    for i in rangi:
        area += (y_spars[i]-y_spars[i+1])*spar_t
        x_areaxdistance += ((y_spars[i]-y_spars[i+1])*spar_t)*(.5*(x_spars[i]+x_spars[i+1]))
        y_areaxdistance += ((y_spars[i]-y_spars[i+1])*spar_t)*(.5*(y_spars[i]+y_spars[i+1]))
    x_cg = x_areaxdistance/area
    y_cg = y_areaxdistance/area
    return(x_cg, y_cg)


def calculate_spline_length_and_centroid(x_coordinates, y_coordinates):
    n = len(x_coordinates) - 1
    h = (x_coordinates[-1] - x_coordinates[0]) / n

    # Calculate the weights for the Simpson's rule
    weights = np.ones(n + 1)
    weights[1:-1:2] = 4
    weights[2:-1:2] = 2

    # Calculate the sum of the weighted x-coordinates
    sum_of_weights_x = np.sum(weights * x_coordinates[:-1])  # Exclude the last element

    # Calculate the sum of the weighted y-coordinates
    sum_of_weights_y = np.sum(weights * y_coordinates[:-1])  # Exclude the last element

    # Calculate the area under the curve
    area = (h / 3) * np.sum(weights)

    # Calculate the centroid coordinates
    x_centroid = (1 / area) * ((h / 3) * sum_of_weights_x)
    y_centroid = (1 / area) * ((h / 3) * sum_of_weights_y)

    # Calculate the length using Simpson's rule formula
    length = (h / 3) * np.sum(
        weights * np.sqrt(np.power(np.diff(x_coordinates, n=1), 2) + np.power(np.diff(y_coordinates, n=1), 2)))

    return length, x_centroid, y_centroid


def split_list_at_numbers(lst, split_nums):
    splitted_lists = []
    sublist = []

    for item in lst:
        sublist.append(item)
        if item in split_nums:
            splitted_lists.append(sublist.copy())
            sublist.clear()
            sublist.append(item)
    splitted_lists.append(sublist)

    return splitted_lists

def calculate_spline_length(x, y):
    total_length = 0
    for i in range(len(x) - 1):
        x1, y1 = x[i], y[i]
        x2, y2 = x[i + 1], y[i + 1]

        segment_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        total_length += segment_length

    return total_length





#calculate evenly spaced locations for spars--------------------------------------------------
#def getsparlocation(sparnr, factor):
#    sparlocation = []
#    for i in range(sparnr):
#        sparlocation.append((factor* ((i+1)/(sparnr+1)))*1000)
#    return(sparlocation)






#INPUTS----------------------------------------------------------------------------------------------------------
sparlocation = [.3, .6] #factor of the cord
span_x = .1         #meters
C_root = 6          #meters
C_tip = 4           #meters
span = 2            #meters
spar_w = .2         #meters
spar_t = .2         #meters
skin_t = .2         #meters
#MAIN PROGRAM---------------------------------------------------------------------------------------------
newx_airfoil, newy_airfoil, factor = get_spanwisegeom(span_x, x_airfoil, y_airfoil, C_root, C_tip, span)
sparlocation = np.array(sparlocation)*factor*1000

x_spars = []
y_spars = []
for i in sparlocation:
    x_index = find_closest_number_indices(newx_airfoil, i)
    for i in x_index:
        x_spars.append(newx_airfoil[i])
        y_spars.append(newy_airfoil[i])
x_cg, y_cg = get_cg(x_spars, y_spars, spar_w, spar_t)
x_splines = split_list_at_numbers(newx_airfoil, x_spars)
y_splines = split_list_at_numbers(newy_airfoil, y_spars)

spline_lengths = []
spline_cgx = []
spline_cgy = []
for i in range(len(x_splines)):
    spline_lengths.append(calculate_spline_length(x_splines[i], y_splines[i]))
    spline_cgx.append(np.average(x_splines[i]))
    spline_cgy.append(np.average(y_splines[i]))
print(spline_lengths)
print(spline_cgx)
print(spline_cgy)



for i in sparlocation:
    x_index = find_closest_number_indices(newx_airfoil, i)
    plt.vlines(x=i, ymin=newy_airfoil[x_index[1]], ymax=newy_airfoil[x_index[0]], colors='black', ls='solid', lw=2)
plt.plot(newx_airfoil, newy_airfoil, 'r')  # 'ro' specifies red color and circle markers
plt.scatter(x_cg, y_cg)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Local airfoil geometry')
plt.axis('equal')
plt.grid(True)
plt.show()







#def getgeompar(airfoil, n_string, t_string)


    #return(geom, Ixx, Iyy, Ixy)

