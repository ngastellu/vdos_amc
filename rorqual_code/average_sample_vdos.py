#!/usr/bin/env python

import sys
from pathlib import Path
import numpy as np



subsample_size = sys.argv[1]
run_type = sys.argv[2]

workdir = Path(subsample_size)


assert run_type.strip() in ['pinned', 'unpinned', 'neglect-edge'], f'Invalid value of run_type arg: {run_type}. Must be "pinned" or "unpinned".'
if run_type == 'pinned':
    vdos_npy_prefix = f'vdos_qcnico_mpi'
elif run_type == 'unpinned':
    vdos_npy_prefix = f'vdos_qcnico_mpi_unpinned'
else:
    vdos_npy_prefix = f'vdos_qcnico_mpi_neglect_near_edge'


subsample_dirs = list(workdir.glob('subsample-*'))
ntot = len(subsample_dirs)
nsucc = 0

vdos_list = []
freqs_list = []
natoms = []

for ssd in subsample_dirs:
    print(f'Loading VDOS from {str(ssd)}...', end=' ')
    n = ssd.name.split('-')[1]
    pattern = f'{vdos_npy_prefix}-{n}-*.npy'
    vdos_npy_path = list(ssd.glob(pattern))
    if len(vdos_npy_path) == 0:
        print(f"[average_sample_vdos] ERROR: VDOS NPY not found at: {str(ssd)}/{pattern}!")
        continue
    else:
        try:
            vdos_npy_path = vdos_npy_path[0] # only one element in this array
            vdos = np.load(vdos_npy_path)
            freqs_list.append(vdos[0,:])
            vdos_list.append(vdos[1,:])
            natoms.append(int(vdos_npy_path.stem.split('-')[-1]))
            nsucc += 1
            print('Success!')
        except Exception as e:
            print(e)

print(f'\n{nsucc} / {ntot} successful VDOS runs.')

# Check that all VDOS are resolved on identical grids (up to machine precision)
dw = np.mean(np.diff(freqs_list, axis=1))
tolerance = 0.01

print('All frequencies match: ', np.all(np.diff(freqs_list, axis=0) < (dw * tolerance)))

avg_vdos = np.average(vdos_list, weights=natoms, axis=0)
vdos_npy_out = workdir / f'{vdos_npy_prefix}_graphene_OBC.npy'
np.save(vdos_npy_out, np.vstack((freqs_list[0], avg_vdos)))