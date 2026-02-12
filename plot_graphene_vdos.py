#!/usr/bin/env python

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qcnico.plt_utils import setup_tex


def plot_vdos(ax, c, div_by_freqs=False): 
    setup_tex(fontsize=25)
    #vdos_npy = Path(f'/Users/nico/Desktop/simulation_outputs/vdos/graphene/vdos_qcnico_mpi-110000-1100000-20.npy')
    vdos_npy = Path(f'/Users/nico/Desktop/simulation_outputs/vdos/graphene/vdos-graphene_OBC_pinned.npy')
 
    freqs, vdos_tot = np.load(vdos_npy)


    #vdos_tot
    if div_by_freqs == True:
            vdos_tot = vdos_tot[100:]/freqs[100:] # remove first elems to avoid small freq values blowing
            freqs = freqs[100:]
    setup_tex(fontsize=30)
    ax.plot(freqs, vdos_tot, c=c, lw=0.8)
    return ax

    

div_by_freqs = False
clr = 'r'

setup_tex(fontsize=25)
fig, ax = plt.subplots()

ax = plot_vdos(ax, clr, div_by_freqs=div_by_freqs)

if div_by_freqs == True:
    ylabel = '$g(\omega)/\omega$'
else:
    ylabel = '$g(\omega)$' 

ax.set_ylabel(ylabel)

ax.set_xlabel('$\omega$ [THz]')

plt.show()