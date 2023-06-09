import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from constants import S, S_fs, b, l_fus, l_cg, h_fmax, h_f1, h_f2, b_f1, b_f2, B_p, l_p, D_p


#functions --------------------------------------------------------------------
# calculation of Cn_beta
def calculate_Cn_beta(S, S_fs, b, l_fus, l_cg, h_fmax, h_f1, h_f2, b_f1, b_f2, B_p, l_p, D_p):
    k_beta =  0.3 * (l_cg / l_fus) + 0.75 * (h_fmax / l_fus) - 0.105
    Cn_beta_f  = -k_beta * (S_fs * l_fus) / (S *b) * (h_f1 / h_f2)**0.5 * (b_f1 / b_f2)**(1/3)
    Cn_beta_p = -0.053 * B_p * (l_p * D_p) / S * b
    Cn_beta_di = -0.017 # [-] high wing configuration
    Cn_beta = Cn_beta_f + Cn_beta_p + Cn_beta_di
    return Cn_beta

#calculation of the tail volume
def calculate_vtail_volume(Cn_beta):
    tail_volume = 55.238 * Cn_beta**2 + 8.724 * Cn_beta + 0.4
    range = np.linspace(-0.01, -0.1, 1000)
    plt.plot(range, 55.238 * range**2 + 8.724 * range + 0.4)
    plt.vlines(Cn_beta, 0, 0.5, colors='r', linestyles='dashed')
    plt.show()
    return tail_volume

def main_vtail():

    '''
    Main function
    '''

    Cn_beta = calculate_Cn_beta(S, S_fs, b, l_fus, l_cg, h_fmax, h_f1, h_f2, b_f1, b_f2, B_p, l_p, D_p)
    vertical_tail_volume = calculate_vtail_volume(Cn_beta)
    print(vertical_tail_volume)

    return vertical_tail_volume
if __name__ == '__main__':
    main_vtail()