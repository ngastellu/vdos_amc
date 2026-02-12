#!/usr/bin/env python

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


datadir = Path('~/Desktop/simulation_outputs/vdos/tempdot6/size_dependence/sample-64').expanduser()

for npy in datadir.iterdir():
    # If NPY corresponds to averge VDOS of subsampled structure, label it using the size of the subsamples
    if '-' in npy.stem:
        label = npy.stem.split('-')[1]
    else:
        label = 'full' # full structure VDOS
    freqs, vdos = np.load(npy)
    plt.plot(freqs, vdos, lw=0.8, label=label)

plt.xlabel('Frequency [THz]')
plt.ylabel('VDOS')
plt.legend()
plt.show()