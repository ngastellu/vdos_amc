#!/usr/bin/env python 

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from qcnico.vdos import norm_int
from qcnico.plt_utils import setup_tex


datfile1 = Path("~/Desktop/simulation_outputs/vdos/tempdot6/size_dependence/sample-64/vdos_full_structure_1angstrom_pin.npy").expanduser()
datfile1 = Path("~/Desktop/simulation_outputs/vdos/graphene/vdos_qcnico_mpi-110000-1100000-20.npy").expanduser()
freqs1, vdos1 = np.load(datfile1)


datfile2 = Path("~/Desktop/simulation_outputs/vdos/tempdot6/size_dependence/sample-64/vdos_full_structure_4angstrom_pin.npy").expanduser()
freqs2, vdos2 = np.load(datfile2)

window_size = 50
avg_filter = np.ones(window_size) / window_size
vdos_wavg1 = np.convolve(vdos1, avg_filter, mode='same')
vdos_wavg2 = np.convolve(vdos2, avg_filter, mode='same')

vdos_wavg1 = norm_int(vdos_wavg1, freqs1)
vdos_wavg2 = norm_int(vdos_wavg2, freqs2)

# assert np.all(freqs1 == freqs2)

print(np.max(freqs1))
print(np.max(freqs2))

setup_tex(fontsize=35)


plt.plot(freqs1, vdos_wavg1, 'r-', lw=0.8, alpha=1, label='graphene')#, label='1\AA\tpin')
# plt.plot(freqs2, vdos_wavg2, 'b-', lw=0.8, alpha=0.5, label='4\AA\tpin')
plt.xlabel('Frequency $\omega$ [THz]')
plt.ylabel('VDOS (normalised)')
# plt.xlim([-1,50])
# plt.plot(freqs1, vdos1, 'r-', lw=0.8, alpha=0.5, label='short')
# plt.plot(freqs2, vdos2, 'b-', lw=0.8, alpha=0.5, label='long')
plt.legend()
plt.show()
