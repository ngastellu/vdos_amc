#!/usr/bin/env python

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from qcnico.md_utils import parse_LAMMPS_log


log_directory = Path('~/Desktop/simulation_outputs/vdos/tempdot6/subsample_center/nve_logs/').expanduser()
dt = 5e-4

for n in [1,7,10]:
    fig, axs = plt.subplots(2,1,sharex=True)
    log_file = log_directory / f'log_nve-{n}.lammps'
    data = parse_LAMMPS_log(log_file)
    print(data.keys())

    t = data['Step'] * dt
    etot = data['TotEng']

    axs[0].plot(t, etot, lw=0.8)
    axs[0].set_ylabel('$E_{tot}$ [eV] (pinned edges)')
    
    log_file = log_directory / f'log_nve_unpinned-{n}.lammps'
    data = parse_LAMMPS_log(log_file)

    t = data['Step'] * dt
    etot = data['TotEng']

    axs[1].plot(t, etot, lw=0.8)
    axs[1].set_ylabel('$E_{tot}$ [eV] (unpinned edges)')
    axs[1].set_xlabel('Time [ps]')

    plt.show()