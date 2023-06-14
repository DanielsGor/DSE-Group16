import pandas as pd
from get_loaddist import load_distribution
import numpy as np
import matplotlib.pyplot as plt

# class intload(load_distribution):
#     def __init__(self, load_dist):
#         self.l = load_dist.load_dist[:, 0]
#         self.load = None
#         self.intload = None
#     def get_intload(self, loadcase):
#         self.load = self.load[loadcase]
#         self.intload = np.zeros((len(self.l), 2))
#         self.intload[:, 0] = self.l
#         for n in range(len(self.l)):
#             for i in range(n+1):
#                 self.intload[n, 1] += self.load[i] * (self.l[i] - self.l[n])
#         return self.intload
#     def plot_intload(self):
#         plt.plot(self.intload[:, 0], self.intload[:, 1])
#         plt.show()
#
# il = intload()
# il.get_intload(1)
