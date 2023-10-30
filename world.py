import numpy as np

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
        self.set_bc(bc)
        self.set_seed(seed)
        self.set_rules(rules)
        self.set_tick(tick)
        self.set_grid(grid)
        if grid is None:
            self.set_height(height)
            self.set_width(width)

    def set_height(self, height) -> None:
        self._height = height

    def set_width(self, width) -> None:
        self._width = width

    def set_bc(self, bc) -> None:
        self._bc = bc

    def set_seed(self, seed) -> None:
        self._seed = seed

    def set_grid(self, grid) -> None:
        self._grid = grid
        if grid is not None:
            self._height, self._width = grid.ny(), grid.nx()
        else:
            self._height, self._width = None, None

    def set_rules(self, rules) -> None:
        self._rules = rules

    def set_tick(self, tick) -> None:
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
