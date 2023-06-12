import numpy as np
import matplotlib.pyplot as plt
import constants as df


def fuselage_internal_loads(external_loads, fuselage_dimensions, type):
    #   Simplify arrays to make sure that they match the output arrays size
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
    fuselage_mass = fuselage_dimensions['mass']
    fuselage_drag_coefficient = fuselage_dimensions['drag_coefficient']
    fuselage_lift_coefficient = fuselage_dimensions['lift_coefficient']
    wing_start_location = fuselage_length - wing_xlocation - (root_chord / 2)
    wing_end_location = wing_start_location + root_chord

    wing_lift = external_loads['wing_lift']
    wing_drag = external_loads['wing_drag']

    wing_tail_weight = wing_lift - fuselage_mass * g

    #   For distributions, there is an increment per millimeter of fuselage length
    n_increments = int(fuselage_length * 1000)
    n_wing_start = int(wing_start_location * 1000)
    n_wing_end = int(wing_end_location * 1000)
    n_root_chord = int(root_chord * 1000)
    n_wbox = [n_wing_start + n_root_chord // 2]

    #   Create a function to add arrays of different size, so the output arrays have a consistent size
    def add_arrays(array1, array2):
        if len(array1) < len(array2):
            array3 = array2.copy()
            array3[:len(array1)] += array1
        else:
            array3 = array1.copy()
            array3[:len(array2)] += array2
        return array3

    #   Assume the critical parachute deployment load is applied longitudinally at the center of the fuselage
    parachute_deployment_drag = parachute_drag_coefficient * 0.5 * rho * cruise_velocity**2 * (parachute_diameter / 2)**2 * np.pi


    #   Assume that the cushion force is evenly distributed over the length of the fuselage
    cushion_lift_distribution = - n_max * fuselage_mass * g / fuselage_length
    cushion_lift_distribution = cushion_lift_distribution * np.ones(n_increments)

    #   Assume that the launch force acts as a point load at the center of the fuselage, in the longitudinal direction
    launch_force = - launcher_energy / track_length

    #   Assume that the fuselage drag is that of a cube for conceptual design
    fuselage_drag = fuselage_drag_coefficient * 0.5 * rho * cruise_velocity**2 * fuselage_length
    fuselage_drag_distribution = fuselage_drag * np.ones(n_increments)

    fuselage_lift = fuselage_lift_coefficient * 0.5 * rho * cruise_velocity**2 * fuselage_length
    fuselage_lift_distribution = - (fuselage_lift / fuselage_length) * np.ones(n_increments)

    wing_drag_distribution = np.append(np.zeros(n_wing_start), wing_drag * np.ones(n_increments - n_wing_start))

    propeller_thrust = - fuselage_drag + wing_drag

    wing_lift_distribution = - wing_lift / root_chord
    wing_lift_distribution = np.concatenate((np.zeros(n_wing_start),
                                  wing_lift_distribution * np.ones(n_wing_end - n_wing_start), np.zeros(n_increments - n_wing_end)))


    wing_tail_distribution = wing_tail_weight / root_chord
    wing_tail_distribution = np.concatenate((np.zeros(n_wing_start),
                                  wing_tail_distribution * np.ones(n_wing_end - n_wing_start), np.zeros(n_increments - n_wing_end)))

    weight_distribution = fuselage_mass * g / fuselage_length
    weight_distribution = weight_distribution * np.ones(n_increments)

    #   Initialise output arrays
    shear_distribution = np.zeros(n_increments)
    moment_distribution = np.zeros(n_increments)
    normal_load_distribution = np.zeros(n_increments)
    wingbox_normal_distribution = n_max * wing_lift_distribution[n_wbox]

    #   Cruise load analysis
    cruise_shear_distribution_slope = - add_arrays(add_arrays(add_arrays(weight_distribution,
                                                              fuselage_lift_distribution),
                                                                         wing_lift_distribution), wing_tail_distribution)
    cruise_shear_distribution = np.cumsum(cruise_shear_distribution_slope * 0.001)

    cruise_moment_distribution = np.cumsum(cruise_shear_distribution * 0.001)

    cruise_normal_load_distribution = - (fuselage_drag_distribution + wing_drag_distribution)

    if type == 'cruise':
        shear_distribution = cruise_shear_distribution

        moment_distribution = cruise_moment_distribution

        normal_load_distribution = cruise_normal_load_distribution

    elif type == 'launch':
        #   Launch load analysis
        shear_distribution = cruise_shear_distribution

        moment_distribution = cruise_moment_distribution

        normal_load_distribution = np.append(launch_force * np.ones(n_increments // 2),
                                                    -launch_force * np.ones(n_increments // 2))

    elif type == 'deployment':
        #   Parachute deployment load analysis
        shear_distribution = cruise_shear_distribution

        moment_distribution = cruise_moment_distribution

        normal_load_distribution = np.append(parachute_deployment_drag * np.ones(n_increments // 2),
                                                       -parachute_deployment_drag * np.ones(n_increments // 2))

    elif type == 'landing':
        #   Cushion load analysis
        shear_distribution_slope = - add_arrays(add_arrays(weight_distribution, wing_tail_distribution), cushion_lift_distribution)
        shear_distribution = np.cumsum(shear_distribution_slope * 0.001)

        moment_distribution = np.cumsum(shear_distribution * 0.001)

        normal_load_distribution = np.zeros(n_increments)

    elif type == 'max':
        #   Maximum load analysis
        shear_distribution_slope = n_max * cruise_shear_distribution_slope
        shear_distribution = np.cumsum(shear_distribution_slope * 0.001)

        moment_distribution = np.cumsum(shear_distribution * 0.001)

        normal_load_distribution = - n_max * add_arrays(fuselage_drag_distribution, wing_drag_distribution)

    return shear_distribution, moment_distribution, normal_load_distribution, wingbox_normal_distribution


def primary_stress_check(boom_area, fuselage_dimensions, internal_loads, material_properties):
    fuselage_width = fuselage_dimensions['width']
    fuselage_height = fuselage_dimensions['height']

    bending = np.max(internal_loads['bending'])
    normal = np.max(internal_loads['normal'])

    tensile_strength = material_properties['tensile strength']
    compressive_strength = material_properties['compressive strength']
    shear_strength = material_properties['shear strength']

    normal_stress_1 = (bending / (2 * boom_area * fuselage_height) + normal / (4 * boom_area)) / 10 ** 6 # In MPa
    normal_stress_2 = (- bending / (2 * boom_area * fuselage_height) + normal / (4 * boom_area)) / 10 ** 6 # In MPa
    compressive_stress = min(normal_stress_1, normal_stress_2)
    tensile_stress = max(normal_stress_1, normal_stress_2)

    result = False

    if compressive_stress < compressive_strength and tensile_stress < tensile_strength:
        result = True

    return result

def boom_reduction(initial_boom_area, fuselage_dimensions):
    fuselage_width = fuselage_dimensions['width']
    fuselage_height = fuselage_dimensions['height']
    fuselage_vthickness = fuselage_dimensions['vertical thickness']
    fuselage_hthickness = fuselage_dimensions['horizontal thickness']

    Bv = fuselage_vthickness * fuselage_height / 6
    Bh = fuselage_hthickness * fuselage_width / 2

    boom_area = initial_boom_area - Bv - Bh

    return boom_area

def secondary_stress_check(boom_area, fuselage_dimensions, internal_loads, material_properties):
    fuselage_length = fuselage_dimensions['length']
    fuselage_width = fuselage_dimensions['width']
    fuselage_height = fuselage_dimensions['height']
    fuselage_vthickness = fuselage_dimensions['vertical thickness']
    wing_xlocation = fuselage_dimensions['wing_xlocation']
    root_chord = fuselage_dimensions['root_chord']
    wing_start_location = fuselage_length - wing_xlocation - (root_chord / 2)
    wing_end_location = wing_start_location + root_chord

    n_increments = int(fuselage_length * 1000)
    n_wing_start = int(wing_start_location * 1000)
    n_wing_end = int(wing_end_location * 1000)
    n_root_chord = int(root_chord * 1000)

    bending = np.max(internal_loads['bending'])
    normal = np.max(internal_loads['normal'])
    shear = np.max(internal_loads['shear'])

    tensile_strength = material_properties['tensile strength']
    compressive_strength = material_properties['compressive strength']
    shear_strength = material_properties['shear strength']

    normal_stress_1 = (bending / (2 * boom_area * fuselage_height) + normal / (4 * boom_area)) / 10 ** 6  # In MPa
    normal_stress_2 = (- bending / (2 * boom_area * fuselage_height) + normal / (4 * boom_area)) / 10 ** 6  # In MPa
    shear_stress_v = shear / (2 * fuselage_vthickness) / 10 ** 6 # In MPa
    compressive_stress = min(normal_stress_1, normal_stress_2)
    tensile_stress = max(normal_stress_1, normal_stress_2)

    #   Mohr's circle
    #   Analyse the stress state in the wingbox,
    #   where there is a combination of y-direction normal stress and shear stress
    #   Sample the stress state at the middle of the wingbox
    n_wbox = [n_wing_start + n_root_chord // 2]
    bending = internal_loads['bending'][n_wbox]
    normal = internal_loads['normal'][n_wbox]
    shear = internal_loads['shear'][n_wbox]
    wingbox_normal = internal_loads['wingbox normal'][n_wbox]

    mohr_normal_x = (bending / (2 * boom_area * fuselage_height) + normal / (4 * boom_area)) / 10 ** 6  # In MPa
    mohr_normal_y = wingbox_normal / (2 * fuselage_vthickness) / 10 ** 6  # In MPa
    mohr_shear = shear / (2 * fuselage_vthickness) / 10 ** 6 # In MPa
    #   Assume that the normal stress acts only in the horizontal direction

    normal_stress_avg = (mohr_normal_x + mohr_normal_y) / 2
    R = np.sqrt(normal_stress_avg ** 2 + shear_stress_v ** 2)
    normal_stress_max = normal_stress_avg + R
    normal_stress_min = normal_stress_avg - R
    shear_stress_max = R

    result = False

    if compressive_stress < compressive_strength and tensile_stress < tensile_strength and \
            shear_stress_v < shear_strength:
        result = True

    return result

def stiffener_sizing(boom_area):
    #   Use stiffeners at the corners of the fuselage, L-shaped, with equal width and height
    radius = np.sqrt(boom_area / np.pi)
    height = 4 * radius
    width = 4 * radius
    thickness = boom_area / (height * width)

    return height, width, thickness



#   Example values

# internal_shear = np.append(np.arange(0, 50), np.arange(50, 0, -1))
# internal_bending = np.append(100 * np.ones(50), 50 * np.ones(50))
# internal_normal = np.append(50 * np.ones(50), 100 * np.ones(50))
fuselage_dimensions = {'width': 0.15, 'height': 0.15, 'length': 0.7, 'wing_xlocation': 0.4,
                       'root_chord': 0.49078, 'mass': 7, 'drag_coefficient': 0.01, 'lift_coefficient': 0.1}
external_loads = {'wing_lift': 700, 'wing_drag': 100, 'wing_moment': 100}
stringer_dimensions = {'width': 0.01, 'height': 0.01, 'thickness': 0.001}
material_properties = {'tensile strength': 7.501, 'compressive strength': 6.53, 'shear strength': 1.88}

shear, moment, normal, vertical = fuselage_internal_loads(external_loads, fuselage_dimensions, 'max')
loads = {'shear': shear,
         'bending': moment,
         'normal': normal,
         'wingbox normal': vertical}

normal_stress, n_stringers_normal, shear_stress, n_stringers_shear = \
    fuselage_layout(loads, fuselage_dimensions, stringer_dimensions, material_properties)

print(normal_stress, n_stringers_normal, shear_stress, n_stringers_shear)

dist = load_distribution(df)
wing_lift_distr = dist.get_loaddist()[:, 1]
wing_lift = np.sum(wing_lift_distr)
wing_drag_distr = dist.get_loaddist()[:, 2]
wing_drag = np.sum(wing_drag_distr)



# def fuselage_layout(internal_loads, fuselage_dimensions, stringer_dimensions, material_properties):
#     #   Fuselage dimensions: width, height  (in m)
#     #   Stringer dimensions: width, height, thickness   (in m)
#     #   Material properties: tensile yield strength, compressive yield strength, shear yield strength (in MPa)
#     #   https://www.matweb.com/search/DataSheet.aspx?MatGUID=cde2cfd21dc446c69fb7e4c3a39880ed
#
#     fuselage_width = fuselage_dimensions['width']
#     fuselage_height = fuselage_dimensions['height']
#
#     stringer_width = stringer_dimensions['width']
#     stringer_height = stringer_dimensions['height']
#     stringer_thickness = stringer_dimensions['thickness']
#
#     balsa_tstrength = material_properties['tensile strength']
#     balsa_cstrength = material_properties['compressive strength']
#     balsa_sstrength = material_properties['shear strength']
#
#     internal_shear = internal_loads['shear']
#     internal_bending = internal_loads['bending']
#     internal_normal = internal_loads['normal']
#     size = np.size(internal_shear)
#
#     #   Bending and normal load analysis
#     #   Neglect the contribution of the skin
#     #   Neglect fuselage drag
#     #   Parallel axis theorem is the dominant contributor to the moment of inertia
#
#     stringer_area = 2 * stringer_width * stringer_thickness + stringer_height * stringer_thickness \
#                     - 2 * stringer_thickness ** 2
#     normal_stress_total = np.zeros(size)    # In Mpa
#     a = False
#     n_stringers_normal = 0   # Number of stringers
#     while a == False and n_stringers_normal * stringer_width < fuselage_width:
#         n_stringers_normal = n_stringers_normal + 1
#         Ixx_individual = stringer_area * (fuselage_height / 2) ** 2
#         Ixx = Ixx_individual * n_stringers_normal
#         normal_stress_bending = internal_bending * fuselage_height / (Ixx * 2 * 10 ** 6)    # Converted to MPa
#         normal_stress = internal_normal / (n_stringers_normal * stringer_area * 10 ** 6)
#         normal_stress_total = normal_stress + normal_stress_bending
#         if np.all(normal_stress_total < balsa_tstrength) and np.all(normal_stress_total < balsa_cstrength):
#             a = True
#
#     #   Shear load analysis
#     #   Shear forces distributed equally between stringers
#     shear_stress = np.zeros(size)    # In Mpa
#     b = False
#     n_stringers_shear = 0
#     while b == False and n_stringers_shear * stringer_width < fuselage_width:
#         n_stringers_shear = n_stringers_shear + 1
#         Vy = internal_shear / n_stringers_shear
#         Ixx_individual = stringer_thickness * stringer_height ** 3 / 12 +\
#                          stringer_thickness * stringer_width * stringer_height ** 2 / 2
#         #   For a c stringer loaded in the y direction, maximum shear stress is in the middle vertical plate
#         shear_stress = Vy * stringer_thickness * (stringer_height ** 2 / 4 + stringer_height * stringer_width) / \
#                        (2 * Ixx_individual * 10 ** 6)   # Convert to MPa
#         if np.all(shear_stress < balsa_sstrength):
#             b = True
#
#
#     return np.max(normal_stress_total), n_stringers_normal, np.max(shear_stress), n_stringers_shear