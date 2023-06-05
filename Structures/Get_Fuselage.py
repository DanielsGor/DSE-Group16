import numpy as np
#   Clean this code

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
def fuselage_layout(loads, fuselage_dimensions, stringer_dimensions, material_properties):
    #   Fuselage dimensions: width, height  (in m)
    #   Stringer dimensions: width, height, thickness   (in m)
    #   Material properties: tensile yield strength, compressive yield strength, shear yield strength (in MPa)
    #   https://www.matweb.com/search/DataSheet.aspx?MatGUID=cde2cfd21dc446c69fb7e4c3a39880ed

    fuselage_width = fuselage_dimensions['width']
    fuselage_height = fuselage_dimensions['height']

    stringer_width = stringer_dimensions['width']
    stringer_height = stringer_dimensions['height']
    stringer_thickness = stringer_dimensions['thickness']

    balsa_tstrength = material_properties['tensile strength']
    balsa_cstrength = material_properties['compressive strength']
    balsa_sstrength = material_properties['shear strength']

    internal_shear = loads['shear']
    internal_bending = loads['bending']
    internal_normal = loads['normal']
    size = np.size(internal_shear)

    #   Bending and normal load analysis
    #   Neglect the contribution of the skin
    #   Neglect fuselage drag
    #   Parallel axis theorem is the dominant contributor to the moment of inertia

    stringer_area = 2 * stringer_width * stringer_thickness + stringer_height * stringer_thickness \
                    - 2 * stringer_thickness ** 2
    normal_stress_total = np.zeros(size)    # In Mpa
    a = False
    n_stringers_normal = 0   # Number of stringers
    while a == False and n_stringers_normal * stringer_width < fuselage_width:
        n_stringers_normal = n_stringers_normal + 1
        Ixx_individual = stringer_area * (fuselage_height / 2) ** 2
        Ixx = Ixx_individual * n_stringers_normal
        normal_stress_bending = internal_bending * fuselage_height / (Ixx * 2 * 10 ** 6)    # Converted to MPa
        normal_stress = internal_normal / (n_stringers_normal * stringer_area * 10 ** 6)
        normal_stress_total = normal_stress + normal_stress_bending
        if np.all(normal_stress_total < balsa_tstrength) and np.all(normal_stress_total < balsa_cstrength):
            a = True

    #   Shear load analysis
    #   Shear forces distributed equally between stringers
    shear_stress = np.zeros(size)    # In Mpa
    b = False
    n_stringers_shear = 0
    while b == False and n_stringers_shear * stringer_width < fuselage_width:
        n_stringers_shear = n_stringers_shear + 1
        Vy = internal_shear / n_stringers_shear
        Ixx_individual = stringer_thickness * stringer_height ** 3 / 12 +\
                         stringer_thickness * stringer_width * stringer_height ** 2 / 2
        #   For a c stringer loaded in the y direction, maximum shear stress is in the middle vertical plate
        shear_stress = Vy * stringer_thickness * (stringer_height ** 2 / 4 + stringer_height * stringer_width) / \
                       (2 * Ixx_individual * 10 ** 6)   # Convert to MPa
        if np.all(shear_stress < balsa_sstrength):
            b = True


    return np.max(normal_stress_total), n_stringers_normal, np.max(shear_stress), n_stringers_shear

#   Example values

# internal_shear = np.append(np.arange(0, 50), np.arange(50, 0, -1))
# internal_bending = np.append(100 * np.ones(50), 50 * np.ones(50))
# internal_normal = np.append(50 * np.ones(50), 100 * np.ones(50))
fuselage_dimensions = {'width': 0.15, 'height': 0.15}
stringer_dimensions = {'width': 0.01, 'height': 0.01, 'thickness': 0.001}
material_properties = {'tensile strength': 7.501, 'compressive strength': 6.53, 'shear strength': 1.88}
loads = {'shear': np.append(np.arange(0, 50), np.arange(50, 0, -1)),
         'bending': np.append(100 * np.ones(50), 50 * np.ones(50)),
         'normal': np.append(50 * np.ones(50), 100 * np.ones(50))}


d = fuselage_layout(loads, fuselage_dimensions, stringer_dimensions, material_properties)



print(d)



