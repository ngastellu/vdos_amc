#!/usr/bin/env python 
import sys
from pathlib import Path
from itertools import chain
import numpy as np
from scipy.spatial import KDTree
from qcnico.coords_io import stream_lammps_traj
from qcnico.vdos import vdos
from mpi4py import MPI
from time import perf_counter

def get_Natoms(dump):
    with open(dump) as fo:
        for _ in range(3):
            fo.readline()
        N = int(fo.readline().strip())
    return N

def get_compute_mask(pos, vels, cutoff=2.6):
    frozen_mask = np.all(vels == 0, axis = 1)

    # Indices of frozen and mobile atoms in global `pos` array
    ifrozen = frozen_mask.nonzero()[0]
    imobile = (~frozen_mask).nonzero()[0]


    tree_frozen = KDTree(pos[frozen_mask])
    tree_mobile = KDTree(pos[~frozen_mask])

    ineglect_mobile = list(chain.from_iterable(tree_frozen.query_ball_tree(tree_mobile, cutoff))) #inds of atoms near frozen atoms in `tree_mobile`
    ineglect_global = imobile[ineglect_mobile] #inds of atoms near frozen atoms in global `pos` array 

    vdos_mask = np.ones(pos.shape[0], dtype=bool)
    vdos_mask[ineglect_global] = False
    vdos_mask[ifrozen] = False

    return vdos_mask



dump = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])
step = int(sys.argv[4])
start_file = int(sys.argv[5])
step_file = int(sys.argv[6])

neglect_edge = True


time_start = perf_counter()

comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
rank = comm.Get_rank()

#dump = f'dump_nve-{step_file}.lammpstrj'
Natoms = get_Natoms(dump)

natoms_per_proc = Natoms // nprocs

if rank < nprocs - 1:
    proc_atoms = np.arange(rank*natoms_per_proc, (rank+1)*natoms_per_proc)# indices of atoms handled by this proc
else:
    proc_atoms = np.arange(rank*natoms_per_proc, Natoms)

if neglect_edge == True:

    frame0 = next(stream_lammps_traj(dump, 
                                start = start_file, 
                                end=start_file + step_file, 
                                step=step_file, 
                                stream_cols=slice(1,7),
                                start_file=start_file,
                                step_file=step_file,
                                atom_indices=proc_atoms))

    pos0 = frame0[:,:3]
    vels0 = frame0[:,3:]

    vdos_mask = get_compute_mask(pos0, vels0)
    outdir = 'mpi_vdos_negelect_near_edge'

else:
    vdos_mask = np.ones(proc_atoms.shape[0])
    outdir = 'mpi_vdos'

ncompute = vdos_mask.sum()
frames_gen = stream_lammps_traj(dump,start=start,
                                end=end,
                                step=step,
                                stream_cols=slice(4,7),
                                start_file=start_file,
                                step_file=step_file,
                                atom_indices=proc_atoms)

vels = np.array([v[vdos_mask,:] for v in frames_gen])

dt = 1e-4 * step # sampling rate in ps
vdos_graphene = vdos(vels, dt=dt)


#if 'unpinned' in dump:
#    outdir = Path('mpi_vdos_unpinned')
#else:
#    outdir = Path('mpi_vdos')
 
Path.mkdir(outdir, exist_ok=True)

npy_name = outdir / f'vdos_qcnico-{rank}_{ncompute}.npy'
np.save(npy_name, vdos_graphene)

time_end = perf_counter()
print(f'Proc {rank} took {time_end-time_start} seconds.')
