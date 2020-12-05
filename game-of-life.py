from typing import Any

from mesa import *
from mesa.space import Grid
from enum import Enum
import matplotlib.pyplot as plt
import random


class State(Enum):
    DEAD = 0
    LIVE = 1


class MyModel(Model):
    def __init__(self, size: int, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.size = size
        self.grid = Grid(size, size, True)
        for i in range(size):
            for j in range(size):
                if random.randint(0, 1) == 0:
                    state = State.DEAD
                else:
                    state = State.LIVE
                cell_agent = CellAgent(i * size + j, self, state)
                self.grid.place_agent(cell_agent, (i, j))

    def step(self):
        new_grid = Grid(self.size, self.size, True)
        for i in range(self.size):
            for j in range(self.size):
                new_cell_agent = self.grid[i][j].step()
                new_grid.place_agent(new_cell_agent, (i, j))
        self.grid = new_grid


class CellAgent(Agent):
    def __init__(self, unique_id: int, model: MyModel, state: State):
        super().__init__(unique_id, model)
        self.state = state

    def step(self) -> Agent:
        neighbors = self.model.grid.get_neighbors(
            (self.unique_id // self.model.size, self.unique_id % self.model.size),
            moore=True)
        total = 0
        for neighbor in neighbors:
            total += neighbor.state.value
        if total == 3:
            return CellAgent(self.unique_id, self.model, State.LIVE)
        elif total == 2:
            return CellAgent(self.unique_id, self.model, self.state)
        else:
            return CellAgent(self.unique_id, self.model, State.DEAD)


if __name__ == '__main__':
    SIZE = 10
    STEPS = 20
    my_model = MyModel(SIZE)
    """
    for i in range(SIZE):
        for j in range(SIZE):
            my_model.grid[i][j].state = State.DEAD
    my_model.grid[2][2].state = State.LIVE
    my_model.grid[2][3].state = State.LIVE
    my_model.grid[3][2].state = State.LIVE
    my_model.grid[3][3].state = State.LIVE
    """
    for step in range(STEPS):
        arr = [[] for g in range(SIZE)]
        for i in range(SIZE):
            for j in range(SIZE):
                agent = my_model.grid[i][j]
                arr[i].append(agent.state.value)
        plt.imshow(arr)
        plt.show()
        my_model.step()
