#!/usr/bin/env pythonw

import sys
import numpy as np
from qcnico.coords_io import read_xyz, write_xyz
from qcnico.remove_dangling_carbons import remove_dangling_carbons
from qcnico.lattice import cartesian_product
from pathlib import Path

def get_size(coords):
    minX = np.min(coords[:,0])
    minY = np.min(coords[:,1])

    maxX = np.max(coords[:,0])
    maxY = np.max(coords[:,1])


    LX = maxX - minX
    LY = maxY - minY

    return LX, LY


def get_grid_size(Lx, Ly, l):
    nx = int(Lx // l)
    ny = int(Ly // l)
    return nx, ny

def truncate(coords, l, center, return_coords=True):
    upper_bounds = center + np.array([l,l])/2
    lower_bounds = center - np.array([l,l])/2

    Xmask = (coords[:,0] <= upper_bounds[0]) * (coords[:,0] >= lower_bounds[0])
    Ymask = (coords[:,1] <= upper_bounds[1]) * (coords[:,1] >= lower_bounds[1])

    mask = Xmask*Ymask

    if return_coords == True:
        return coords[mask]
    else:
        return mask


def sample_grid(coords, l, yield_center=False):
    """Truncate a large MAC structure by keeping a `l*l` square at grid position `(i,j)`."""

    Lx, Ly = get_size(coords)
    nx, ny = get_grid_size(Lx, Ly, l)

    grid_inds = cartesian_product(np.arange(nx), np.arange(ny))
 
    sample_centers = np.array([[Lx - l*(2*j + 1)/2, Ly - l*(2*i + 1)/2] for i,j in grid_inds])

    for center in sample_centers:
        if yield_center == True:
            yield truncate(coords, l, center), center
        else:
            yield truncate(coords, l, center)
        




l = 80.0
rCC = 1.8

posfile = 'square_ase_graphene_cell_big.npy'


MAC = np.load(posfile)

for k, out in enumerate(sample_grid(MAC, l, yield_center=True)):
    outdir = Path(f'{l}/subsample-{k}')
    Path.mkdir(outdir, parents=True, exist_ok=True)
    sample, center = out
    sample = remove_dangling_carbons(sample, rCC)
    np.save(outdir / 'coords.npy', sample)
    np.save(outdir / 'center.npy', center)
