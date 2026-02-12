#!/usr/bin/env python

import sys
from pathlib import Path
import numpy as np
from qcnico.coords_io import write_LAMMPS_data


eps = 5 # extra room in angstroms for box size

Lz = float(sys.argv[1])
z_coord = Lz / 2 # put sheet in the middle of the box

infile = 'coords.npy'
atoms = np.load(infile)

if atoms.shape[1] == 2:
    N = atoms.shape[0]
    atoms = np.vstack((atoms.T, np.zeros(N))).T # promote atoms to 3d

atoms[:,2] =  z_coord

Lx = np.max(atoms[:,0])  + eps
Ly = np.max(atoms[:,1])  + eps

min_coords = np.array([np.min(atoms[:,k]) for k in range(3)]) - eps
min_coords[2] = 0
supercell = np.array([Lx, Ly, Lz])


write_LAMMPS_data(atoms, supercell, minimum_coords=min_coords,filename='carbon.data')

