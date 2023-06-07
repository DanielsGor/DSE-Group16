import numpy as np
import matplotlib.pyplot as plt
from constants import g, rho, T, V_cruise, m_tot, ROC, Cm_ac, b, S, A, MAC, lamda, c_r, c_t, C_l_alpha, b_fus, x_bar_ac
from matplotlib.widgets import Slider, Button


"""
This is a program to size the horizontal tail based on the approach described by Torenbeek's book called Synthesis of 
Subsonic Airplane Design. The program uses various inputs from mainly the aerodynamics department and gives an
interactive scissor plot in which the cg range can be varied and optimized visually. This results in a horizontal
tail volume which can be obtained by using the button in the plot.
"""

# r = 50                          # turn radius [m]
# ROC = 5                         # rate of climb [m/s]

####Tail####
delta_h = 80                    # change in altitude for climb [m]
A_h= 5                          # aspect ratio horizontal tail [-]
lamda_h = 1.0                   # taper ratio horizontal tail [-]
C_l_alpha_h = 0.1 * 180/np.pi   # lift curve slope horizontal tail [-]


####Stability####
SM = 0.10                       # stability margin [-]
x_cg_min_bar = 0.25             # minimum cg position [-]
x_cg_max_bar = 0.295             # maximum cg position [-]
delta_x_cg_bar = x_cg_max_bar - x_cg_min_bar # [-] cg range, normalised by mac
x_bar_cg_range = np.linspace(-0.5, 1, 1000)


####Airflow interactions####
VhV2 = 1                        # (V_h/V)^2 [-]
deda = 0                        # downwash gradient [-]

####Functions####

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

#The v_climb function has been replaced by the v_climb requirement
# def calculate_v_climb(r, ROC, delta_h):
#
#     '''
#     Calculates the climb speed based on r, ROC and delta_h
#     '''
#
#     climb_angle = np.arctan(delta_h / (np.pi * r))  # [rad] climb angle
#     v_climb = ROC / np.sin(climb_angle)  # [m/s] climb speed
#
#     return v_climb


def calculate_C_L_Ah(W, v_climb, S):

    '''
    Calculates the lift coefficient of the UAV without tail based on the weight, rho, v_climb and S
    '''

    C_L_Ah = 2 * W / (rho * v_climb**2 * S)

    return C_L_Ah


def calculate_stability_control(x_bar_ac, C_L_h_alpha, C_L_Ah_alpha, deda, VhV2, SM, C_L_h, C_L_Ah):

    '''
    Calculates the stability and control lines for the scissor plot. Stability is calculated with and without the
    stability margin.
    '''

    # Stability
    htail_volume_stability = (x_bar_cg_range - x_bar_ac) / (C_L_h_alpha / C_L_Ah_alpha * (1 - deda) * VhV2)
    htail_volume_stability_SM = (x_bar_cg_range - x_bar_ac + SM) / (C_L_h_alpha / C_L_Ah_alpha * (1 - deda) * VhV2)

    # Control
    slope = 1 / (C_L_h / C_L_Ah * VhV2)
    intercept = (Cm_ac / C_L_Ah - x_bar_ac) / (C_L_h / C_L_Ah * VhV2)

    htail_volume_control = slope * x_bar_cg_range + intercept

    return htail_volume_stability, htail_volume_stability_SM, htail_volume_control


def inverted_htail_volume_control(htail_volume_control, C_L_h, C_L_Ah, x_bar_ac):

    '''
    Calculates the x_bar_cg location of a given horizontal tail volume
    '''

    slope = 1 / (C_L_h / C_L_Ah * VhV2)
    intercept = (Cm_ac / C_L_Ah - x_bar_ac) / (C_L_h / C_L_Ah * VhV2)

    x_bar_cg = (htail_volume_control - intercept) / slope

    return x_bar_cg


def scissor_plot(x_bar_cg_range, htail_volume_stability, htail_volume_stability_SM, htail_volume_control, delta_x_cg_bar, C_L_h, C_L_Ah, x_bar_ac):

    def update_line(value):

        '''
        Update the location of the cg range line
        '''

        x_control = inverted_htail_volume_control(value, C_L_h, C_L_Ah, x_bar_ac)
        line.set_data([x_control, x_control + delta_x_cg_bar], [value, value])

        fig.canvas.draw_idle()

    # Define a function to handle the button click event
    def button_callback(event):

        '''
        Button to save the current value of the slider
        '''
        global horizontal_tail_volume
        horizontal_tail_volume = slider.val
        print(f"Saved Value: {horizontal_tail_volume}")


    # Create the plot
    fig, ax = plt.subplots()

    ax.plot(x_bar_cg_range, htail_volume_stability, label='Stability line', color='orange')
    ax.plot(x_bar_cg_range, htail_volume_stability_SM, label='Stability line with SM', color='black')
    ax.plot(x_bar_cg_range, htail_volume_control, label='Control line', color='black')

    initial_height = 0.5
    y_line = [initial_height, initial_height]

    x_control = inverted_htail_volume_control(initial_height, C_L_h, C_L_Ah, x_bar_ac)
    x_line = [x_control, x_control + delta_x_cg_bar]

    line, = ax.plot(x_line, y_line, color='green')

    slider_pos = [0.92, 0.1, 0.03, 0.8]  # [left, bottom, width, height]

    # Slider
    slider_ax = fig.add_axes(slider_pos, facecolor='lightgray')
    slider = Slider(slider_ax, 'Height', -1, 1.5, valinit=initial_height, orientation='vertical')

    # Button
    button_ax = fig.add_axes([0.85, 0.02, 0.1, 0.03])
    button = Button(button_ax, 'Save')

    # Initiate button and slider
    button.on_clicked(button_callback)
    slider.on_changed(update_line)

    ax.set_title('Horizontal tail sizing - Scissor plot', loc='center')
    ax.set_xlabel('CG location / MAC', labelpad=10)
    ax.set_ylabel('Horizontal tail volume', labelpad=10)
    ax.grid()

    plt.show()


def main_htail():

    '''
    Main function
    '''

    # v_climb = calculate_v_climb(r, ROC, delta_h)
    v_climb = 15.1
    C_L_h_alpha = calculate_C_L_h_alpha(A_h, lamda_h, C_l_alpha_h)
    C_L_w_alpha = calculate_C_L_w_alpha(A, lamda, C_l_alpha)
    C_L_Ah_alpha = calculate_C_L_Ah_alpha(C_L_w_alpha, lamda, b, b_fus, c_r, S)
    C_L_h = calculate_C_L_h(A_h)
    C_L_Ah = calculate_C_L_Ah(m_tot*g, v_climb, S)

    htail_volume_stability, htail_volume_stability_SM, htail_volume_control = calculate_stability_control(x_bar_ac, C_L_h_alpha, C_L_Ah_alpha, deda, VhV2, SM, C_L_h, C_L_Ah)
    scissor_plot(x_bar_cg_range, htail_volume_stability, htail_volume_stability_SM, htail_volume_control, delta_x_cg_bar, C_L_h, C_L_Ah, x_bar_ac)
    if 'horizontal_tail_volume' in globals():
        print('Final horizontal tail volume: ', horizontal_tail_volume)
        return horizontal_tail_volume
    else:
        print('No horizontal tail volume saved')
        return None

if __name__ == '__main__':
    main_htail()