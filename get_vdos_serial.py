#!/usr/bin/env python 

import numpy as np
from qcnico.coords_io import stream_lammps_traj
from qcnico.vdos import vdos


dump = 'dump_nve-1.lammpstrj'

frames_gen = stream_lammps_traj(dump,start=110000,end=200000, step=1, stream_cols=slice(5,8),start_file=100000,step_file=1)

vels = np.array([v for v in frames_gen])
print(vels.shape, flush=True)

vdos_graphene = vdos(vels, dt=5e-4)

np.save('vdos_qcnico.npy', vdos_graphene)
