import numpy as np
from grid import Grid
from numpy.typing import NDArray

class World:
    """The world in which the Game of Life is played."""
    def __init__(
        self,
        height: int = 1,
        width: int = 1,
        bc: str = "Hard wall",
        ic: NDArray[np.float64 | np.int64] = None,
        grid: NDArray[np.float64 | np.int64] = None,
        rules: list[int] = [2, 3, 3],
        tick: float | int = 0.1,
    ) -> None:
        """Create a new world.

        Args:
            bc: the boundary conditions.
            ic: the initial conditions.
            rules: the rules of Game of Life.
            tick: the duration between iterations.
            grid: the grid containing dead/live cells.
            height: the vertical extent of the world.
            width: the horizontal extent of the world.
        """
        self._bc = bc
        self._ic = ic
        self._rules = rules
        self._tick = tick
        self._grid = grid
        if grid is None:
            self._height = height
            self._width = width

    @property
    def height(self) -> int:
        """The vertical extent of the world."""
        return self._height

    @height.setter
    def height(self, height: int) -> None:
        self._height = height

    @property
    def width(self) -> int:
        """The horizontal extent of the world."""
        return self._width

    @width.setter
    def width(self, width: int) -> None:
        self._width = width

    @property
    def bc(self) -> str:
        """The boundary conditions of the world."""
        return self._bc

    @bc.setter
    def bc(self, bc: str) -> None:
        self._bc = bc

    @property
    def ic(self) -> NDArray[np.float64 | np.int64]:
        """The world's initial state."""
        return self._ic

    @ic.setter
    def ic(self, grid: NDArray[np.float64 | np.int64]) -> None:
        self._ic = grid

    @property
    def grid(self) -> NDArray[np.float64 | np.int64]:
        """The world's spatial distribution of dead/live cells."""
        return self._grid

    @grid.setter
    def grid(self, grid: NDArray[np.float64 | np.int64]) -> None:
        self._grid = grid
        if grid is not None:
            self._height, self._width = grid.ny, grid.nx
        else:
            self._height, self._width = None, None    

    @property
    def rules(self) -> list[int]:
        """The rules of Game of Life."""
        return self._rules

    @rules.setter
    def rules(self, rules: list[str]) -> None:
        self._rules = rules

    @property
    def tick(self) -> float | int:
        """The time between iterations."""
        return self._tick

    @tick.setter
    def tick(self, tick: float | int) -> None:
        self._tick = tick

    def outcome(self, is_alive: bool, num_live_neighbours: int) -> int:
        """The outcome of a cell after an iteration, given its current state and those of its neighbours.

        Args:
            is_alive: whether the cell is dead or alive.
            num_live_neighbours: how many live neighbours the cell has.
        """
        if is_alive:
            if num_live_neighbours == self._rules[0] or num_live_neighbours == self._rules[1]:
                return 1
            else:
                return 0
        else:
            if num_live_neighbours == self._rules[2]:
                return 1
            else:
                return 0

    def count_live_neighbours(self, neighbourhood: NDArray[np.float64 | np.int64]) -> int:
        """Count the number of live neighbours a cell has.

        Args:
            neighbourhood: the nearest neighbours of the cell.
        """
        return np.sum(neighbourhood) - neighbourhood[1, 1]
