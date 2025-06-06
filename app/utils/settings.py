import pygame

# Screen Settings
FULLSCREEN = True  # Set to True for fullscreen mode
SCREEN_WIDTH = 800  # Default width (used when not in fullscreen)
SCREEN_HEIGHT = 600  # Default height (used when not in fullscreen)
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
GREY = (128, 128, 128)

# Game Settings
GAME_TITLE = "Mage Cats"
GAME_TIME_LIMIT = 300 # 5 minutes in seconds 

# Player Settings
PLAYER_SPEED = 5
PLAYER_HP = 1
PLAYER_MAX_HP = 1

# Enemy Settings
ENEMY_SPEED = 2
SPAWN_INTERVAL = 1000  # milliseconds

# Enemy-specific settings
SQUARE_ENEMY_SPEED = 1.5
SQUARE_ENEMY_HP = 40
SQUARE_ENEMY_DAMAGE = 15

TRIANGLE_ENEMY_SPEED = 3
TRIANGLE_ENEMY_HP = 15
TRIANGLE_ENEMY_DAMAGE = 8

FAST_ENEMY_SPEED = 4
FAST_ENEMY_HP = 10
FAST_ENEMY_DAMAGE = 5