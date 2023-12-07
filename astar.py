# astar.py

from queue import PriorityQueue

from components import *

class AStar:
    """
    A* algorithm implementation for finding the next step in the Snake game.
    The A* algorithm uses the formula f(n) = g(n) + h(n), where g(n) is the cost
    of the path from the starting node to node n, and h(n) is an admissible heuristic
    estimate of the cost from node n to the goal.

    In the context of the Snake game:
    - g(n) is represented by the number of moves made by the snake.
    - h(n) is the Manhattan distance from the snake's head to the food.
    """

    def __init__(self):
        # Possible movement directions
        self.paths = [
            KEY_RIGHT,
            KEY_LEFT,
            KEY_UP,
            KEY_DOWN
        ]

        # Dictionary mapping keys to their opposites
        self.invalid = {
            KEY_UP: KEY_DOWN,
            KEY_DOWN: KEY_UP,
            KEY_LEFT: KEY_RIGHT,
            KEY_RIGHT: KEY_LEFT
        }

        # Counter for the number of moves made by the snake
        self.moves = 0

    def collides(self, headPosition, snake):
        """ Check for body collision on the next step """
        return any([body.position == headPosition for body in snake.body[: -1]])

    def getDistances(self, goal, current, snake):
        """ Calculate distances for each possible path """
        distances = PriorityQueue()
        self.moves += 1

        for path in self.paths:
            x = None
            y = None
            goal_x = goal.x
            goal_y = goal.y

            # Calculate the next position based on the chosen path
            if path is KEY_UP:
                x = current.x
                y = current.y - 1

            elif path is KEY_DOWN:
                x = current.x
                y = current.y + 1

            elif path is KEY_RIGHT:
                x = current.x + 1
                y = current.y

            elif path is KEY_LEFT:
                x = current.x - 1
                y = current.y

            # Skip paths where the snake collides with itself
            if self.collides((x, y), snake):
                continue

            # Calculate g(n), h(n), and f(n)
            gn = self.moves
            hn = abs(x - goal_x) + abs(y - goal_y)
            fn = gn + hn

            # Add to the priority queue
            distances.put((fn, path))

        return distances

    def get_next_step(self, food, snake):
        """ Returns the next step based on A* algorithm """
        if snake.head.x == food.x and snake.head.y:
            self.moves = 0
            return snake.direction

        distances = self.getDistances(food, snake.head, snake)

        if distances.qsize() == 0:
            return snake.direction

        return distances.get()[1]
