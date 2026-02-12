#!/usr/bin/env python 

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


datfile = Path("~/Desktop/simulation_outputs/vdos/tempdot6/size_dependence/sample-64/vdos_full_structure.npy").expanduser()
data = np.load(datfile)

plt.plot(*data, 'r-', lw=0.8)
plt.xlabel('Frequency [THz]')
plt.ylabel('VDOS')
plt.show()
