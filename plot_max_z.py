#!/usr/bin/env python 

import numpy as np
import matplotlib.pyplot as plt
from qcnico.coords_io import stream_lammps_traj
from qcnico.md_utils import count_natoms_lammpstrj, count_nsteps_lammpstrj, get_framerate_lammpstrj
from qcnico.plt_utils import setup_tex
from pathlib import Path


trajfile = Path('~/Desktop/simulation_outputs/vdos/graphene/dump_nve_unpinned-50.lammpstrj').expanduser()

N = count_natoms_lammpstrj(trajfile)
print('# of atoms  = ',N)
nsteps = count_nsteps_lammpstrj(trajfile,N)
print('# of steps = ', nsteps)
frame_rate, iframe0 = get_framerate_lammpstrj(trajfile, return_first_frame_index=True)
print('(frame rate, first frame index) = ', (frame_rate, iframe0))

nframes = 1 + ((nsteps-iframe0)//(frame_rate*100))
print('# of sampled frames =',  nframes)

frames_gen = stream_lammps_traj(trajfile, iframe0, nsteps, step=frame_rate*100, start_file=iframe0, step_file=frame_rate)
z_max_abs = np.zeros(nframes)

for k, pos in enumerate(frames_gen):
    print(k)
    # if pos.shape != (N, 3):
    #     print(k, k*frame_rate + iframe0)
    #     continue
    z_max_abs[k] = np.max(np.abs(pos[:,2]))

iframes = np.arange(iframe0, nsteps-100, frame_rate*100)

setup_tex()

plt.plot(iframes, z_max_abs, 'r-', lw=0.8)
plt.xlabel('MD frame')
plt.ylabel('$\\text{max}\,|z|$')
plt.show()
