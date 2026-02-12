#!/usr/bin/env python

from pathlib import Path
import numpy as np


current_dir = Path.cwd()
system_size = int(float(current_dir.name))

subsample_dirs = list(current_dir.glob('subsample-*'))

ntot = len(subsample_dirs)
nsucc = 0

vdos_list = []
freqs_list = []
natoms = []

for ssd in subsample_dirs:
    print(f'Loading VDOS from {str(ssd)}...', end=' ')
    n = ssd.name.split('-')[1]
    try:
        vdos = np.load(ssd / f'vdos_qcnico_mpi-{n}.npy')
        freqs_list.append(vdos[0,:])
        vdos_list.append(vdos[1,:])
        natoms.append(np.load(ssd / f'coords.npy').shape[0])
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
np.save(f'avg_vdos-{system_size}.npy', np.vstack((freqs_list[0], avg_vdos)))