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
        self.mat_tens = None  # Tensile strength of balsasud ultralite in MPa
        self.mat_comp = None  # Compressive strength of balsasud ultralite in MPa
        self.mat_shear = None  # Shear strength of balsasud ultralite in MPa
        self.mat_density = None  # Density of balsasud ultralite in kg/m^3
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
        self.type = 'max'





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
        fuselage_drag = fuselage_drag_coefficient * 0.5 * rho * cruise_velocity ** 2 * fuselage_length
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

            self.moment_distribution = np.cumsum(shear_distribution * 0.001)

            self.normal_load_distribution = np.zeros(n_increments)

        elif self.type == 'max':
            #   Maximum load analysis
            shear_distribution_slope = n_max * cruise_shear_distribution_slope
            self.shear_distribution = np.cumsum(shear_distribution_slope * 0.001)

            self.moment_distribution = np.cumsum(shear_distribution * 0.001)

            self.normal_load_distribution = - n_max * add_arrays(fuselage_drag_distribution, wing_drag_distribution)

        return self.shear_distribution, self.moment_distribution, self.normal_load_distribution, self.wingbox_normal_distribution

    def primary_stress_check(self):
        fuselage_height = self.height

        bending = np.max(self.moment_distribution)
        normal = np.max(self.normal_load_distribution)

        tensile_strength = self.mat_tens
        compressive_strength = self.mat_comp

        normal_stress_1 = (bending / (2 * self.boom_area * fuselage_height) + normal / (4 * self.boom_area)) / 10 ** 6  # In MPa
        normal_stress_2 = (- bending / (2 * self.boom_area * fuselage_height) + normal / (4 * self.boom_area)) / 10 ** 6  # In MPa
        compressive_stress = min(normal_stress_1, normal_stress_2)
        tensile_stress = max(normal_stress_1, normal_stress_2)

        self.result = False

        if compressive_stress < compressive_strength and tensile_stress < tensile_strength:
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

        tensile_strength = self.mat_tens
        compressive_strength = self.mat_comp
        shear_strength = self.mat_shear

        normal_stress_1 = (bending / (2 * self.boom_area * fuselage_height) + normal / (4 * self.boom_area)) / 10 ** 6  # In MPa
        normal_stress_2 = (- bending / (2 * self.boom_area * fuselage_height) + normal / (4 * self.boom_area)) / 10 ** 6  # In MPa
        shear_stress_v = shear / (2 * skin_vthickness) / 10 ** 6  # In MPa
        compressive_stress = min(normal_stress_1, normal_stress_2)
        tensile_stress = max(normal_stress_1, normal_stress_2)

        #   Mohr's circle
        #   Analyse the stress state in the wingbox,
        #   where there is a combination of y-direction normal stress and shear stress
        #   Sample the stress state at the middle of the wingbox
        n_wbox = [n_wing_start + n_root_chord // 2]
        bending = self.moment_distribution[n_wbox]
        normal = self.normal_load_distribution[n_wbox]
        shear = self.shear_distribution[n_wbox]
        wingbox_normal = self.wingbox_normal_distribution[n_wbox]

        mohr_normal_x = (bending / (2 * self.boom_area * fuselage_height) + normal / (4 * self.boom_area)) / 10 ** 6  # In MPa
        mohr_normal_y = wingbox_normal / (2 * skin_vthickness) / 10 ** 6  # In MPa
        mohr_shear = shear / (2 * skin_vthickness) / 10 ** 6  # In MPa
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

    def stiffener_sizing(self):
        #   Use stiffeners at the corners of the fuselage, L-shaped, with equal width and height
        radius = np.sqrt(self.boom_area / np.pi)
        self.stringer_height = 4 * radius
        self.stringer_width = 4 * radius
        self.stringer_thickness = self.boom_area / (self.stringer_height * self.stringer_width)

        return self.stringer_height, self.stringer_width, self.stringer_thickness

fus = fuselage(df)
fus.shear_distribution, fus.moment_distribution, fus.normal_load_distribution, fus.wingbox_normal_distribution  = fus.fuselage_internal_loads()
fus.mat_comp = 345 * 10**6
fus.mat_tens = 345 * 10**6
fus.mat_shear = 207 * 10**6
fus.mat_density = 2800

stringer_dimensions = {'height': None, 'width': None, 'thickness': None, 'mass': float('inf')}

# Loop through different stringer numbers and dimensions
# Still need to account for different materials and include Mohr's circle
for b in np.arange(10**-6, 10**-4, 10**-6):
    fus.boom_area = b
    if fus.primary_stress_check() is True:
        for c in np.arange(0.001, 0.010, 0.001):
            fus.skin_vthickness = c
            for d in np.arange(0.001, 0.010, 0.001):
                fus.skin_hthickness = d
                fus.boom_area = fus.boom_reduction()
                if fus.secondary_stress_check() is True:
                    h, w, t = fus.stiffener_sizing()
                    m = 4 * fus.mat_density * fus.length * (h * w + 2 * h * t + 2 * w * t)
                    if m < stringer_dimensions['mass']:
                        stringer_dimensions['height'] = h
                        stringer_dimensions['width'] = w
                        stringer_dimensions['thickness'] = t
                        stringer_dimensions['mass'] = m



