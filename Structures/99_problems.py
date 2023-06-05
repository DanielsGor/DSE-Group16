from constants import df
#   Loads are going to affect the configuration

#   Belly landing loads
#   Cruise loads
#   Climb loads
#   Wingbox loads
#   Catapult attachment points and loads

#   Fuselage components configuration (01/06): width = 0.15 m height = 0.15 m length = 0.7 m

#   Process: start with an initial number of structural elements (stringers, formers n+r, rods, skin), evaluate and iterate
#   (increase number of failing elements and reduce redundant ones)

#   Input: loads
#   Output: placement of stringers, formers n+r and rods, dimensions of stringers, formers n+r, rods and skin
#   Ixx assumption: only stringers contribute
#   Cross-sectional area A: stringers and skin

import numpy as np

class fuselage:
    def __init__(self):
        # create self attributes with the lines of code below
        self.length = df['fus_l']  # Length of the fuselage in meters
        self.width = df['fus_w']  # Width of the fuselage in meters
        self.height = df['fus_h']  # Height of the fuselage in meters
        self.skin_thickness = df['t_skin']  # Thickness of the fuselage skin in meters
        self.stringer_pitch = df['str_pitch']  # Spacing between stringers in meters
        self.stringer_width = df['str_w']  # Width of the stringers in meters
        self.stringer_height = df['str_h']  # Height of the stringers in meters
        self.stringer_thickness = df['str_t']  # Thickness of the stringers in meters
        self.balsa_tens = df['balsa_tens']  # Tensile strength of balsasud ultralite in MPa
        self.balsa_comp = df['balsa_comp']  # Compressive strength of balsasud ultralite in MPa
        self.internal_shear = None
        self.internal_bending = None
        self.pitch_list = None
        self.normal_stress = None
        self.p = None
    def test(self):
        print(self.length)

def fuselage_layout():
    fuselage_length = 0.7  # Length of the fuselage in meters
    fuselage_width = 0.15  # Width of the fuselage in meters
    fuselage_height = 0.15  # Height of the fuselage in meters
    skin_thickness = 0.01  # Thickness of the fuselage skin in meters
    stringer_pitch = 0.2  # Spacing between stringers in meters
    stringer_width = 0.02  # Width of the stringers in meters
    stringer_height = 0.02  # Height of the stringers in meters
    stringer_thickness = 0.005  # Thickness of the stringers in meters
    #   For wood materials, assume that yield strength = ultimate strength, use graphs for support
    balsa_tstrength = 7.501  # Tensile strength of balsasud ultralite in MPa
    balsa_cstrength = 6.53  # Compressive strength of balsasud ultralite in MPa

    #   Internal loading diagrams should be made here
    #   Dummy values are used for now
    internal_shear = np.append(np.arange(0, 50), np.arange(50, 0, -1))
    internal_bending = np.append(100 * np.ones(50), 50 * np.ones(50))

    pitch_list = np.arange(0.01, 0.7, 0.01)

    normal_stress = 0
    p = 0.15

    while np.all(normal_stress) < balsa_tstrength and np.all(normal_stress) < balsa_cstrength:
        n = fuselage_width // p
        stringer_area = (stringer_width + stringer_height) * stringer_thickness - stringer_thickness ** 2
        Ixx = 2 * n * stringer_area * (fuselage_height / 2) ** 2
        normal_stress = internal_bending * fuselage_height / (Ixx * 2)
        p = p + 0.01


    return normal_stress, p

# d = fuselage_layout()

# print(d)
#   The following function is ChatGPT's stupid invention (it obviously does not work, but gave me a nice idea
def generate_fuselage_layout(loads):
    # Define the dimensions and materials of the fuselage
    fuselage_length = 10.0  # Length of the fuselage in meters
    fuselage_diameter = 1.0  # Diameter of the fuselage in meters
    skin_thickness = 0.01  # Thickness of the fuselage skin in meters
    stringer_spacing = 0.2  # Spacing between stringers in meters
    stringer_width = 0.02  # Width of the stringers in meters
    stringer_thickness = 0.005  # Thickness of the stringers in meters
    material_strength = 1000.0  # Material strength in megapascals (MPa)

    # Calculate the cross-sectional area of the fuselage
    fuselage_area = 2 * 3.14159 * (fuselage_diameter / 2) * fuselage_length

    # Calculate the total force acting on the fuselage
    total_force = sum(loads.values())

    # Calculate the required number of stringers based on the total force
    num_stringers = int(total_force / (stringer_spacing * material_strength * stringer_thickness))

    # Calculate the load on each stringer
    stringer_load = total_force / num_stringers

    # Calculate the required thickness of the skin
    skin_thickness = stringer_load / (2 * material_strength * fuselage_area)

    # Generate the stringer and skin layout
    stringer_layout = "Stringer Layout:\n"
    for i in range(num_stringers):
        stringer_layout += f"Stringer {i+1}: Position: {i * stringer_spacing}m\n"

    skin_layout = "Skin Layout:\n"
    skin_layout += f"Thickness: {skin_thickness}m\n"

    return stringer_layout + "\n" + skin_layout

# Example usage:
loads = {
    "axial": 10000.0,  # Axial load in newtons
    "bending": 5000.0,  # Bending load in newton-meters
    "shear": 2000.0  # Shear load in newtons
}


