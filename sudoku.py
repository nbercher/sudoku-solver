# -*- coding: utf-8 -*-

"""
sudoku.py - Sudoku solver

Nicolas Bercher, nicolas.bercher@altihydrolab.fr, 2022-01-01.

This script is the property of Nicolas Bercher, AltiHydroLab.fr.
All rights reserved.
"""

import os
import sys
import numpy

GRID_SIZE = 9
MIN_CLUES_9x9 = 17


def solve(grid):
    """Solve Sudoku grid."""
    return grid # tmp


def read(filepath):
    """Read CSV file as a Numpy array."""
    arr = numpy.genfromtxt(filepath, delimiter=',')
    return arr


def check_grid(grid):
    """Check the grid post reading."""
    if numpy.prod(grid_in.shape) != GRID_SIZE*GRID_SIZE:
        raise ValueError("Wrong input grid size %dx%d, but %dx%d is required." % grid_in.shape + (GRID_SIZE,GRID_SIZE,))
    if (GRID_SIZE*GRID_SIZE - numpy.sum(numpy.isnan(grid_in))) < MIN_CLUES_9x9:
        raise ValueError("Impossible to solve Sudoku grid of size %dx%d with less than 17 clues." % grid_in.shape)


def grid2int(arr):
    """Convert floating point array with NaNs to interger array with zeroes."""
    arr[numpy.isnan(arr)] = 0
    return numpy.int64(arr)


def write(filepath, arr):
    """Write CSV file from a Numpy array, cast to integer before actual write."""
    arr = grid2int(arr)
    numpy.savetxt(filepath, arr, delimiter=',', fmt="%d")
    print(arr)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 -c solve.py file.csv")
        exit()
    # Process input file:
    filepath_in = sys.argv[1]
    grid_in = read(filepath_in)
    check_grid(grid_in)
    # Solve:
    grid_out = solve(grid_in)
    # Process output file:
    filepath_out = os.extsep.join([filepath_in, 'solved'])
    write(filepath_out, grid_out)
