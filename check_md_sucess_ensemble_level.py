#!/usr/bin/env python 

from pathlib import Path
import subprocess as sbp
from qcnico.md_utils import check_LAMMPS_success
import sys


def sample_level_check(sample_dir):
    subsample_dirs = sample_dir.glob('subsample-*')

    all_success = True

    with open(sample_dir / 'failed_md_runs.txt', 'w') as fo:
        for d in subsample_dirs:
            log_nve = d / 'log_nve.lammps'
            success, last_line = check_LAMMPS_success(log_nve,return_last_line=True)
            if not success:     
                all_success = False
                fo.write(f"{sample_dir.parent.name.split('-')[1]}: {last_line}\n")
    
    return all_success


def ensemble_level_check(ensemble_name):
    ensemble_dir = Path(ensemble_name)
    if ensemble_name == '40x40':
        isamples = range(1,301)
    elif ensemble_name == 'tempdot6':
        isamples = range(218)
    else:
        print(f'ERROR: Unrecognized ensmble name: {ensemble_name}. Must be "40x40" or "tempdot6".')
    
    for i in isamples:
        print(f'{i} --> ', end='')
        sample_dir = ensemble_dir / f'sample-{i}' / '80.0'
        sample_success = sample_level_check(sample_dir)
        if sample_success:
            print('~ Success ~')
        else:
            nfails = sbp.run(f"wc -l {ensemble_name}/sample-{i}/80.0/failed_md_runs.txt", shell=True, capture_output=True).stdout.decode().split()[0]
            print(f' !!! {nfails} failed runs !!!')

#####################################################################

ensemble_name = sys.argv[1]
ensemble_level_check(ensemble_name)

  