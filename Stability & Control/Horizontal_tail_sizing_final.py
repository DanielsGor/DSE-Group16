import numpy as np
import matplotlib.pyplot as plt
from constants import *
from matplotlib.widgets import Slider, Button

"""
This is a program to size the horizontal tail based on the approach described by Torenbeek's book called Synthesis of 
Subsonic Airplane Design. The program uses various inputs from mainly the aerodynamics department and gives an
interactive scissor plot in which the cg range can be varied and optimized visually. This results in a horizontal
tail volume which can be obtained by using the button in the plot.
"""

#%% Define Input Parameters
r = 50                          # turn radius [m]
ROC = 5                         # rate of climb [m/s]
delta_h = 80                    # change in altitude for climb [m]
A_h= 5                          # aspect ratio horizontal tail [-]
lamba_h = 0.8                   # taper ratio horizontal tail [-]
C_l_alpha_h = 0.1 * 180/np.pi   # lift curve slope horizontal tail [-]
SM = 0.10                       # stability margin [-]

#%% Assume several parameters
VhV2 = 1                        # (V_h/V)^2 [-]
deda = 0                        # downwash gradient [-]



#%% Functions used in the program

def calculate_C_L_w_alpha(A, lamda, C_l_alpha):
    '''
    Calculates the lift slope of the wing based on the lift slope of the airfoil and the geometry of the wing based
    on the approach described by Torenbeek.
    '''

    E = 1 + 2 * lamda / (A * (1 + lamda))  # [E-6]
    C_L_w_alpha = 0.995 * C_l_alpha / (E + C_l_alpha/(np.pi * A))  # [E-5]

    return C_L_w_alpha


def calculate_C_L_Ah_alpha(C_L_w_alpha, lamda, b, b_fus, c_r, S):

    '''
    Calculates the lift slope of the UAV without tail based on the lift slope of the wing and the wing
    geometry based on the approach described by Torenbeek.
    '''

    S_net = S - c_r * b_fus * (1 + lamda/b)/2  # [E-30 ish]
    K_i = (1 + 2.15 * b_fus/ b) * S_net/S + np.pi/2 * 1/ C_L_w_alpha * b_fus**2/S  # [E-33]
    C_L_Ah_alpha = C_L_w_alpha * K_i  # [E-30]

    return C_L_Ah_alpha


def calculate_C_L_h_alpha(A_h, lamda_h, C_l_h_alpha):

    '''
    Calculates the lift slope of the horizontal tail based on the lift slope of the horizontal tail airfoil and the tail
    geometry based on the approach described by Torenbeek.
    '''

    E = 1 + 2 * lamda_h / (A_h * (1 + lamda_h))
    C_L_h_alpha = 0.995 * C_l_h_alpha / (E + C_l_h_alpha/(np.pi * A_h))

    return C_L_h_alpha


def calculate_C_L_h(A_h):

    '''
    Calculates the lift coefficient of the horizontal tail based on initial tail geometry
    '''

    C_L_h = -0.35 * A_h ** (1 / 3)

    return C_L_h


def calculate_v_climb(r, ROC, delta_h):

    '''
    Calculates the climb speed based on r, ROC and delta_h
    '''

    climb_angle = np.arctan(delta_h / (np.pi * r))  # [rad] climb angle
    v_climb = ROC / np.sin(climb_angle)  # [m/s] climb speed

    return v_climb


def calculate_C_L_Ah(W, v_climb, S):

    '''
    Calculates the lift coefficient of the UAV without tail based on the weight, rho, v_climb and S
    '''

    C_L_Ah = 2 * W / (rho * v_climb**2 * S)

    return C_L_Ah


def calculate_stability_control(x_bar_ac, C_L_h_alpha, C_L_Ah_alpha, deda, VhV2, SM):

    '''
    Calculates the stability and control lines for the scissor plot. Stability is calculated with and without the
    stability margin.
    '''

    x_bar_cg_range = np.linspace(-0.5, 1, 1000)

    # Stability
    htail_volume_stability = (x_bar_cg_range - x_bar_ac) / (C_L_h_alpha / C_L_Ah_alpha * (1 - deda) * VhV2)
    htail_volume_stability_SM = (x_bar_cg_range - x_bar_ac + SM) / (C_L_h_alpha / C_L_Ah_alpha * (1 - deda) * VhV2)

    # Control
    slope = 1 / (C_L_h / C_L_Ah * VhV2)
    intercept = (C_m_ac / C_L_Ah - x_bar_ac) / (C_L_h / C_L_Ah * VhV2)

    htail_volume_control = slope * x_bar_cg_range + intercept

    return htail_volume_stability, htail_volume_stability_SM, htail_volume_control


def inverted_htail_volume_control(htail_volume_control):

    '''
    Calculates the x_bar_cg location of a given horizontal tail volume
    '''

    slope = 1 / (C_L_h / C_L_Ah * VhV2)
    intercept = (C_m_ac / C_L_Ah - x_bar_ac) / (C_L_h / C_L_Ah * VhV2)

    x_bar_cg = (htail_volume_control - intercept) / slope

    return x_bar_cg


def scissor_plot(x_bar_cg_range, htail_volume_stability, htail_volume_stability_SM, htail_volume_control, delta_x_cg_bar):

    def update_line(value):

        '''
        Update the location of the cg range line
        '''

        x_control = inverted_htail_volume_control(value)
        line.set_data([x_control, x_control + delta_x_cg_bar], [value, value])

        fig.canvas.draw_idle()

    # Define a function to handle the button click event
    def button_callback(event):

        '''
        Button to save the current value of the slider
        '''

        saved_value = slider.val
        print(f"Saved Value: {saved_value}")


    # Create the plot
    fig, ax = plt.subplots()

    ax.plot(x_bar_cg_range, htail_volume_stability, label='Stability line')
    ax.plot(x_bar_cg_range, htail_volume_stability_SM, label='Stability line with SM')
    ax.plot(x_bar_cg_range, htail_volume_control, label='Control line')

    initial_height = 0.5
    y_line = [initial_height, initial_height]

    x_control = inverted_htail_volume_control(initial_height)
    x_line = [x_control, x_control + delta_x_cg_bar]

    line, = ax.plot(x_line, y_line, color='r')

    # Slider
    slider_ax = fig.add_axes([0.15, 0.05, 0.7, 0.03])
    slider = Slider(slider_ax, 'Height', 0, 1, valinit=initial_height)

    # Button
    button_ax = fig.add_axes([0.85, 0.05, 0.1, 0.03])
    button = Button(button_ax, 'Save')

    # Initiate button and slider
    button.on_clicked(button_callback)
    slider.on_changed(update_line)

    plt.title('Horizontal tail sizing - Scissor plot')
    plt.xlabel('CG location / MAC')
    plt.ylabel('Horizontal tail volume')
    plt.grid()
    plt.legend()
    plt.show()


def main():

    '''
    Main function
    '''

    print(V_cruise)

if __name__ == '__main__':
    main()