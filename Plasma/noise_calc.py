import numpy as np

def dB2W(noise_dB):
    return np.power(10, (noise_dB-120)/1)

def W2dB(noise_W):
    return 10*np.log10(noise_W) + 120

if __name__ == "__main__":
    noise_requirement = 30  #dB
    d = 120                 #m
    d_ref = 0.2128          #m

    noise_req_power = dB2W(noise_requirement)
    noise_source_power = noise_requirement*(d/d_ref)**2
    noise_source = W2dB(noise_source_power)
    print(noise_source)

