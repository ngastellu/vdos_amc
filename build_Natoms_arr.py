#!/usr/bin/env python

import sys
from pathlib import Path
import numpy as np



def official_name(ensemble):
    if ensemble == '40x40':
        return 'sAMC-500'
    elif ensemble == 'tempdot6':
        return 'sAMC-q400'
    else:
        raise ValueError(f"Invalid ensemble {ensemble}!")


def get_Natoms_sample(xyz):
    with open(xyz) as fo:
        return int(fo.readline().strip())


def build_Natoms_arr(ensemble):
    ensemble_dir = Path(f'/Users/nico/Desktop/scripts/disorder_analysis_MAC/structures/{ensemble}')
    sample_xyzs = ensemble_dir.glob('*xyz')
    arr = []
    for sample_xyz in sample_xyzs:
        i = int(sample_xyz.stem.split('-')[1])
        try:
            N = get_Natoms_sample(sample_xyz)
            arr.append([i, N])
        except Exception as e:
            print(f'{i} --> {e}')
    
    return np.array(arr)



ensemble = sys.argv[1]
Natoms_arr = build_Natoms_arr(official_name(ensemble))
np.save(f'/Users/nico/Desktop/simulation_outputs/vdos/{ensemble}/natoms.npy', Natoms_arr)
