import numpy as np
import matplotlib.pyplot as plt


class Grid:
    def __init__(self, cells=None, nx=0, ny=0):
        if cells is None:
            self._cells = np.zeros([nx, ny])
            self._nx = nx
            self._ny = ny
        else:
            self._cells = cells
            # can't also specify nx and ny unless they are same as size of cells
            self._nx, self._ny = np.shape(cells)

    def cells(self):
        return self._cells

    def nx(self):
        return self._nx

    def ny(self):
        return self._ny

    def num_alive(self):
        return np.sum(self._cells == 1)

    def num_dead(self):
        return np.sum(self._cells == 0)

    def binarise(self, threshold=0.66):
        self._cells = np.where(self._cells < threshold, 0, 1)

    def clear(self):
        self._cells.fill(0)

    def plot(self):
        return plt.pcolor(self.cells(), cmap="binary")

