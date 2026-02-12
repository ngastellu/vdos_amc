#!/usr/bin/env python 

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


datfile = Path("~/Desktop/simulation_outputs/vdos/graphene/vdos_qcnico_mpi-410000-4400000-20.npy").expanduser()
# datfile = Path("~/Desktop/simulation_outputs/vdos/graphene/vdos_qcnico_mpi_new.npy").expanduser()
# datfile = Path("~/Desktop/simulation_outputs/vdos/tempdot6/sample-1/vdos_qcnico_mpi-1.npy").expanduser()
freqs, vdos = np.load(datfile)

window_size = 100
avg_filter = np.ones(window_size) / window_size
vdos_wavg = np.convolve(vdos, avg_filter, mode='same')

plt.plot(freqs, vdos_wavg, 'r-', lw=0.8)
plt.xlabel('Frequency [THz]')
plt.ylabel('VDOS')
plt.show()
