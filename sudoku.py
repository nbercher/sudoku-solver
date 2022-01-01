#! /usr/bin/env python3

# -*- coding: utf-8 -*-

"""sudoku.py - Sudoku (naive) solver.

Nicolas Bercher, nicolas.bercher@altihydrolab.fr, 2022-01-01.

This script is the property of Nicolas Bercher, AltiHydroLab.fr.
All rights reserved.

"""

import os
import sys
import numpy
import collections


GRID_SIZE = 9
BLOCK_SIZE = int(GRID_SIZE / 3)
MIN_CLUES_9x9 = 17
BLOCK_FULL = set(list(numpy.arange(1, GRID_SIZE+1)))


class Grid():
    """Sudoku grid, 9x9 size."""

    def __init__(self, arr):
        self._gsize = GRID_SIZE
        self._bsize = BLOCK_SIZE
        arr[numpy.isnan(arr)] == 0
        self.grid = numpy.int64(arr)

    def getelementblock(self, l, c):
        """Get 3x3 block that hold element of element coordinates (l, c)."""
        tobs = lambda x: int(x / self._bsize)
        return self.getblock(tobs(l), tobs(c))

    def getblock(self, bl, bc):
        """Get 3x3 block of block coordinates (bl, bc)."""
        bl0, bc0 = bl * self._bsize, bc * self._bsize
        return self.grid[bl0:bl0+self._bsize,bc0:bc0+self._bsize]

    def getelementclues(self, l, c):
        """Get the set of clues for an (unset) element of element coordinates (l, c)."""
        clues_s = set()
        clues_s.update(list(self.grid[l,:]))
        clues_s.update(list(self.grid[:,c]))
        clues_s.update(list(self.getelementblock(l,c).flatten()))
        clues_s.remove(0)
        return clues_s

    def getelementpossiblevalues(self, l, c):
        """Get the set of possible values for an unset element of element coordinates (l, c)."""
        return BLOCK_FULL - self.getelementclues(l, c)

    def iterunsolved(self):
        """Iterate over the (l,c) coordinates of the unsolved element(s)."""
        for l_, c_ in zip(*numpy.where(self.grid == 0)):
            yield l_, c_

    def getunsolved(self, od=None):
        """Get an OrderedDict of the unsolved elements {(l,c): set(possible_values)}.

        If od is not None, assume this is the result of the previous
        call to self.getunsolved().

        """
        coords_iter = self.iterunsolved() if od is None else od.keys()
        unsolved_m = [((l_, c_), self.getelementpossiblevalues(l_, c_)) for l_, c_ in list(coords_iter)]
        arg_rank = numpy.argsort(numpy.array([len(v_) for _, v_ in unsolved_m]))
        unsolved_sorted_m = numpy.array(unsolved_m, dtype=object)[arg_rank]
        unsolved_od = collections.OrderedDict(unsolved_sorted_m)
        return unsolved_od

    def solve_naive(self, verbose=0):
        """Naive Sudoku solver: assume that, for each iteration, one unsolved
        element at least is directly solvable (i.e., len(getelementpossiblevalues() == 1).

        """
        # Sort unsolved elements by rank = nb possible values:
        unsolved_od = self.getunsolved()
        # Recursive solving:
        self._solve_naive_iter(unsolved_od, verbose=verbose)

    def _solve_naive_iter(self, unsolved_od, verbose=0):
        if len(unsolved_od) == 0:
            return
        for k_ in list(unsolved_od.keys()):
            pv_ = unsolved_od[k_]
            if len(pv_) == 1:
                l_, c_ = k_
                self.grid[l_, c_] = list(unsolved_od.pop(k_))[0]
                if verbose > 0:
                    print("Unsolved = %d" % (numpy.sum(self.grid==0),))
            else:
                break
        # Get updated unsolved_od and proceed:
        unsolved_od_next = self.getunsolved(od=unsolved_od)
        self._solve_naive_iter(unsolved_od_next, verbose=verbose)


def solve(arr):
    """Solve Sudoku grid."""
    grid = Grid(grid2int(arr))
    grid.solve_naive()
    return grid.grid


def read(filepath):
    """Read CSV file as a Numpy array."""
    arr = numpy.genfromtxt(filepath, delimiter=',')
    return arr


def check_grid(arr):
    """Check the grid post reading."""
    if numpy.prod(arr.shape) != GRID_SIZE*GRID_SIZE:
        raise ValueError("Wrong input grid size %dx%d, but %dx%d is required." % arr.shape + (GRID_SIZE,GRID_SIZE,))
    if (GRID_SIZE*GRID_SIZE - numpy.sum(numpy.isnan(arr))) < MIN_CLUES_9x9:
        raise ValueError("Impossible to solve Sudoku grid of size %dx%d with less than 17 clues." % arr.shape)


def grid2int(arr):
    """Convert floating point array with NaNs to interger array with zeroes."""
    arr[numpy.isnan(arr)] = 0
    return numpy.int64(arr)


def write(filepath, arr):
    """Write CSV file from a Numpy array, cast to integer before actual write."""
    arr = grid2int(arr)
    numpy.savetxt(filepath, arr, delimiter=',', fmt="%d")


def main(filepath_in):
    # Process input file:
    arr_in = read(filepath_in)
    check_grid(arr_in)
    # Solve:
    arr_out = solve(arr_in)
    # Process output file:
    filepath_out = os.extsep.join([filepath_in, 'solved'])
    write(filepath_out, arr_out)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: ./solve.py file.csv")
        exit()
    main(sys.argv[1])
