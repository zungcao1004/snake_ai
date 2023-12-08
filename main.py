# main.py

import curses
import sys

from astar import AStar
from components import *


class StdOutWrapper:
    """ Helper class to capture and print terminal output """
    text = ""

    def write(self, txt):
        """ Append text to the internal buffer """
        self.text += txt
        self.text += "\n"

    def get_text(self):
        """ Get the captured text """
        return self.text


def startGame():
    # Redirect stdout and stderr to a custom wrapper
    mystdout = StdOutWrapper()
    sys.stdout = mystdout
    sys.stderr = mystdout

    # Initialize the curses window
    curses.initscr()
    window = curses.newwin(HEIGHT, WIDTH, 0, 0)
    window.timeout(TIMEOUT)
    window.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    window.border(0)

    # Initialize game components
    snake = Snake(SNAKE_X, SNAKE_Y, window)
    food = Food(window, snake)
    astar = AStar()

    while True:
        window.clear()
        window.border(0)

        # Render the game objects
        snake.render()
        food.render()

        window.addstr(0, 5, snake.getScore)
        event = window.getch()

        if event == 27:  # ASCII value for 'Esc' key
            break

        # Check if snake has reached the food
        if snake.head.x == food.x and snake.head.y == food.y:
            snake.eatFood(food)

        # Use A* algorithm to get the next step
        event = astar.get_next_step(food, snake)

        # Update snake direction based on user input
        if event in (KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT):
            snake.makeMove(event)

        # Update snake position
        snake.update()

        # Check for collision
        if snake.collided():
            break

    # End curses and print the high score
    curses.endwin()
    print(f"High score :: {snake.score}")

    # Restore standard output and print captured text
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    sys.stdout.write(mystdout.get_text())


if __name__ == "__main__":
    startGame()
