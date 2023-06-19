from constants import df
from Structures.get_loaddist import load_distribution
import numpy as np
#   Clean this code

class fuselage:
    def __init__(self, df):
        # create self attributes with the lines of code below
        self.length = df['l_fus']  # Length of the fuselage in meters
        self.width = df['w_fus']  # Width of the fuselage in meters
        self.height = df['h_fmax']  # Height of the fuselage in meters
        self.skin_vthickness = None
        self.skin_hthickness = None
        self.mass = df['m_fus']  # Fuselage mass in kg
        self.wingbox_location = df['wingbox_loc']    # Distance of the wingbox edge from the fuselage nose in meters
        self.root_chord = df['c_r']  # Root chord of the wing in meters
        self.stringer_width = None  # Width of the stringers in meters
        self.stringer_height = None  # Height of the stringers in meters
        self.stringer_thickness = None  # Thickness of the stringers in meters
        self.dist = load_distribution(df)
        self.array = self.dist.get_array()
        self.wing_lift = sum(self.dist.get_loaddist()[:, 1])
        self.wing_drag = sum(self.dist.get_loaddist()[:, 2])
        self.stringer_mat_tens = None  # Tensile strength of stringer material in MPa
        self.stringer_mat_comp = None  # Compressive strength of stringer material in MPa
        self.stringer_mat_shear = None  # Shear strength of stringer material in MPa
        self.stringer_mat_density = None  # Density of stringer material in kg/m^3
        self.skin_mat_tens = None  # Tensile strength of skin material in MPa
        self.skin_mat_comp = None  # Compressive strength of skin material in MPa
        self.skin_mat_shear = None  # Shear strength of skin material in MPa
        self.skin_mat_density = None  # Density of skin material in kg/m^3
        self.max_load_factor = df['n_max']  # Maximum load factor
        self.fuselage_drag_coefficient = None
        self.fuselage_lift_coefficient = None
        self.parachute_drag_coefficient = df['Cd_para']
        self.parachute_diameter = df['D_para']
        self.cruise_velocity = df['V_cruise']
        self.energy_catapult = df['energy_catapult']    # Energy of the catapult in kJ
        self.track_length = df['track_length']
        self.shear_distribution = None
        self.moment_distribution = None
        self.normal_load_distribution = None
        self.wingbox_normal_distribution = None
        self.boom_area = None
        self.result = None
        self.type = None
        self.Kt = None

    def fuselage_internal_loads(self):
        #   Simplify arrays to make sure that they match the output arrays size
        # Possible improvements: Include bending contribution due to wing drag and thrust
        g = 9.80665  # [m/s^2] gravitational acceleration
        n_max = self.max_load_factor  # Maximum load factor
        cube_drag_coefficient = 0.8  # Drag coefficient of the cube https://www.engineeringtoolbox.com/drag-coefficient-d_627.html
        parachute_drag_coefficient = self.parachute_drag_coefficient  # Drag coefficient of the parachute
        parachute_diameter = self.parachute_diameter  # [m] Diameter of the parachute
        cruise_velocity = self.cruise_velocity  # [m/s] Cruise velocity
        rho = 1.225  # [kg/m^3] air density at sea level

        launcher_energy = 1000 * self.energy_catapult  # [J] Launcher energy
        track_length = self.track_length  # [m] Track length

        fuselage_length = self.length  # [m] Fuselage length
        wingbox_location = self.wingbox_location
        root_chord = self.root_chord
        fuselage_mass = self.mass  # [kg] Fuselage mass
        fuselage_drag_coefficient = self.fuselage_drag_coefficient  # [-] Fuselage drag coefficient


        if self.fuselage_drag_coefficient is None:
            fuselage_drag_coefficient = cube_drag_coefficient


        fuselage_lift_coefficient = self.fuselage_lift_coefficient

        if self.fuselage_lift_coefficient is None:
            fuselage_lift_coefficient = 0


        wing_start_location = fuselage_length - wingbox_location - (root_chord / 2)
        wing_end_location = wing_start_location + root_chord

        wing_lift = self.wing_lift
        wing_drag = self.wing_drag

        wing_tail_weight = wing_lift - fuselage_mass * g

        #   For distributions, there is an increment per millimeter of fuselage length
        n_increments = int(fuselage_length * 1000)
        n_wing_start = int(wing_start_location * 1000)
        n_wing_end = int(wing_end_location * 1000)
        n_root_chord = int(root_chord * 1000)
        n_wbox = int(wingbox_location * 1000)

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
        parachute_deployment_drag = parachute_drag_coefficient * 0.5 * rho * cruise_velocity ** 2 * (
                    parachute_diameter / 2) ** 2 * np.pi

        #   Assume that the cushion force is evenly distributed over the length of the fuselage
        cushion_lift_distribution = - n_max * fuselage_mass * g / fuselage_length
        cushion_lift_distribution = cushion_lift_distribution * np.ones(n_increments)

        #   Assume that the launch force acts as a point load at the center of the fuselage, in the longitudinal direction
        launch_force = - launcher_energy / track_length

        #   Assume that the fuselage drag is that of a cube for conceptual design
        fuselage_drag = fuselage_drag_coefficient * 0.5 * rho * cruise_velocity ** 2 * self.width * self.height
        fuselage_drag_distribution = fuselage_drag * np.ones(n_increments)

        fuselage_lift = fuselage_lift_coefficient * 0.5 * rho * cruise_velocity ** 2 * fuselage_length
        fuselage_lift_distribution = - (fuselage_lift / fuselage_length) * np.ones(n_increments)

        wing_drag_distribution = np.append(np.zeros(n_wing_start), wing_drag * np.ones(n_increments - n_wing_start))

        propeller_thrust = - fuselage_drag + wing_drag

        wing_lift_distribution = - wing_lift / root_chord
        wing_lift_distribution = np.concatenate((np.zeros(n_wing_start),
                                                 wing_lift_distribution * np.ones(n_wing_end - n_wing_start),
                                                 np.zeros(n_increments - n_wing_end)))

        wing_tail_distribution = wing_tail_weight / root_chord
        wing_tail_distribution = np.concatenate((np.zeros(n_wing_start),
                                                 wing_tail_distribution * np.ones(n_wing_end - n_wing_start),
                                                 np.zeros(n_increments - n_wing_end)))

        weight_distribution = fuselage_mass * g / fuselage_length
        weight_distribution = weight_distribution * np.ones(n_increments)

        #   Initialise output arrays
        self.shear_distribution = np.zeros(n_increments)
        self.moment_distribution = np.zeros(n_increments)
        self.normal_load_distribution = np.zeros(n_increments)
        self.wingbox_normal_distribution = n_max * wing_lift_distribution[n_wbox]

        #   Cruise load analysis
        cruise_shear_distribution_slope = - add_arrays(add_arrays(add_arrays(weight_distribution,
                                                                             fuselage_lift_distribution),
                                                                  wing_lift_distribution), wing_tail_distribution)
        cruise_shear_distribution = np.cumsum(cruise_shear_distribution_slope * 0.001)

        cruise_moment_distribution = np.cumsum(cruise_shear_distribution * 0.001)

        cruise_normal_load_distribution = - (fuselage_drag_distribution + wing_drag_distribution)

        if self.type == 'cruise':
            self.shear_distribution = cruise_shear_distribution

            self.moment_distribution = cruise_moment_distribution

            self.normal_load_distribution = cruise_normal_load_distribution

        elif self.type == 'launch':
            #   Launch load analysis
            self.shear_distribution = cruise_shear_distribution

            self.moment_distribution = cruise_moment_distribution

            self.normal_load_distribution = np.append(launch_force * np.ones(n_increments // 2),
                                                 -launch_force * np.ones(n_increments // 2))

        elif self.type == 'deployment':
            #   Parachute deployment load analysis
            self.shear_distribution = cruise_shear_distribution

            self.moment_distribution = cruise_moment_distribution

            self.normal_load_distribution = np.append(parachute_deployment_drag * np.ones(n_increments // 2),
                                                 -parachute_deployment_drag * np.ones(n_increments // 2))

        elif self.type == 'landing':
            #   Cushion load analysis
            shear_distribution_slope = - add_arrays(add_arrays(weight_distribution, wing_tail_distribution),
                                                    cushion_lift_distribution)
            self.shear_distribution = np.cumsum(shear_distribution_slope * 0.001)

            self.moment_distribution = np.cumsum(self.shear_distribution * 0.001)

            self.normal_load_distribution = np.zeros(n_increments)

        elif self.type == 'max':
            #   Maximum load analysis
            shear_distribution_slope = n_max * cruise_shear_distribution_slope
            self.shear_distribution = np.cumsum(shear_distribution_slope * 0.001)

            self.moment_distribution = np.cumsum(self.shear_distribution * 0.001)

            self.normal_load_distribution = - n_max * add_arrays(fuselage_drag_distribution, wing_drag_distribution)

        return self.shear_distribution, self.moment_distribution, self.normal_load_distribution, self.wingbox_normal_distribution

    def primary_stress_check(self):
        fuselage_height = self.height

        bending = np.max(self.moment_distribution)
        normal = np.max(self.normal_load_distribution)

        tensile_strength = self.stringer_mat_tens
        compressive_strength = self.stringer_mat_comp

        # Apply Kt factor to normal stress
        normal_stress_1 = self.Kt * (bending / (2 * self.boom_area * fuselage_height) + normal / (4 * self.boom_area)) / 10 ** 6  # In MPa
        normal_stress_2 = self.Kt * (- bending / (2 * self.boom_area * fuselage_height) + normal / (4 * self.boom_area)) / 10 ** 6  # In MPa
        compressive_stress = min(normal_stress_1, normal_stress_2)
        tensile_stress = max(normal_stress_1, normal_stress_2)

        self.result = False

        if tensile_stress < 0:
            tensile_stress = 0

        if abs(compressive_stress) < compressive_strength and tensile_stress < tensile_strength:
            self.result = True

        return self.result

    def boom_reduction(self):
        fuselage_width = self.width
        fuselage_height = self.height
        skin_vthickness = self.skin_vthickness
        skin_hthickness = self.skin_hthickness

        Bv = skin_vthickness * fuselage_height / 6
        Bh = skin_hthickness * fuselage_width / 2

        self.boom_area = self.boom_area - Bv - Bh

        return self.boom_area

    def secondary_stress_check(self):
        fuselage_length = self.length
        fuselage_width = self.width
        fuselage_height = self.height
        skin_vthickness = self.skin_vthickness
        skin_hthickness = self.skin_hthickness
        wing_xlocation = self.wingbox_location
        root_chord = self.root_chord
        wing_start_location = fuselage_length - wing_xlocation - (root_chord / 2)
        wing_end_location = wing_start_location + root_chord

        n_increments = int(fuselage_length * 1000)
        n_wing_start = int(wing_start_location * 1000)
        n_wing_end = int(wing_end_location * 1000)
        n_root_chord = int(root_chord * 1000)

        bending = np.max(self.moment_distribution)
        normal = np.max(self.normal_load_distribution)
        shear = np.max(self.shear_distribution)

        stringer_tensile_strength = self.stringer_mat_tens
        stringer_compressive_strength = self.stringer_mat_comp
        stringer_shear_strength = self.stringer_mat_shear

        skin_tensile_strength = self.skin_mat_tens
        skin_compressive_strength = self.skin_mat_comp
        skin_shear_strength = self.skin_mat_shear


        #   Ignore contribution of skin to normal stress, could possibly evaluate stress at multiple points later
        Ixx_boom = self.boom_area * (fuselage_height / 2) ** 2
        Ixx_hskin = skin_hthickness * fuselage_width * (fuselage_height / 2) ** 2
        Ixx_hskin = 0
        Ixx_vskin = skin_vthickness * fuselage_height ** 3 / 12
        Ixx_vskin = 0
        Ixx = 4 * Ixx_boom + 2 * Ixx_hskin + 2 * Ixx_vskin

        #   Apply Kt factor to normal stress
        normal_stress_1 = self.Kt * (bending * (fuselage_height / 2) / Ixx + normal / (4 * self.boom_area)) / 10 ** 6  # In MPa
        normal_stress_2 = self.Kt * (- bending * (fuselage_height / 2) / Ixx + normal / (4 * self.boom_area)) / 10 ** 6  # In MPa
        shear_stress_v = shear / (2 * skin_vthickness) / 10 ** 6  # In MPa
        compressive_stress = min(normal_stress_1, normal_stress_2)
        tensile_stress = max(normal_stress_1, normal_stress_2)

        #   Mohr's circle
        #   Analyse the stress state of the wingbox skin,
        #   where there is a combination of y-direction normal stress and shear stress
        #   Sample the stress state at the middle of the wingbox
        n_wbox = [n_wing_start + n_root_chord // 2]
        bending = self.moment_distribution[n_wbox]
        normal = self.normal_load_distribution[n_wbox]
        shear = self.shear_distribution[n_wbox]
        wingbox_normal = self.wingbox_normal_distribution

        #   Assume that the skin takes 5% of the total normal stress (only for this analysis)
        mohr_normal_x = 0.05 * (bending / (2 * self.boom_area * fuselage_height) +
                                normal / (4 * self.boom_area)) / 10 ** 6  # In MPa
        mohr_normal_y = 0.05 * wingbox_normal / (2 * skin_vthickness) / 10 ** 6  # In MPa
        mohr_shear = shear / (2 * skin_vthickness) / 10 ** 6  # In MPa
        #   Assume that the normal stress acts only in the horizontal direction

        normal_stress_avg = (mohr_normal_x + mohr_normal_y) / 2
        R = np.sqrt(normal_stress_avg ** 2 + mohr_shear ** 2)
        normal_stress_max = max(normal_stress_avg + R, normal_stress_avg - R)
        normal_stress_min = min(normal_stress_avg - R, normal_stress_avg + R)
        shear_stress_max = R

        result = False

        if tensile_stress < 0:
            tensile_stress = 0

        if normal_stress_max < 0:
            normal_stress_max = 0

        if normal_stress_min > 0:
            normal_stress_min = 0

        #   If in the next iteration of the design ribs are applied, the Mohr's circle method must be revised,
        #   as most of the load will be carried by the ribs
        if abs(compressive_stress) < stringer_compressive_strength and tensile_stress < stringer_tensile_strength and \
                shear_stress_v < skin_shear_strength and normal_stress_max < skin_compressive_strength and \
                abs(normal_stress_min) < skin_tensile_strength and shear_stress_max < skin_shear_strength:
            result = True

        return result

    def stiffener_sizing(self):
        #   Use stiffeners at the corners of the fuselage, L-shaped, with equal width and height
        radius = np.sqrt(self.boom_area / np.pi)
        self.stringer_height = 4 * radius
        self.stringer_width = 4 * radius
        self.stringer_thickness = self.boom_area / (self.stringer_height + self.stringer_width)

        return self.stringer_height, self.stringer_width, self.stringer_thickness

fus = fuselage(df)

fus.skin_mat_comp = 80 * 10**6
fus.skin_mat_tens = 80 * 10**6
fus.skin_mat_shear = 60 * 10**6
fus.skin_mat_density = 900

fus.stringer_mat_comp = 345 * 10**6
fus.stringer_mat_tens = 345 * 10**6
fus.stringer_mat_shear = 207 * 10**6
fus.stringer_mat_density = 2800

fus.Kt = 2

dimensions = {'launch': {'vertical skin thickness': None, 'horizontal skin thickness': None, 'skin mass': None,
                        'stringer height': None, 'stringer width': None, 'stringer thickness': None,
                       'stringer mass': None, 'total mass': float('inf')}, 'landing': {'vertical skin thickness': None, 'horizontal skin thickness': None, 'skin mass': None,
                        'stringer height': None, 'stringer width': None, 'stringer thickness': None,
                       'stringer mass': None, 'total mass': float('inf')}, 'deployment': {'vertical skin thickness': None, 'horizontal skin thickness': None, 'skin mass': None,
                        'stringer height': None, 'stringer width': None, 'stringer thickness': None,
                       'stringer mass': None, 'total mass': float('inf')}, 'max': {'vertical skin thickness': None, 'horizontal skin thickness': None, 'skin mass': None,
                        'stringer height': None, 'stringer width': None, 'stringer thickness': None,
                       'stringer mass': None, 'total mass': float('inf')}}



# Loop through different stringer numbers and dimensions
# Still need to account for different materials and include Mohr's circle

for i in ['launch', 'landing', 'deployment', 'max']:
    fus.type = i
    fus.shear_distribution, fus.moment_distribution, fus.normal_load_distribution, \
        fus.wingbox_normal_distribution = fus.fuselage_internal_loads()
    for b in np.arange(0.00001, 0.0001, 0.00001):
        fus.boom_area = b
        if fus.primary_stress_check() is True:
            for c in np.arange(0.0001, 0.001, 0.0001):
                fus.skin_vthickness = c
                for d in np.arange(0.0001, 0.001, 0.0001):
                    fus.skin_hthickness = d
                    fus.boom_area = fus.boom_reduction()
                    if fus.secondary_stress_check() is True and fus.boom_area > 0:
                        h, w, t = fus.stiffener_sizing()
                        mskin = 2 * fus.skin_mat_density * fus.length * (c * fus.height + d * fus.width)
                        mbooms = 4 * fus.stringer_mat_density * fus.length * (h * t + w * t)
                        m = mskin + mbooms
                        if m < dimensions[i]['total mass']:
                            dimensions[i]['vertical skin thickness'] = c
                            dimensions[i]['horizontal skin thickness'] = d
                            dimensions[i]['skin mass'] = mskin
                            dimensions[i]['stringer mass'] = mbooms
                            dimensions[i]['stringer height'] = h
                            dimensions[i]['stringer width'] = w
                            dimensions[i]['stringer thickness'] = t
                            dimensions[i]['total mass'] = m
    print('step done')


print(dimensions['launch']['total mass'], dimensions['landing']['total mass'], dimensions['deployment']['total mass'],
      dimensions['max']['total mass'])
