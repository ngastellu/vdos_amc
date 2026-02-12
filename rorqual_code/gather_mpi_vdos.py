#!/usr/bin/env python

import sys
import numpy as np
from pathlib import Path


run_type = sys.argv[1]
assert run_type.strip() in ['pinned', 'unpinned', 'neglect-edge'], f'Invalid value of run_type arg: {run_type}. Must be "pinned" or "unpinned".'

if run_type == 'pinned':
    vdos_dir = Path('mpi_vdos/')
elif run_type == 'unpinned':
    vdos_dir = Path('mpi_vdos_unpinned/')
else:
    vdos_dir = Path('mpi_vdos_neglect_near_edge')

npys = list(vdos_dir.glob('*npy'))

freqs0, vdos = np.load(npys[0])
natoms = int(npys[0].stem.split('_')[2])

vdos *= natoms
natoms_tot = natoms

for npy in npys[1:]:
    natoms = int(npy.stem.split('_')[2])
    freqs, vdos2 = np.load(npy)
    assert np.all(freqs == freqs0), 'freqs do not match!'
    vdos += (vdos2 * natoms)
    natoms_tot += natoms

vdos /= natoms_tot

nn = Path().cwd().name.split('-')[1]

if run_type == 'pinned':
    outname = f'vdos_qcnico_mpi-{nn}-{natoms_tot}.npy'
elif run_type == 'unpinned':
    outname = f'vdos_qcnico_mpi_unpinned-{nn}-{natoms_tot}.npy'
else:
    outname = f'vdos_qcnico_mpi_neglect_near_edge-{nn}-{natoms_tot}.npy'

np.save(outname, np.vstack((freqs0, vdos)))
