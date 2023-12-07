# constant.py

# Dimensions of the game window
WIDTH = 80
HEIGHT = 30

# Maximum coordinates for the game area, accounting for borders
MAX_X = WIDTH - 5
MAX_Y = HEIGHT - 5

# Timeout value for controlling the speed of the game
TIMEOUT = 60

# Initial length of the snake
SNAKE_LEN = 5

# Initial position of the snake
SNAKE_X = SNAKE_LEN + 1
SNAKE_Y = 3

# Characters representing different elements in the game
BODY_CHAR = "~"   # Character for the snake's body segments
HEAD_CHAR = "%"   # Character for the snake's head
FOOD_CHAR = "@"   # Character for the food item
