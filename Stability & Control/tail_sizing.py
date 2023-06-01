import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from vertical_tail_sizing import main_vtail
from Horizontal_tail_sizing_final import main_htail
from constants import S, b, MAC

vtail_volume = main_vtail()
htail_volume = main_htail()

print(f"Vertical tail volume: {vtail_volume}")
print(f"Horizontal tail volume: {htail_volume}")

# Initial values
slope = 1
intercept = 0

l_h = np.linspace(0.5, 2, 1000)
l_v = np.zeros_like(l_h)
S_h = np.zeros_like(l_h)
S_v = np.zeros_like(l_h)

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
plt.subplots_adjust(left=0.15, bottom=0.25)  # Adjust the plot area

line_h, = ax1.plot(l_h, S_h, 'b-', label='S_h')
line_v, = ax2.plot(l_v, S_v, 'r-', label='S_v')

ax1.set_xlabel('l_h [m]')
ax1.set_ylabel('S_h', color='b')
ax1.tick_params('y', colors='b')

ax2.set_ylabel('S_v', color='r')
ax2.tick_params('y', colors='r')

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Slider positions
slider_slope_ax = plt.axes([0.15, 0.1, 0.65, 0.03])
slider_intercept_ax = plt.axes([0.15, 0.05, 0.65, 0.03])

# Sliders
slider_slope = Slider(slider_slope_ax, 'slope', 0, 2, valinit=slope)
slider_intercept = Slider(slider_intercept_ax, 'intercept', 0, 1, valinit=intercept)


def update_plot(val):
    # Get the updated values from the sliders
    slope = slider_slope.val
    intercept = slider_intercept.val

    # Update the data
    l_v = slope * l_h + intercept
    S_h = htail_volume * S * MAC / l_h
    S_v = vtail_volume * S * b / l_v

    # Update the plot lines
    line_h.set_ydata(S_h)
    line_v.set_xdata(l_h)  # Maybe change this to l_v SHOULD BE REVISED
    line_v.set_ydata(S_v)

    # Redraw the plot
    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()
    fig.canvas.draw_idle()


# Register the update function with the sliders
slider_slope.on_changed(update_plot)
slider_intercept.on_changed(update_plot)

plt.show()

