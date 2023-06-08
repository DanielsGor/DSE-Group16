import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

test_setup = pd.DataFrame({
    'A': ['c', 'v', 'c', 'c'],
    'f_act': ['c', 'c', 'v', 'c'],
    'f_car': ['c', 'c', 'c', 'v']
})

def generate_combinations(fixed_values, ranges):
    # Convert fixed values to iterables
    fixed_iterables = {key: [value] for key, value in fixed_values.items()}

    # Combine fixed values with ranges
    values = {**fixed_iterables, **ranges}

    # Generate all combinations
    combinations = list(itertools.product(*values.values()))
    combinations = pd.DataFrame(combinations, columns=values.keys())

    return combinations



"""
Test 1: vary alpha to get Cl-alpha, Cd-alpha, Cm-alpha plots for plasma on/off

We get the values for Cl-alpha for both plasma on/off cases and the get the delta Cl-alpha plots. From this we determine the optimal alpha for the plasma actuation.
This alpha value we then use to do the remaining experiments.
"""
alpha_range = np.arange(0, 16, 1)
V_range = [15]

# Sample values for test 1
A = 4.5
f_actuator = 120
f_carrier = 1000

fixed_values = {
        'A': A,
        'f_actuator': f_actuator,
        'f_carrier': f_carrier
    }

ranges = {
        'alpha': alpha_range,
        'V': V_range,
        
    }

df_test_1 =generate_combinations(fixed_values, ranges)
print('test')


"""
Test 2: Vary A, f_actuator and f_carrier and find the one with the most influence. The other two we then keep constant. We need to find a method to determine which constant value
this has to be.
"""

A_range = [3, 4.5, 6]
f_actuator_range = [10, 120, 230]
f_carrier_range = [500, 1000, 1500]



def block_0():
    """
    Block 0: Keep A, f_actuator, f_carrier constant while varying alpha and V
    """

    fixed_values = {
        'A': 4.5,
        'f_actuator': 120,
        'f_carrier': 1000
    }

    ranges = {
        'alpha': alpha_range,
        'V': V_range,
        
    }

    combinations = generate_combinations(fixed_values, ranges)
    return combinations


def block_1():
    """
    Block 0: Keep A, f_actuator, f_carrier constant while varying alpha and V
    """

    fixed_values = {
        'f_actuator': 120,
        'f_carrier': 1000
    }

    ranges = {
        'alpha': alpha_range,
        'V': V_range,
        'A': A_range,
        
    }

    combinations = generate_combinations(fixed_values, ranges)
    return combinations



block_1 = block_1()
print(block_1)


