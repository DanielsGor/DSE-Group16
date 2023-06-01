import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

#functions --------------------------------------------------------------------
#calculate C_L_w_alpha
def calculate_C_L_w_alpha(A, lamda, C_l_alpha):
    E = 1 + 2 * lamda / (A * (1 + lamda))
    C_L_w_alpha = 0.995 * C_l_alpha / (E + C_l_alpha/(np.pi * A))    
    return C_L_w_alpha

#calculate C_L_Ah_alpha
def calculate_C_L_Ah_alpha(C_L_w_alpha, lamda, b, b_fus, c_r, S):
    S_net = S - c_r * b_fus * (1 + lamda/b)/2
    K_i = (1 + 2.15 * b_fus/ b) * S_net/S + np.pi/2 * 1/ C_L_w_alpha * b_fus**2/S
    C_L_Ah_alpha = C_L_w_alpha * K_i
    return C_L_Ah_alpha

#calculate C_L_h_alpha
def calculate_C_L_h_alpha(A_h, lamda_h, C_l_h_alpha):
    E = 1 + 2 * lamda_h / (A_h * (1 + lamda_h))
    C_L_h_alpha = 0.995 * C_l_h_alpha / (E + C_l_h_alpha/(np.pi * A_h))
    return C_L_h_alpha

#constants & inputs -----------------------------------------------------------
#environmental constants
rho = 1.225 # [kg/m^3] air density
g = 9.80665 # [m/s^2] gravitational acceleration
T = 288.15 # [K] temperature

#aircraft constants
m = 7.68 # [kg] aircraft mass
W = m * g # [N] aircraft weight

#cg definitions
x_bar_cg_range = np.linspace(-0.5, 1, 1000) #just for plotting
x_bar_ac = 0.25 # [-] aerodynamic center position aircraft, normalised by mac  #to be adapted once we have the data
x_cg_max_bar = 0.35 # [-] cg max, normalised by mac
x_cg_min_bar = 0.15 # [-] cg min, normalised by mac
delta_x_cg_bar = x_cg_max_bar - x_cg_min_bar # [-] cg range, normalised by mac

#maneuvrability
r = 50 # [m] turn radius
ROC = 5 # [m/s] rate of climb #guessed out of thin air
deltah = 80 # [m] change in altitude for climb
climb_angle = np.arctan(deltah/(np.pi * r)) # [rad] climb angle
v_climb = ROC /np.sin(climb_angle) # [m/s] climb speed

#wing constants
S = 1.1# [m^2] wing surface area
b = 2.95# [m] wing span
b_fus = 0.15 # [m] fuselage width #update asap!
C_l_alpha = 6.161 # [-] lift curve slope airfoil wing
A = b**2 / S # [-] aspect ratio wing
lamda = 0.45 # [-] taper ratio wing
c_r = 0.49078 # [m] root chord wing
mac = 0.37288 # [m] mean aerodynamic chord wing

#horizontal tail constants
A_h = 5 # [-] aspect ratio horizontal tail
lamda_h =  0.8 # [-] taper ratio horizontal tail
C_l_alpha_h = 0.1 * 180/np.pi # [-] lift curve slope horizontal tail airfoil / based on NACA 0012
VhV2 = 1.0 # [-] ratio of horizontal tail velocity to aircraft velocity

#C_L calculations
C_L_h_alpha = calculate_C_L_h_alpha(A_h, lamda_h, C_l_alpha_h)
C_L_w_alpha = calculate_C_L_w_alpha(A, lamda, C_l_alpha)
C_L_Ah_alpha = calculate_C_L_Ah_alpha(C_L_w_alpha, lamda, b, b_fus, c_r, S)
C_L_h = -0.35 * A_h**(1/3) # Lift coefficient of the horizontal tail
C_L_Ah = 2 * W / (rho * v_climb**2 * S) # Lift coefficient of the main wing
C_m_ac = -0.16 # [-]
deda = 0.0 #depends on the tail configuration # formula E-52 in Torenbeek, r and m in fig E-13

# Stability line ----------------------------------------------------------------
SM = 0.1 #stability margin

