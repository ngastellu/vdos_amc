#!/usr/bien/env python

import numpy as np
from qcnico.qcplots import plot_atoms
import matplotlib.pyplot as plt
from ase.build import graphene_nanoribbon



gnr1 = graphene_nanoribbon(180, 84, type='armchair', saturated=False, vacuum=None,sheet=True)
pos1 = gnr1.positions[:,[0,2]]
a1 = gnr1._cellobj.array[0,0]
a2 = gnr1._cellobj.array[2,2]

print(a1)
print(a2)


supercell_copy = pos1.copy()
supercell_copy[:,0] += a1

supercell_copy2 = pos1.copy()
supercell_copy2[:,1] += a2

supercell_copy3 = supercell_copy.copy()
supercell_copy3[:,1] += a2

fig, ax = plot_atoms(pos1,dotsize=2,show=False)
ax.scatter(*supercell_copy.T, marker='o',facecolor='none', edgecolor='r',linewidth=0.5,s=8.0)
ax.scatter(*supercell_copy2.T, marker='o',facecolor='none', edgecolor='b',linewidth=0.5,s=8.0)
ax.scatter(*supercell_copy3.T, marker='o',facecolor='none', edgecolor='g',linewidth=0.5,s=8.0)

print('a1 = ', a1)
print('a2 = ', a2)

print(pos1.shape)

outfile = 'square_ase_graphene_cell_big.npy'
np.save(outfile, pos1)
np.save(f'cell_dims_of_{outfile}' , np.array([a1, a2]))

plt.show()

