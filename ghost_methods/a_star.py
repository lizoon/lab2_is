from math import sqrt
from typing import Optional

from ghost_methods.data_structure import GridLocation, PriorityQueue, GridWithWeights


class AStar:
    def __init__(self, gameBoard, square):
        self.gameBoard = gameBoard
        self.grid = GridWithWeights(len(gameBoard[0]), len(gameBoard))
        self.grid.weights = square
        for i in gameBoard:
            var = [j for j, x in enumerate(i) if x == 3]
            for k in var:
                if (i, k) == (12, 13) or (i, k) == (12, 14):
                    pass
                self.grid.walls.append((i, k))

    def heuristic(self, a: GridLocation, b: GridLocation) -> float:
        (x1, y1) = a
        (x2, y2) = b
        return sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def search(self, start: GridLocation, goal: GridLocation):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from: dict[GridLocation, Optional[GridLocation]] = {}
        cost_so_far: dict[GridLocation, float] = {}
        came_from[start] = None
        cost_so_far[start] = 0

        step = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            step += 1

            for next in self.grid.neighbors(current):
                new_cost = cost_so_far[current] + self.grid.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(next, goal)
                    frontier.put(next, priority)
                    came_from[next] = current

        #return came_from, cost_so_far
        return came_from, cost_so_far
