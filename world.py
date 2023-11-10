import numpy as np
from grid import Grid
from numpy.typing import NDArray

class World:
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
        return self._height

    @height.setter
    def height(self, height: int) -> None:
        self._height = height

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, width: int) -> None:
        self._width = width

    @property
    def bc(self) -> str:
        return self._bc

    @bc.setter
    def bc(self, bc: str) -> None:
        self._bc = bc

    @property
    def ic(self) -> NDArray[np.float64 | np.int64]:
        return self._ic

    @ic.setter
    def ic(self, grid: NDArray[np.float64 | np.int64]) -> None:
        self._ic = grid

    @property
    def grid(self) -> NDArray[np.float64 | np.int64]:
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
        return self._rules

    @rules.setter
    def rules(self, rules: list[str]) -> None:
        self._rules = rules

    @property
    def tick(self) -> float | int:
        return self._tick

    @tick.setter
    def tick(self, tick: float | int) -> None:
        self._tick = tick

    def outcome(self, is_alive: bool, num_live_neighbours: int) -> int:
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
        return np.sum(neighbourhood) - neighbourhood[1, 1]
