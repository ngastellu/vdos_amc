#!/usr/bin/env python 

import numpy as np
from qcnico.coords_io import stream_lammps_traj
from qcnico.vdos import vdos
from mpi4py import MPI

def get_Natoms(dump):
    with open(dump) as fo:
        for _ in range(3):
            fo.readline()
    return int(fo.readline().strip())


comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
rank = comm.Get_rank()

dump = 'dump_nve-1.lammpstrj'
Natoms = get_Natoms(dump)

natoms_per_proc = Natoms // nprocs

if rank < nprocs - 1:
    proc_atoms = np.arange(rank*natoms_per_proc, (rank+1)*natoms_per_proc)# indices of atoms handled by this proc
else:
    proc_atoms = np.arange(rank*natoms_per_proc, Natoms)

frames_gen = stream_lammps_traj(dump,start=110000,end=200000, step=1, stream_cols=slice(5,8),start_file=180000,step_file=1, atom_indices=proc_atoms)

vels = np.array([v for v in frames_gen])

vdos_graphene = vdos(vels, dt=5e-4)

np.save(f'vdos_qcnico-{rank}_{proc_atoms.shape[0]}.npy', vdos_graphene)