a = 1 /  (C_L_h_alpha / C_L_Ah_alpha * (1 - deda) * VhV2)
b = - x_bar_ac * a

htail_volume_stability = (x_bar_cg_range - x_bar_ac) / (C_L_h_alpha / C_L_Ah_alpha * (1 - deda) * VhV2)
htail_volume_stability_SM = (x_bar_cg_range - x_bar_ac + SM) / (C_L_h_alpha / C_L_Ah_alpha * (1 - deda) * VhV2)

# Control line ------------------------------------------------------------------
a =1 / (C_L_h / C_L_Ah * VhV2)
b = (C_m_ac / C_L_Ah - x_bar_ac) / (C_L_h / C_L_Ah * VhV2)

htail_volume_control = a * x_bar_cg_range + b

def inverted_htail_volume_control(htail_volume_control):
    return (htail_volume_control - b) / a
#htail_volume_control = 1 / (C_L_h / C_L_Ah * VhV2) * x_bar_cg_range + (C_m_ac / C_L_Ah - x_bar_ac) / (C_L_h / C_L_Ah * VhV2)

p = htail_volume_control - htail_volume_stability_SM
m = np.min(p[p>delta_x_cg_bar])
print(m, p)
idx = int(np.where(p == m)[0][0])
#print('The minimum distance between the stability and control line is: ', m, ' at x_bar_cg = ', x_bar_cg_range[idx])
print(idx)

# Create the figure and axes
fig, ax = plt.subplots()

# Plot the X plot
ax.plot(x_bar_cg_range, htail_volume_stability, label='Stability line')
ax.plot(x_bar_cg_range, htail_volume_stability_SM, label='Stability line with SM')
ax.plot(x_bar_cg_range, htail_volume_control, label='Control line')

# Set the initial height of the horizontal line
initial_height = 0.5

# Get the x-coordinate of the control line
x_control = inverted_htail_volume_control(initial_height)

# Define the x-coordinates for the horizontal line
x_line = [x_control, x_control + delta_x_cg_bar]

# Define the y-coordinates for the horizontal line
y_line = [initial_height, initial_height]

# Plot the horizontal line
line, = ax.plot(x_line, y_line, color='r')


# Create a slider axes
slider_ax = fig.add_axes([0.15, 0.05, 0.7, 0.03])

# Create the slider
slider = Slider(slider_ax, 'Height', 0, 1, valinit=initial_height)

# Define a function to update the horizontal line position
def update_line(value):
    # Calculate the x-coordinate of the control line based on the new y-coordinate value
    x_control = inverted_htail_volume_control(value)

    # Update the data of the horizontal line
    line.set_data([x_control, x_control + delta_x_cg_bar], [value, value])

    fig.canvas.draw_idle()

# Define a function to handle the button click event
def button_callback(event):
    # Save the value of the slider as a variable
    saved_value = slider.val
    print(f"Saved Value: {saved_value}")


# Create a button axes
button_ax = fig.add_axes([0.85, 0.05, 0.1, 0.03])

# Create the button
button = Button(button_ax, 'Save')

# Register the button click event handler
button.on_clicked(button_callback)
# Register the update function with the slider
slider.on_changed(update_line)

plt.title('Horizontal tail sizing - Scissor plot')
plt.xlabel('x_cg_bar')
plt.ylabel('Volume_h')
plt.grid()
plt.show()



'''
#plotting ----------------------------------------------------------------------
plt.plot(x_bar_cg_range, htail_volume_stability, label = 'Stability line')
plt.plot(x_bar_cg_range, htail_volume_stability_SM, label = 'Stability line with SM')
plt.plot(x_bar_cg_range, htail_volume_control, label = 'Control line')
plt.hlines(y=htail_volume_control[idx], xmin= x_bar_cg_range[idx], xmax = x_bar_cg_range[idx] + delta_x_cg_bar, label = 'x_cg range')
plt.title('Horizontal tail sizing - Scissor plot')
plt.xlabel('x_cg_bar')
plt.ylabel('Volume_h')
plt.grid()
plt.legend()
plt.show()
'''