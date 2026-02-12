#!/usr/bin/env python

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qcnico.plt_utils import setup_tex


def official_name(ensemble):
    if ensemble == '40x40':
        return 'hyperuniform'
        # return 'sAMC-500'
    elif ensemble == 'tempdot6':
        # return 'sAMC-q400'
        return 'hyperfluctuating'
    else:
        raise ValueError(f"Invalid ensemble {ensemble}!")


def plot_all_at_once(ensemble, ax, c, alpha=0.2, div_by_freqs=False): 

    vdos_dir = Path(f'/Users/nico/Desktop/simulation_outputs/vdos/{ensemble}/vdos_npys_80.0_avgd')
    vdos_npys = vdos_dir.glob('vdos*npy')
    for k, npy in enumerate(vdos_npys):
        freqs, vdos = np.load(npy)
        if div_by_freqs == True:
            vdos = vdos[2000:]/freqs[2000:] # remove first elems to avoid small freq values blowing
            freqs = freqs[2000:]
        
        setup_tex(fontsize=30)
        if k == 0:
            ax.plot(freqs, vdos, c=c, alpha=alpha, lw=0.7, label=official_name(ensemble))
        else:
            ax.plot(freqs, vdos, c=c, alpha=alpha, lw=0.7)
    return ax


def plot_average(ensemble, ax, c, div_by_freqs=False): 
    vdos_dir = Path(f'/Users/nico/Desktop/simulation_outputs/vdos/{ensemble}/vdos_npys_80.0_avgd')
    vdos_npys = list(vdos_dir.glob('vdos*npy'))

    natoms_arr = np.load(vdos_dir.parent / 'natoms.npy')
    natoms_dict = {natoms_arr[k,0]:natoms_arr[k,1] for k in range(natoms_arr.shape[0])}
    
    npy = vdos_npys[0]
    ii = int(npy.stem.split('-')[1])
    N = natoms_dict[ii]
    freqs, vdos_tot = np.load(npy)
    vdos_tot *= N

    Ntot = N

    for npy in vdos_npys[1:]:
        ii = int(npy.stem.split('-')[1])
        print(ii, end=' --> ')

        try:
            N = natoms_dict[ii]
            freqs, vdos = np.load(npy)
        except Exception as e:
            print(e)
            continue
        vdos_tot += vdos * N
        Ntot += N
        print('ye')
    
    vdos_tot /= Ntot
    if div_by_freqs == True:
            vdos_tot = vdos_tot[100:]/freqs[100:] # remove first elems to avoid small freq values blowing
            freqs = freqs[100:]
    setup_tex(fontsize=30)
    ax.plot(freqs, vdos_tot, c=c, lw=0.8, label=official_name(ensemble))
    return ax

    

plot_style = 'average'
div_by_freqs = True
valid_plot_styles = ['all', 'average']
if plot_style not in valid_plot_styles:
    raise ValueError("plot_style must be one of the following values: " + (','.join(valid_plot_styles)))

ensembles = ['tempdot6', '40x40']
colours = ['r', 'b']

setup_tex(fontsize=30)

fig, axs = plt.subplots(2,1,sharex=True, sharey=True)

for e, c, ax in zip(ensembles, colours, axs):
    if plot_style == 'all':
        ax = plot_all_at_once(e, ax, c, div_by_freqs=div_by_freqs)
    elif plot_style == 'average':
        ax = plot_average(e, ax, c, div_by_freqs=div_by_freqs)
    else:
        print(f'!!!!! plot_style = {plot_style} not supported !!!!!')

    if plot_style == 'all':
        if div_by_freqs == True:
            ylabel = '$g(\omega)/\omega$'
        else:
            ylabel = '$g(\omega)$' 
    else:
        if div_by_freqs == True:
            ylabel = '$\langle g(\omega)\\rangle /\omega$'
        else:
            ylabel = '$\langle g(\omega)\\rangle$'
    ax.set_ylabel(ylabel)
    ax.legend()

axs[1].set_xlabel('$\omega$ [THz]')

fig.subplots_adjust(hspace=0.087)
plt.show()