import numpy as np

total_yaw = 180 #deg

V = 15.1 #m/s

R = 50 #m

t = R * np.deg2rad(total_yaw)/V  

yaw_rate = total_yaw/t
print(yaw_rate)