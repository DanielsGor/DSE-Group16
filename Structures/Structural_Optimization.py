from Get_Fuselage import *
from constants import df
#   Clean this code

class fuselage:
    def __init__(self):
        # create self attributes with the lines of code below
        self.length = df['fus_l']  # Length of the fuselage in meters
        self.width = df['fus_w']  # Width of the fuselage in meters
        self.height = df['fus_h']  # Height of the fuselage in meters
        self.skin_thickness = df['t_skin']  # Thickness of the fuselage skin in meters
        self.mass = df['fus_h']  # Fuselage mass in kg
        self.wingbox_location = None    # Distance of the wingbox edge from the fuselage nose in meters
        self.root_chord = df['c_r']  # Root chord of the wing in meters
        self.stringer_width = df['str_w']  # Width of the stringers in meters
        self.stringer_height = df['str_h']  # Height of the stringers in meters
        self.stringer_thickness = df['str_t']  # Thickness of the stringers in meters
        self.balsa_tens = df['balsa_tens']  # Tensile strength of balsasud ultralite in MPa
        self.balsa_comp = df['balsa_comp']  # Compressive strength of balsasud ultralite in MPa
        self.balsa_shear = None  # Shear strength of balsasud ultralite in MPa
        self.n_stringers = None
        self.internal_shear = None
        self.internal_bending = None
        self.internal_normal = None
        self.normal_stress = None
        self.wing_lift = None  # Lift of the main wing in Newtons
        self.wing_drag = None  # Drag of the main wing in Newtons
        self.wing_moment = None  # Moment of the main wing in Newtons per meter


# Define the optimization parameters
max_stringer_number = 10  # Maximum number of stringers allowed
max_stringer_dimension = 100  # Maximum dimension of stringers allowed
max_weight = float('inf')  # Maximum weight allowed (initialized with infinity)
min_cost = float('inf')  # Minimum cost (initialized with infinity)
max_recyclability = 0  # Maximum recyclability (initialized with 0)

# Loop through different stringer numbers and dimensions
for stringer_number in range(1, max_stringer_number + 1):
    for height in range(1, max_stringer_dimension + 1):
        for width in range(1, max_stringer_dimension + 1):
            for thickness in range(1, max_stringer_dimension + 1):
                # Calculate weight based on stringer number and dimensions
                weight = calculate_weight(stringer_number, height, width, thickness)

                # Calculate cost based on stringer number and dimensions
                cost = calculate_cost(stringer_number, height, width, thickness)

                # Calculate recyclability based on stringer number and dimensions
                recyclability = calculate_recyclability(stringer_number, height, width, thickness)

                # Check if the current solution is better than the previous best
                if weight <= max_weight and cost <= min_cost and recyclability >= max_recyclability:
                    # Update the best solution
                    best_stringer_number = stringer_number
                    best_height = height
                    best_width = width
                    best_thickness = thickness
                    max_weight = weight
                    min_cost = cost
                    max_recyclability = recyclability

# Print the optimized solution
print("Optimized Solution:")
print("Stringer Number:", best_stringer_number)
print("Height:", best_height)
print("Width:", best_width)
print("Thickness:", best_thickness)
print("Weight:", max_weight)
print("Cost:", min_cost)
print("Recyclability:", max_recyclability)




