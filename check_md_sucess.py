#!/usr/bin/env python 

from pathlib import Path
from qcnico.md_utils import check_LAMMPS_success



cwd = Path('.')
subsample_dirs = cwd.glob('subsample-*')

nsucc = 0
ntot = 0
failed = []

for d in subsample_dirs:
    ntot += 1
    print(str(d), end = ' --> ')
    log_nve = d / 'log_nve.lammps'
    success, last_line = check_LAMMPS_success(log_nve,return_last_line=True)
    if success:
        print('Success ツ')
        nsucc += 1
    else:
        print('Failed! Last line = ', last_line)
        failed.append(str(d).split('-')[1])
    
print(f'\n*** {nsucc} / {ntot} successful runs ***')

if len(failed) > 0:
    print('Failed runs: ')
    for f in failed:
        print(f)