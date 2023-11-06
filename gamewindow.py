from PyQt6.QtWidgets import QWidget

import matplotlib.pyplot as plt
import numpy as np

class GameWindow(QWidget):
    def __init__(self, world):
        super().__init__()
        self._world = world
        self._create_mpl_figure()
        self.run()

    def _create_mpl_figure(self):
        plt.figure()
        ax = plt.axes(xticks=[], yticks=[])
        ax.figure.canvas.manager.set_window_title("Game of Life")
        ax.figure.canvas.manager.toolbar.hide()
        self._im = ax.imshow(self._world._grid.cells(), cmap="binary", vmin=0, vmax=1)

    def run(self):
        ni, nj = self._world._height, self._world._width
        world = np.zeros((ni+2, nj+2), dtype=int)
        plt.pause(self._world._tick)
        finished = False
        while not finished:
            world[1:-1, 1:-1] = self._world._grid._cells
            if self._world._bc == "Periodic":
                world[1:-1, 0] = self._world._grid._cells[:, -1]
                world[1:-1, -1] = self._world._grid._cells[:, 0]
                world[0, :] = world[-2, :]
                world[-1, :] = world[1, :]
            for i in range(1, ni+1):  # go down each column
                for j in range(1, nj+1):  # go across each row
                    neighbourhood = world[i - 1 : i + 2, j - 1 : j + 2]
                    num_live_neighbours = self._world.count_live_neighbours(
                        neighbourhood
                    )
                    self._world._grid._cells[i-1, j-1] = self._world.outcome(
                        world[i, j], num_live_neighbours
                    )
            if not np.any(self._world._grid._cells - world[1:-1, 1:-1]):
                finished = True
            else:
                self._im.set_data(self._world._grid._cells)
                plt.pause(self._world._tick)
