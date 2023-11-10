import numpy as np
import matplotlib.pyplot as plt
from numpy.typing import NDArray

class Grid:
    """A grid for playing Game of Life."""
    def __init__(self, cells: NDArray[np.float64 | np.int64] = None, nx: int = 0, ny: int = 0) -> None:
        """Create a new grid.

        Args:
            cells: the spatial distribution of dead/live cells.
            nx: the number of cells along the horizontal axis.
            ny: the number of cells along the vertical axis.
        """
        if cells is None:
            self._cells = np.zeros([ny, nx])
            self._nx = nx
            self._ny = ny
        else:
            self._cells = cells
            # can't also specify nx and ny unless they are same as size of cells
            self._ny, self._nx = np.shape(cells)

    @property
    def cells(self) -> NDArray[np.float64 | np.int64]:
        """The grid cells."""
        return self._cells

    @cells.setter
    def cells(self, cells: NDArray[np.float64 | np.int64]) -> None:
        self._cells = cells
        self._ny, self._nx = cells.shape

    @property
    def nx(self) -> int:
        """The number of cells along the horizontal axis."""
        return self._nx

    @property
    def ny(self) -> int:
        """The number of cells along the vertical axis."""
        return self._ny

    def num_alive(self) -> int:
        """The number of live cells."""
        return np.sum(self._cells == 1)

    def num_dead(self) -> int:
        """The number of dead cells."""
        return np.sum(self._cells == 0)

    def binarise(self, threshold: float = 0.66) -> None:
        """Set cells dead or alive based on their numerical value.

        Args:
            threshold: the value below which cells are considered to be dead.
        """
        self._cells = np.where(self._cells < threshold, 0, 1)

    def clear(self) -> None:
        """Set all cells to zero, i.e. all cells are dead."""
        self._cells.fill(0)

    def plot(self):
        """Plot the grid cells."""
        return plt.pcolor(self.cells, cmap="binary")
