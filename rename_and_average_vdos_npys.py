#!/usr/bin/env python

import sys
from os import chdir
from pathlib import Path
from functools import reduce
import numpy as np


def get_Natoms_from_vdos_npys(subsample_dir):
    npys_dir = subsample_dir / 'mpi_vdos'
    npys = npys_dir.glob("*.npy")
    return sum(map(lambda x: int(x.stem.split('_')[-1]), npys))

def get_Natoms_from_data(subsample_dir):
    with open(subsample_dir / 'carbon.data') as fo:
        for _ in range(3):
            line = fo.readline()
    return int(line.strip().split()[0])


def rename_subsample_vdos(subsample_dir):
    Natoms_npys = get_Natoms_from_vdos_npys(subsample_dir)
    Natoms_data = get_Natoms_from_data(subsample_dir)

    assert Natoms_npys == Natoms_data, f"ERROR: Natoms from VDOS NPYs ({Natoms_npys}) != Natoms from carbon.data ({Natoms_data})"

    Natoms = Natoms_npys

    n_subsample = int(subsample_dir.name.split('-')[1])

    vdos_npy = subsample_dir / f"vdos_qcnico_mpi-{n_subsample}.npy"
    new_npy_name = subsample_dir / f"vdos-{n_subsample}_{Natoms}.npy"
    vdos_npy.rename(new_npy_name)

    return Natoms, np.load(new_npy_name)


def full_sample_VDOS(n_sample):
    sample_dir = Path(f"sample-{n_sample}/80.0")
    subsample_dirs = sample_dir.glob("subsample-*")
    Natoms_list = []
    vdos_list = []
    for subsamp_d in subsample_dirs:
        Natoms, vdos = rename_subsample_vdos(subsamp_d)
        Natoms_list.append(Natoms)
        vdos_list.append(vdos)

    vdos_list = np.array(vdos_list)
    return vdos_list.sum(axis=0)/ sum(Natoms_list)


def process_sample(sample_dir):
    n_sample = int(sample_dir.name.split('-')[1])
    sample_vdos = full_sample_VDOS(n_sample)
    np.save(sample_dir / f"vdos-{n_sample}.npy", sample_vdos)


def process_ensemble(structype):
    ensemble_dir = Path(structype)
    sample_dirs = sorted(ensemble_dir.glob("sample-*"))
    chdir(ensemble_dir)
    for sd in sample_dirs:
        print(f"\n*** {sd} ***")
        try:
            process_sample(sd)
        except Exception as e:
            print(e)
            #continue
    
####################################################################################################

structype = sys.argv[1]
process_ensemble(structype)
