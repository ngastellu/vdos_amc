#!/usr/bin/env python

import matplotlib.pyplot as plt
from qcnico.plt_utils import setup_tex
from qcnico.data_utils import moving_average
import numpy as np
from pathlib import Path
from dump2VDOS import get_vdos
import subprocess as sbp



def get_nframes(vacf_file):
    tail_out = sbp.run(f'tail -n 10 {vacf_file}', shell=True, capture_output=True).stdout.decode().split('\n')
    print(tail_out)
    ipenultimate = int(tail_out[0].split()[0])
    iultimate = int(tail_out[-6].split()[0])
    step = iultimate - ipenultimate
    
    with open(vacf_file) as fo:
        for _ in range(4):
            line0 = fo.readline()
        ifirst = int(line0.split()[0])
    
    return (iultimate - ifirst) // step


def process_frame(fo):
    line = fo.readline()
    iframe = int(line.strip().split()[0])
    for _ in range(4):
        line = fo.readline()
    vv =  float(line.split()[1])
    return iframe, vv
    

def parse_vacf(vacf_file):
    nframes = get_nframes(vacf_file)
    vacf = np.zeros((2,nframes))

    # Skip first three lines
    with open(vacf_file) as fo:
        for _ in range(3):
            fo.readline()
        for k in range(nframes):
            vacf[:,k] = process_frame(fo)

    vacf[1,:] /= vacf[1,0]
    return vacf

dt = 0.5 # MD timestep in fs 
corlen = 500

vacf_full_file = Path('~/Desktop/simulation_outputs/vdos/graphene/vacf_full.dat').expanduser()
vacf_full = parse_vacf(vacf_full_file)

vacf_ave_file = Path('~/Desktop/simulation_outputs/vdos/graphene/vacf_ave100.dat').expanduser()
vacf_ave = parse_vacf(vacf_ave_file)

fig, ax = plt.subplots()


full_time = vacf_full[0,:]
ax.plot(*vacf_full, label='full', lw=0.8)
ax.plot(*vacf_ave, label='avg', lw=0.8)
# ax.plot(full_time, moving_average(vacf_full[1,:],500),lw=0.8)
ax.set_ylabel(r"$\frac{v(t)\cdot v(t)}{v(0)\cdot v(0)}$", fontsize=20)
ax.set_xlabel("Time [ps]")
ax.legend()
plt.show()


get_vdos(vacf_full, corlen, dt)