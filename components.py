# components.py

from curses import KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT
from random import randint

from constant import *

class Body(object):
    """ Represents a body segment of the snake """
    def __init__(self, x, y, char=BODY_CHAR):
        """ Initializes a body segment with a specified position and character """
        self.x = x
        self.y = y
        self.char = char

    @property
    def position(self):
        """ Returns the position of the body segment """
        return self.x, self.y


class Food(object):
    """ Represents a food item with random location """
    def __init__(self, window, snake, char=FOOD_CHAR):
        """ Initializes a food item with a random location and character """
        self.x = randint(10, MAX_X)
        self.y = randint(10, MAX_Y)
        self.char = char
        self.window = window
        self.snake = snake

    def render(self):
        """ Renders the food item on the game window """
        self.window.addstr(self.y, self.x, self.char)

    def reset(self):
        """ Resets the food item to a new random location """
        self.x = randint(10, MAX_X)
        self.y = randint(10, MAX_Y)

        if self.collides():
            self.reset()

    def collides(self):
        """ Checks if the food item collides with the snake's body """
        return any([body.position == (self.x, self.y) for body in self.snake.body[:-1]])


class Snake(object):
    """ Represents the snake in the game """
    def __init__(self, x, y, window):
        """ Initializes the snake with a specified position and window """
        self.window = window
        self.body = list()
        self.score = 0
        self.headCharacter = HEAD_CHAR
        self.timeout = TIMEOUT

        # Create the initial body segments of the snake
        for i in range(SNAKE_LEN, 0, -1):
            self.body.append(Body(x, y))

        self.body.append(Body(x, y, self.headCharacter))
        self.direction = KEY_RIGHT
        self.last = (x, y)

        # Dictionary mapping keys to corresponding movement methods
        self.move = {
            KEY_UP: self.moveUp,
            KEY_DOWN: self.moveDown,
            KEY_LEFT: self.moveLeft,
            KEY_RIGHT: self.moveRight
        }

        # Dictionary mapping keys to their opposites
        self.invalid = {
            KEY_UP: KEY_DOWN,
            KEY_DOWN: KEY_UP,
            KEY_LEFT: KEY_RIGHT,
            KEY_RIGHT: KEY_LEFT
        }

    @property
    def getScore(self):
        """ Returns the current score as a formatted string """
        return "Score : " + str(self.score)

    def eatFood(self, food: Food):
        """ Handles the snake eating a food item """
        food.reset()
        body = Body(self.last[0], self.last[1])
        self.body.insert(-1, body)
        self.score += 1

        # Adjust game speed based on score
        if self.score % 3 == 0:
            if self.timeout > 20:
                self.timeout -= 5
            self.window.timeout(self.timeout)

    @property
    def head(self):
        """ Returns the head of the snake """
        return self.body[-1]

    def collided(self):
        """ Checks if the snake collides with itself """
        return any([body.position == self.head.position for body in self.body[:-1]])

    def update(self):
        """ Updates the position of the snake """
        last = self.body.pop(0)
        last.x = self.body[-1].x
        last.y = self.body[-1].y

        self.body.insert(-1, last)
        self.last = (self.head.x, self.head.y)
        self.move[self.direction]()

    def makeMove(self, direction):
        """ Updates the snake's direction based on user input """
        # If the key and current directions are opposite, don't react
        if direction != self.invalid[self.direction]:
            self.direction = direction

    def render(self):
        """ Renders the snake on the game window """
        for body in self.body:
            self.window.addstr(body.y, body.x, body.char)

    # Movement methods for different directions
    def moveUp(self):
        self.head.y -= 1

        if self.head.y < 1:
            self.head.y = MAX_Y

    def moveDown(self):
        self.head.y += 1

        if self.head.y > MAX_Y:
            self.head.y = 1

    def moveLeft(self):
        self.head.x -= 1

        if self.head.x < 1:
            self.head.x = MAX_X

    def moveRight(self):
        self.head.x += 1

        if self.head.x > MAX_X:
            self.head.x = 1
