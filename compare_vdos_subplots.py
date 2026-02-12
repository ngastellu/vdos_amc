#!/usr/bin/env python 

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from qcnico.vdos import norm_int
from qcnico.plt_utils import setup_tex



# datfile1 = Path("~/Desktop/simulation_outputs/vdos/graphene/vdos_qcnico_mpi_new.npy").expanduser()
# datfile1 = Path("~/Desktop/simulation_outputs/vdos/graphene/vdos_qcnico_mpi-110000-1100000-20.npy").expanduser()
datfile1 = Path("~/Desktop/simulation_outputs/vdos/tempdot6/subsample_center/sample-0/vdos_qcnico_mpi-0.npy").expanduser()
freqs1, vdos1 = np.load(datfile1)

# datfile2 = Path("~/Desktop/simulation_outputs/vdos/tempdot6/sample-100/vdos_qcnico_mpi-100.npy").expanduser()
# datfile2 = Path("~/Desktop/simulation_outputs/vdos/graphene/vdos_qcnico_mpi-410000-4400000-20.npy").expanduser()
# datfile2 = Path("~/Desktop/simulation_outputs/vdos/tempdot6/subsample_center/sample-0/vdos_qcnico_mpi_short-0.npy").expanduser()
datfile2 = Path("~/Desktop/simulation_outputs/vdos/graphene/airebo_results/vdos_qcnico_mpi_new.npy").expanduser()
freqs2, vdos2 = np.load(datfile2)

window_size = 100
avg_filter = np.ones(window_size) / window_size
vdos_wavg1 = np.convolve(vdos1, avg_filter, mode='same')
vdos_wavg2 = np.convolve(vdos2, avg_filter, mode='same')

vdos_wavg1 = norm_int(vdos_wavg1[100:]/freqs1[100:], freqs1[100:])
vdos_wavg2 = norm_int(vdos_wavg2[100:]/freqs2[100:], freqs2[100:])

# vdos_wavg1 = norm_int(vdos_wavg1[100:], freqs1[100:])
# vdos_wavg2 = norm_int(vdos_wavg2[100:], freqs2[100:])

# assert np.all(freqs1 == freqs2)

print(np.max(freqs1))
print(np.max(freqs2))

setup_tex(fontsize=35)

fig, ax  = plt.subplots(2,1,sharex=True, sharey=True)


ax[0].plot(freqs1[100:], vdos_wavg1, 'r-', lw=1.0, label='amorphous')
ax[1].plot(freqs2[100:], vdos_wavg2, 'r-', lw=1.0, label='crystalline')
ax[1].set_xlabel('Frequency $\omega$ [THz]')
# ax[0].set_ylabel('VDOS (normalised)')
# ax[1].set_ylabel('VDOS (normalised)')
# plt.plot(freqs1, vdos1, 'r-', lw=0.8, alpha=0.5, label='short')
# plt.plot(freqs2, vdos2, 'b-', lw=0.8, alpha=0.5, label='long')
for a in ax:
    a.legend()
fig.text(0.02, 0.5, '$g(\omega)/\omega$', va='center', rotation='vertical')
plt.show()
