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
PLAYER_HP = 100
PLAYER_MAX_HP = 100
PLAYER_INVICIBILITY_TIME = 1000  # milliseconds

# Enemy Settings
ENEMY_SPEED = 2
ENEMY_HP = 20
ENEMY_DAMAGE = 10
SPAWN_INTERVAL = 1000  # milliseconds

# Enemy-specific settings
SQUARE_ENEMY_SPEED = 1.5
SQUARE_ENEMY_HP = 40
SQUARE_ENEMY_DAMAGE = 15

TRIANGLE_ENEMY_SPEED = 3
TRIANGLE_ENEMY_HP = 15
TRIANGLE_ENEMY_DAMAGE = 8
TRIANGLE_ENEMY_PROJECTILE_COOLDOWN = 500  # milliseconds
TRIANGLE_ENEMY_PROJECTILE_DAMAGE = 5

FAST_ENEMY_SPEED = 4
FAST_ENEMY_HP = 10
FAST_ENEMY_DAMAGE = 5

# BOSS_SPAWSN_INTERVAL = 300000  # 5 minutes in milliseconds
BOSS_SPAWN_INTERVAL = 5 *1000