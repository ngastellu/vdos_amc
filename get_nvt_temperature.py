#!/usr/bin/env python

from qcnico.md_utils import parse_LAMMPS_log
from qcnico.plt_utils import setup_tex
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# logfile = Path('~/Desktop/simulation_outputs/vdos/graphene/log_nve.lammps').expanduser()
# logfile = Path('~/Desktop/simulation_outputs/vdos/tempdot6/subsample_center/sample-0/log_nve.lammps').expanduser()
logfile = Path('~/Desktop/simulation_outputs/vdos/tempdot6/full_structure-64/log_nve.lammps').expanduser()
LAMMPS_log = parse_LAMMPS_log(logfile)

steps = LAMMPS_log['Step']
temp = LAMMPS_log['Temp']
energy = LAMMPS_log['TotEng']

#np.save('run_temperature.npy',temps)

setup_tex()
plt.plot(steps, energy, 'r-', lw=0.8)
# plt.plot()
plt.xlabel('Step')
plt.ylabel('$E_{tot}$ [eV]')
plt.show()

