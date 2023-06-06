import numpy as np
# from constants import df
#   Clean this code

# class fuselage:
#     def __init__(self):
#         # create self attributes with the lines of code below
#         self.length = df['fus_l']  # Length of the fuselage in meters
#         self.width = df['fus_w']  # Width of the fuselage in meters
#         self.height = df['fus_h']  # Height of the fuselage in meters
#         self.skin_thickness = df['t_skin']  # Thickness of the fuselage skin in meters
#         self.stringer_pitch = df['str_pitch']  # Spacing between stringers in meters
#         self.stringer_width = df['str_w']  # Width of the stringers in meters
#         self.stringer_height = df['str_h']  # Height of the stringers in meters
#         self.stringer_thickness = df['str_t']  # Thickness of the stringers in meters
#         self.balsa_tens = df['balsa_tens']  # Tensile strength of balsasud ultralite in MPa
#         self.balsa_comp = df['balsa_comp']  # Compressive strength of balsasud ultralite in MPa
#         self.internal_shear = None
#         self.internal_bending = None
#         self.pitch_list = None
#         self.normal_stress = None
#         self.p = None


def fuselage_internal_loads(external_loads, fuselage_dimensions):
    # Possible improvements: Include bending contribution due to wing drag and thrust
    g = 9.80665 # [m/s^2] gravitational acceleration
    n_max = 3.75 # Maximum load factor
    cube_drag_coefficient = 0.8 # Drag coefficient of the cube https://www.engineeringtoolbox.com/drag-coefficient-d_627.html
    parachute_drag_coefficient = 2.116328266 # Drag coefficient of the parachute
    parachute_diameter = 2.1336 # [m] Diameter of the parachute
    cruise_velocity = 15.1 # [m/s] Cruise velocity
    rho = 1.225 # [kg/m^3] air density at sea level

    launcher_energy = 1000 # [J] Launcher energy
    track_length = 2.4 # [m] Track length

    fuselage_length = fuselage_dimensions['length'] # [m] Fuselage length
    fuselage_width = fuselage_dimensions['width']
    fuselage_height = fuselage_dimensions['height']
    wing_xlocation = fuselage_dimensions['wing_xlocation']
    root_chord = fuselage_dimensions['root_chord']
    wing_start_location = fuselage_length - wing_xlocation - (root_chord / 2)
    wing_end_location = wing_start_location + root_chord

    wing_lift = external_loads['wing_lift']
    wing_drag = external_loads['wing_drag']
    wing_moment = external_loads['wing_moment']

    fuselage_mass = external_loads['fuselage_mass']

    wing_tail_weight = wing_lift - fuselage_mass * g

    #   For distributions, there is an increment per millimeter of fuselage length
    n_increments = fuselage_length * 1000

    #   Assume the critical parachute deployment load is applied longitudinally at the center of the fuselage
    parachute_drag = parachute_drag_coefficient * 0.5 * rho * cruise_velocity**2 * (parachute_diameter / 2)**2 * np.pi


    #   Assume that the cushion force is evenly distributed over the length of the fuselage
    cushion_lift_distribution = - n_max * fuselage_mass * g / fuselage_length
    cushion_lift_distribution = np.full_like(np.arange(0, n_increments), cushion_lift_distribution)

    #   Assume that the launch force acts as a point load at the center of the fuselage, in the longitudinal direction
    launch_force = - launcher_energy / track_length


    #   Assume that the fuselage drag is that of a cube for conceptual design
    fuselage_drag = cube_drag_coefficient * 0.5 * rho * cruise_velocity**2 * \
                    fuselage_width * fuselage_height
    fuselage_drag_distribution = np.full_like(np.arange(0, n_increments), fuselage_drag)

    wing_drag_distribution = np.append(np.zeros(n_increments * wing_start_location // fuselage_length),
        np.full_like(np.arange(0, n_increments * (fuselage_length - wing_start_location) // fuselage_length), wing_drag))

    propeller_thrust = - fuselage_drag + wing_drag

    lift_distribution = - wing_lift / root_chord
    lift_distribution = np.append(np.zeros(n_increments * wing_start_location // fuselage_length),
                                  np.full_like(np.arange(0, n_increments * root_chord // fuselage_length), lift_distribution))

    wing_tail_distribution = wing_tail_weight / root_chord
    wing_tail_distribution = np.append(np.zeros(n_increments * wing_start_location // fuselage_length),
        np.full_like(np.arange(0, n_increments * root_chord // fuselage_length), wing_tail_distribution))

    weight_distribution = fuselage_mass * g / fuselage_length
    weight_distribution = np.full_like(np.arange(0, n_increments), weight_distribution)


    #   Cruise load analysis
    shear_distribution_slope = - weight_distribution + lift_distribution + wing_tail_distribution
    shear_distribution = np.cumsum(shear_distribution_slope * 0.001)

    moment_distribution_slope = np.cumsum(shear_distribution * 0.001)

    normal_load_distribution = - (fuselage_drag_distribution + wing_drag_distribution)

    #   Launch load analysis



def fuselage_layout(internal_loads, fuselage_dimensions, stringer_dimensions, material_properties):
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

    internal_shear = internal_loads['shear']
    internal_bending = internal_loads['bending']
    internal_normal = internal_loads['normal']
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
fuselage_dimensions = {'width': 0.15, 'height': 0.15, 'length': 0.7}
stringer_dimensions = {'width': 0.01, 'height': 0.01, 'thickness': 0.001}
material_properties = {'tensile strength': 7.501, 'compressive strength': 6.53, 'shear strength': 1.88}
loads = {'shear': np.append(np.arange(0, 50), np.arange(50, 0, -1)),
         'bending': np.append(100 * np.ones(50), 50 * np.ones(50)),
         'normal': np.append(50 * np.ones(50), 100 * np.ones(50))}


d = fuselage_layout(loads, fuselage_dimensions, stringer_dimensions, material_properties)



print(d)



