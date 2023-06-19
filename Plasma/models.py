import numpy as np

cls = np.asarray([0.0028,0.0029,0.0024,0.0018,0.0013,0.0026])
print(np.max(np.abs(cls/np.average(cls)))-1)
