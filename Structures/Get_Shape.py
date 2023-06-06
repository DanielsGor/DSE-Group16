import numpy as np
import matplotlib.pyplot as plt
#inpute: amount of spars, skin geometry, spar thickness
#Output: type, dimensions, Ixx, Iyy, Ixy, J


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

    plt.plot(x_airfoil, y_airfoil, 'b')  # 'bo' specifies blue color and circle markers
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Check general airfoil geometry')
    plt.axis('equal')
    plt.grid(True)
    plt.show()


#giving wing crossection for given span_x and airfoil geometry-------------------------------
def get_spanwisegeom(span_x, x_airfoil, y_airfoil, C_root, C_tip, span):
    factor = C_root - ((span_x / span) * (C_root - C_tip))
    print(factor)
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
    sum_of_weights_x = np.sum(weights * x_coordinates)

    # Calculate the sum of the weighted y-coordinates
    sum_of_weights_y = np.sum(weights * y_coordinates)

    # Calculate the area under the curve
    area = (h / 3) * np.sum(weights)

    # Calculate the centroid coordinates
    x_centroid = (1 / area) * ((h / 3) * sum_of_weights_x)
    y_centroid = (1 / area) * ((h / 3) * sum_of_weights_y)

    # Calculate the length using Simpson's rule formula
    length = (h / 3) * np.sum(
        weights * np.sqrt(np.power(np.diff(x_coordinates), 2) + np.power(np.diff(y_coordinates), 2)))

    return length, x_centroid, y_centroid





#calculate evenly spaced locations for spars--------------------------------------------------
#def getsparlocation(sparnr, factor):
#    sparlocation = []
#    for i in range(sparnr):
#        sparlocation.append((factor* ((i+1)/(sparnr+1)))*1000)
#    return(sparlocation)






#inputs of the program-----------------------------
sparlocation = [.3, .6] #should be within root cord length
#sparnr = 3
span_x = .1         #meters
C_root = 6          #meters
C_tip = 4           #meters
span = 2            #meters
spar_w = .2         #meters
spar_t = .2
#---------------------------------------------------
newx_airfoil, newy_airfoil, factor = get_spanwisegeom(span_x, x_airfoil, y_airfoil, C_root, C_tip, span)
sparlocation = np.array(sparlocation)*factor*1000
print(sparlocation)

x_spars = []
y_spars = []
for i in sparlocation:
    x_index = find_closest_number_indices(newx_airfoil, i)
    for i in x_index:
        x_spars.append(newx_airfoil[i])
        y_spars.append(newy_airfoil[i])
x_cg, y_cg = get_cg(x_spars, y_spars, spar_w, spar_t)

print(x_spars)
print(y_spars)

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

