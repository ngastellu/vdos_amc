#!/usr/bin/env python

from pathlib import Path
from itertools import chain
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
from qcnico.coords_io import read_dump
from qcnico.qcplots import plot_atoms

"""This script obtains the list of atoms close to the frozen edge atoms in a MD simulation from which a VDOS is computed.
It then plots the frozen edge atoms and the atoms close to make sure the obtained lists make sense.

The atoms close to the frozen edge atoms are neglected when extracting the VDOS from the MD trajectory."""


DATADIR = Path('~/Desktop/simulation_outputs/vdos/graphene').expanduser()
xsf_path = DATADIR / 'subsample0_frame0_nve.xsf'

read_out, *_ = read_dump(xsf_path, read_cols=slice(1,7))
pos = read_out[:,:3]
vels = read_out[:,3:]

frozen_mask = np.all(vels == 0, axis = 1)

# Indices of frozen and mobile atoms in global `pos` array
ifrozen = frozen_mask.nonzero()[0]
imobile = (~frozen_mask).nonzero()[0]


tree_frozen = KDTree(pos[frozen_mask])
tree_mobile = KDTree(pos[~frozen_mask])

cutoff = 2.6 # roughly distance of second coordination shell in graphene

ineglect_mobile = list(chain.from_iterable(tree_frozen.query_ball_tree(tree_mobile, cutoff))) #inds of atoms near frozen atoms in `tree_mobile`
ineglect_global = imobile[ineglect_mobile] #inds of atoms near frozen atoms in global `pos` array 

clrs = np.array(['k'] * pos.shape[0])
clrs[ifrozen] = 'r'
clrs[ineglect_global] = 'blue'

plot_atoms(pos, colour=clrs)