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
    spararea = 0
    #define cg of all flanges together
    for i in range(len(x_spars)):
        spararea += spar_w*spar_t
        x_areaxdistance += (spar_w*spar_t)*x_spars[i]
        y_areaxdistance += (spar_w*spar_t)*y_spars[i]
    rangi = np.arange(0, len(x_spars), 2)
    for i in rangi:
        spararea += (y_spars[i]-y_spars[i+1])*spar_t
        x_areaxdistance += ((y_spars[i]-y_spars[i+1])*spar_t)*(.5*(x_spars[i]+x_spars[i+1]))
        y_areaxdistance += ((y_spars[i]-y_spars[i+1])*spar_t)*(.5*(y_spars[i]+y_spars[i+1]))
    x_cg = x_areaxdistance/spararea
    y_cg = y_areaxdistance/spararea
    return(x_cg, y_cg, spararea)


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
    segment_length = []
    segment_cgx = []
    segment_cgy = []
    for i in range(len(x) - 1):
        x1, y1 = x[i], y[i]
        x2, y2 = x[i + 1], y[i + 1]
        segment_length.append(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))
        segment_cgx.append((x1+x2)/2)
        segment_cgy.append((y1+y2)/2)
        segments = np.array([segment_length, segment_cgx, segment_cgy])
    cg_spine = np.array([np.sum(segments[0]*segments[1])/np.sum(segments[0]),
                         np.sum(segments[0]*segments[2])/np.sum(segments[0])])
    total_length = np.sum(segment_length)

    return total_length, segments, cg_spine

a , b, cg_spine = calculate_spline_length(x_airfoil, y_airfoil)

def IdealisedBoom(w_cap, t_cap, x_cgcap, y_cgcap, t_skin, cg_airfoil, Mx, My, spline, it):
    cg_cap = np.array([x_cgcap, y_cgcap])
    for i in range(len(cg_cap[0])):
        cg_cap[:,i] = cg_cap[:,i] - cg_airfoil
    sigma = np.zeros(len(cg_cap[0]))
    B = np.full(4, w_cap * t_cap)
    Bskin = np.zeros(4)
    Btot = np.zeros((it,4))
    for i in range(it):
        Ixx = np.sum(cg_cap[1,:] ** 2 * (B + Bskin))
        Iyy = np.sum(cg_cap[0,:] ** 2 * (B + Bskin))
        Ixy = np.sum(cg_cap[0,:] * cg_cap[1,:] * (B + Bskin))
        for j in range(len(cg_cap[0])):
            # Calculates sigma in whatever Mx and My are given in divided by mm^2
            sigma[j] = ((Mx * Iyy - My * Ixy) / (Ixx * Iyy - Ixy ** 2)) * cg_cap[1, j] + ((My * Ixx - Mx * Ixy) / (Ixx * Iyy - Ixy ** 2)) * cg_cap[0, j]
        Bskin[0] = t_skin * (np.abs(cg_cap[1,0] - cg_cap[1,1])) / 6 * (2 + sigma[1]/sigma[0]) + t_skin * (spline[1]) / 6 * (2 + sigma[2]/sigma[0])
        Bskin[1] = t_skin * (np.abs(cg_cap[1,1] - cg_cap[1,0])) / 6 * (2 + sigma[0]/sigma[1]) + t_skin * (spline[3]) / 6 * (2 + sigma[3]/sigma[1])
        Bskin[2] = t_skin * (np.abs(cg_cap[1,2] - cg_cap[1,3])) / 6 * (2 + sigma[3]/sigma[2]) + t_skin * (spline[1]) / 6 * (2 + sigma[0]/sigma[1])
        Bskin[3] = t_skin * (np.abs(cg_cap[1,3] - cg_cap[1,2])) / 6 * (2 + sigma[2]/sigma[3]) + t_skin * (spline[3]) / 6 * (2 + sigma[1]/sigma[3])
        Btot[i,:] = B + Bskin
    return Btot









# length, segments = calculate_spline_length(newx_airfoil, newy_airfoil)
# print(length)
# print(segments)



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
spar_w = 200         #mm
spar_t = 20         #mm
skin_t = 1         #mm


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
sparx_cg, spary_cg, spararea = get_cg(x_spars, y_spars, spar_w, spar_t)
x_splines = split_list_at_numbers(newx_airfoil, x_spars)
y_splines = split_list_at_numbers(newy_airfoil, y_spars)

spline_lengths = []
spline_cgx = []
spline_cgy = []


for i in range(len(x_splines)):
    spline_lengths.append(calculate_spline_length(x_splines[i], y_splines[i])[0]) #use new function ONNO
    spline_cgx.append(calculate_spline_length(x_splines[i], y_splines[i])[2][0]) #use new function ONNO
    spline_cgy.append(calculate_spline_length(x_splines[i], y_splines[i])[2][1]) #use new function ONNO

print(spline_lengths)
print(spline_cgx)
print(spline_cgy)


total_area = 0
total_areax = 0
total_areay = 0
for i in range(len(spline_lengths)):
    total_area += spline_lengths[i]*skin_t
    total_area += spararea
    total_areax += spline_lengths[i]*skin_t*spline_cgx[i]
    total_areax += sparx_cg*spararea
    total_areay += spline_lengths[i]*skin_t*spline_cgy[i]
    total_areay += spary_cg * spararea

totalcg_x = total_areax/total_area
totalcg_y = total_areay/total_area

for i in sparlocation:
    x_index = find_closest_number_indices(newx_airfoil, i)
    plt.vlines(x=i, ymin=newy_airfoil[x_index[1]], ymax=newy_airfoil[x_index[0]], colors='black', ls='solid', lw=2)
plt.plot(newx_airfoil, newy_airfoil, 'r')  # 'ro' specifies red color and circle markers
plt.scatter(totalcg_x, totalcg_y)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Local airfoil geometry')
plt.axis('equal')
plt.grid(True)
plt.show()







#def getgeompar(airfoil, n_string, t_string)


    #return(geom, Ixx, Iyy, Ixy)

