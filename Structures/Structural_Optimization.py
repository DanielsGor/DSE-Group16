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
        self.wingbox_location = df['wingbox_loc']    # Distance of the wingbox edge from the fuselage nose in meters
        self.root_chord = df['c_r']  # Root chord of the wing in meters
        self.stringer_width = df['str_w']  # Width of the stringers in meters
        self.stringer_height = df['str_h']  # Height of the stringers in meters
        self.stringer_thickness = df['str_t']  # Thickness of the stringers in meters
        self.mat_tens = df['balsa_tens']  # Tensile strength of balsasud ultralite in MPa
        self.mat_comp = df['balsa_comp']  # Compressive strength of balsasud ultralite in MPa
        self.mat_shear = None  # Shear strength of balsasud ultralite in MPa
        self.dist = load_distribution(df)
        self.wing_lift = sum(self.dist.get_loaddist()[:, 1])
        self.wing_drag = sum(self.dist.get_loaddist()[:, 2])
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
        self.fuselage_vthickness = None
        self.fuselage_hthickness = None



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
        fuselage_drag_coefficient = cube_drag_coefficient  # [-] Fuselage drag coefficient

        if self.fuselage_drag_coefficient is not None:
            fuselage_drag_coefficient = self.fuselage_drag_coefficient

        fuselage_lift_coefficient = 0

        if self.fuselage_lift_coefficient is not None:
            fuselage_lift_coefficient = self.fuselage_lift_coefficient


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
            shear_distribution_slope = - add_arrays(add_arrays(weight_distribution, wing_tail_distribution),
                                                    cushion_lift_distribution)
            shear_distribution = np.cumsum(shear_distribution_slope * 0.001)

            moment_distribution = np.cumsum(shear_distribution * 0.001)

            normal_load_distribution = np.zeros(n_increments)

        elif type == 'max':
            #   Maximum load analysis
            shear_distribution_slope = n_max * cruise_shear_distribution_slope
            shear_distribution = np.cumsum(shear_distribution_slope * 0.001)

            moment_distribution = np.cumsum(shear_distribution * 0.001)

            normal_load_distribution = - n_max * add_arrays(fuselage_drag_distribution, wing_drag_distribution)

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

        result = False

        if compressive_stress < compressive_strength and tensile_stress < tensile_strength:
            result = True

        return self.result

    def boom_reduction(self):
        fuselage_width = self.width
        fuselage_height = self.height
        fuselage_vthickness = self.fuselage_vthickness
        fuselage_hthickness = self.fuselage_hthickness

        Bv = fuselage_vthickness * fuselage_height / 6
        Bh = fuselage_hthickness * fuselage_width / 2

        self.boom_area = self.boom_area - Bv - Bh

        return self.boom_area

    def secondary_stress_check(self):
        fuselage_length = self.length
        fuselage_width = self.width
        fuselage_height = self.height
        fuselage_vthickness = self.fuselage_vthickness
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
        shear_stress_v = shear / (2 * fuselage_vthickness) / 10 ** 6  # In MPa
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
        mohr_normal_y = wingbox_normal / (2 * fuselage_vthickness) / 10 ** 6  # In MPa
        mohr_shear = shear / (2 * fuselage_vthickness) / 10 ** 6  # In MPa
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
        self.stringer_thickness = self.boom_area / (height * width)

        return self.stringer_height, self.stringer_width, self.stringer_thickness

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




