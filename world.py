import numpy as np
from grid import Grid

class World:
    def __init__(
        self,
        height=1,
        width=1,
        bc="Hard wall",
        seed=None,
        grid=None,
        rules=[2, 3, 3],
        tick=0.1,
    ) -> None:
        self._bc = bc
        self._seed = seed
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
    def height(self, height) -> None:
        self._height = height

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, width) -> None:
        self._width = width

    @property
    def bc(self) -> str:
        return self._bc

    @bc.setter
    def bc(self, bc) -> None:
        self._bc = bc

    @property
    def seed(self) -> None:
        return self._seed

    @seed.setter
    def seed(self, seed) -> None:
        self._seed = seed

    @property
    def grid(self) -> None:
        return self._grid

    @grid.setter
    def grid(self, grid) -> None:
        self._grid = grid
        if grid is not None:
            self._height, self._width = grid.ny, grid.nx
        else:
            self._height, self._width = None, None    

    @property
    def rules(self) -> list[int]:
        return self._rules

    @rules.setter
    def rules(self, rules) -> None:
        self._rules = rules

    @property
    def tick(self) -> float | int:
        return self._tick

    @tick.setter
    def tick(self, tick) -> None:
        self._tick = tick

    def outcome(self, is_alive, num_live_neighbours):
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

    def count_live_neighbours(self, neighbourhood):
        return np.sum(neighbourhood) - neighbourhood[1, 1]
